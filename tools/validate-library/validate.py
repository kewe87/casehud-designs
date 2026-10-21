#!/usr/bin/env python3
"""Validate components/, cases/, lighting/ and their indexes against schema/.

Usage: python tools/validate-library/validate.py [repo-dir]
Needs: pip install jsonschema
"""
import json
import pathlib
import sys

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
bad = 0


def fail(msg):
    global bad
    bad += 1
    print("FAIL:", msg)


def load(p):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        fail(f"{p.relative_to(root)}: {e}")
        return None


# schema registry so that relative $refs ("common.schema.json#/...") resolve
schemas = {}
registry = Registry()
for f in sorted((root / "schema").glob("*.schema.json")):
    doc = load(f)
    schemas[f.name] = doc
    res = Resource.from_contents(doc)
    registry = registry.with_resource(doc["$id"], res).with_resource(f.name, res)

for name, doc in schemas.items():
    Draft202012Validator.check_schema(doc)


def validator(name):
    return Draft202012Validator(schemas[name], registry=registry)


def schema_check(path, doc, schema):
    for e in sorted(validator(schema).iter_errors(doc), key=lambda e: list(e.path)):
        loc = "/".join(str(x) for x in e.absolute_path)
        fail(f"{path.relative_to(root)}: {loc}: {e.message[:200]}")


def inside(p, w, h, tol=1.0):
    return -tol <= p[0] <= w + tol and -tol <= p[1] <= h + tol


def check_component(path, d):
    dim = d["dimensions_mm"]
    if d["id"] != path.stem:
        fail(f"{path.name}: id must equal the file name")
    if "leds" in d:
        leds = d["leds"]
        pos = leds["positions_mm"]
        if leds["count"] != len(pos):
            fail(f"{path.name}: leds.count {leds['count']} != {len(pos)} positions")
        for i, p in enumerate(pos):
            if not inside(p, dim["w"], dim["h"]):
                fail(f"{path.name}: LED {i} at {p} lies outside {dim['w']}x{dim['h']} mm")
        nxt = 0
        for z in leds.get("zones", []):
            if z["first"] != nxt:
                fail(f"{path.name}: zone {z['id']} must start at {nxt}")
            nxt = z["first"] + z["count"]
        if leds.get("zones") and nxt != leds["count"]:
            fail(f"{path.name}: zones cover {nxt} of {leds['count']} LEDs")
    if "display" in d and d["display"].get("area_mm"):
        a = d["display"]["area_mm"]
        if a["x"] < 0 or a["y"] < 0 or a["x"] + a["w"] > dim["w"] + 1 or a["y"] + a["h"] > dim["h"] + 1:
            fail(f"{path.name}: display area outside the part")


def check_case(path, d):
    if d["id"] != path.stem:
        fail(f"{path.name}: id must equal the file name")
    for m in d.get("mounts", []):
        v = d["views"].get(m["view"])
        if not v:
            fail(f"{path.name}: mount {m['id']} uses missing view {m['view']}")
            continue
        for lay in m["layouts"]:
            if len(lay["snap_mm"]) != lay["count"]:
                fail(f"{path.name}: mount {m['id']} layout {lay['fan_mm']}: snap points != count")
            for p in lay["snap_mm"]:
                if not inside(p, v["size_mm"]["w"], v["size_mm"]["h"]):
                    fail(f"{path.name}: mount {m['id']} snap point {p} outside the view")


def check_set(folder, schema, check, index_name, list_key):
    files = sorted((root / folder).rglob("*.json")) if (root / folder).is_dir() else []
    seen = {}
    for f in files:
        d = load(f)
        if d is None:
            continue
        schema_check(f, d, schema)
        if "id" in d and "format" in d:
            if d["id"] in seen:
                fail(f"{f.relative_to(root)}: duplicate id {d['id']}")
            seen[d["id"]] = f
            if folder in ("components", "cases") and f.parent.name == folder:
                fail(f"{f.relative_to(root)}: must be in a <vendor> sub folder")
            if check:
                try:
                    check(f, d)
                except KeyError:
                    pass  # already reported by the schema check
    idx_path = root / index_name
    idx = load(idx_path) if idx_path.exists() else None
    if idx is None:
        if files:
            fail(f"{index_name} missing")
        return
    listed = {}
    for e in idx.get(list_key, []):
        listed[e["id"]] = e
        f = root / e["file"]
        if ".." in e["file"] or not f.is_file():
            fail(f"{index_name}: {e['id']}: file {e['file']} not found")
        elif e["id"] not in seen or seen[e["id"]] != f:
            fail(f"{index_name}: {e['id']} does not match {e['file']}")
    for i in seen:
        if i not in listed:
            fail(f"{index_name}: {i} is not listed")


check_set("components", "component.schema.json", check_component, "components.json", "components")
check_set("cases", "case.schema.json", check_case, "cases.json", "cases")
check_set("lighting", "lighting.schema.json", None, "lighting.json", "presets")

# keep the designs index in the format CaseHUD parses
d = load(root / "index.json")
if d is not None and (d.get("version") != 1 or not isinstance(d.get("designs"), list)):
    fail("index.json: expected {version:1, designs:[...]}")

print("OK" if not bad else f"{bad} problem(s)")
sys.exit(1 if bad else 0)
