# Components, cases and lighting presets

Format version **1**. The JSON Schemas live in [`schema/`](../schema/); they are the
authoritative definition, this page explains them. Fields are only ever added in a
backward-compatible way within version 1 (readers must ignore unknown optional fields
only if the schema version is higher than the one they know).

[Deutsch](#deutsch) · [English](#english)

## English

### Layout of the repository

| Path | Content | Index | Schema |
|---|---|---|---|
| `designs/` | LCD dashboard designs | `index.json` (unchanged) | CaseHUD parser |
| `components/<vendor>/<id>.json` | hardware parts (fans, RAM, blocks, strips, displays, controllers, boards) | `components.json` | `schema/component.schema.json` |
| `cases/<vendor>/<id>.json` | PC case templates | `cases.json` | `schema/case.schema.json` |
| `lighting/<id>.json` | LED effect presets | `lighting.json` | `schema/lighting.schema.json` |

`<id>` is lowercase `a-z0-9-`, at most 64 characters, and equals the file name. `<vendor>` is a
lowercase folder name (`lian-li`, `alphacool`, ...). Indexes are `{"version":1, "<list>":[...]}`
and every entry has `id` and `file` (relative path, no `..`).

### Coordinates

All lengths are **millimetres**. Origin is the **top-left corner** of the view, x to the right,
y down. For a component the view is its *front view* (the side you see through the case window);
`dimensions_mm` is `w` (x extent), `h` (y extent), `d` (depth, towards the viewer).

### Shape primitives

```json
{"type": "rect", "x": 0, "y": 0, "w": 120, "h": 124, "r": 6, "role": "body"}
{"type": "circle", "cx": 60, "cy": 62, "r": 50, "role": "display"}
{"type": "ring", "cx": 60, "cy": 62, "r_outer": 58, "r_inner": 50, "role": "lit"}
{"type": "polygon", "points": [[0,0],[10,0],[10,5]], "role": "frame"}
```

Shapes are drawn in array order (later on top). `role` is a hint for styling: `body`, `frame`,
`glass`, `display`, `lit`, `cutout`, `label`, `zone`. Optional `label` (max 80 chars).

### Component (`components/<vendor>/<id>.json`)

| Field | Meaning |
|---|---|
| `format` | always `1` |
| `id`, `vendor`, `model` | identity; `part_numbers` is an array of manufacturer SKUs |
| `category` | `fan`, `fan-lcd`, `ram`, `gpu-block`, `cpu-block`, `distro-plate`, `pump`, `reservoir`, `strip`, `display`, `controller`, `mainboard`, `case-accessory` |
| `dimensions_mm` | `{w,h,d}`, `approximate: true` if estimated |
| `outline.front` / `outline.side` | shape lists; `front` is required, `side` optional; `approximate` flag |
| `leds.count` | number of addressable LEDs |
| `leds.positions_mm` | `[x,y]` per LED, **in the order the device addresses them** (index 0 = first LED) |
| `leds.zones` | optional split into zones: `{id,name,first,count,direction}`; zones must be contiguous, start at 0 and cover all LEDs |
| `leds.direction` | free text, e.g. "13 bottom left to right, then 13 top left to right" |
| `leds.approximate` | `true` if positions were derived from photos/dimensions, not published or measured |
| `leds.measured_count`, `leds.manufacturer_count` | only if the two disagree; `count` is the preferred value |
| `connection` | `type` = `argb-header`, `usb-controller`, `smbus`, `proprietary`, `none`; `notes` |
| `usb` | `{vid, pid}` as 4 lowercase hex digits, for USB devices |
| `display` | `{width_px, height_px, area_mm}` for screens |
| `sources` | array of `{url, note}` (https only): manufacturer pages and retailers used |
| `verified_by` | array of `measured` (on the contributor's own hardware), `manufacturer` (published data), `community` |
| `notes` | free text, open questions, caveats |

A reader should treat `leds.approximate` and `dimensions_mm.approximate` as "good enough to draw,
not good enough to machine a bracket".

### Case (`cases/<vendor>/<id>.json`)

* `dimensions_mm`: external `w`, `h`, `d` exactly as the manufacturer lists them (W/H/D).
* `views.front` / `views.side`: each has `size_mm {w,h}` and `outline` (shapes: panels, glass, frame,
  chambers, cut-outs). The mapping of a view to a physical face is given in the view's `name`.
* `mounts`: fan/radiator mounting positions. Each mount has `face` (`top`, `bottom`, `front`, `rear`,
  `side`, `other`), `view`, a `region` shape (envelope incl. radiator), `layouts` (per fan size:
  `fan_mm`, `count`, `snap_mm` = fan centres in the view in mounting order), optional `radiator_mm`,
  `max_thickness_mm`, `slots` (true if the holes are slots) and `notes`.
* `integrated_lighting` (optional): lighting built into the case, e.g. an ARGB strip. Each entry is
  `{component, zone?, view, position_mm, path_mm?, notes?}`: the library component (and optionally one
  of its zones) is placed in the view, its first LED at `position_mm`, the LEDs spread evenly along the
  polyline `path_mm` in addressing order. A strip that wraps a corner uses one entry per leg/zone.
* `areas`: motherboard tray, PSU, PSU shroud, drive bays, chambers (shape + kind).
* `approximate: true` means the geometry was estimated (only `dimensions_mm` and the numeric
  fan/radiator support are published).

### Lighting presets (`lighting/<id>.json`)

* `name` and `description`: `{de, en}`.
* `effect`: one of the engine effects `rainbow`, `solid`, `breathing`, `wave`, `sensor`, `cycle`,
  `meteor`, `fill`, `burst`, `shuttle`, `bounce`, `stack`, `sparkle`, `stripes`, `sand`, `spark`,
  `meet`, `rainbow-gaps`.
* `params`: the effect's parameters with the engine's own keys (`speed` 0-100, `color`, `color1`..`colorN`,
  `colors` = how many palette colors are used, `period`, `tail`, `size`, `density`, `count`,
  `balls`, `gaps`, `scale`, `width`, `background`, `useAccent`, `sensor`, `min`, `max`, `low`, `high`,
  `smoothing`, `alternate`, `vertical`). Colors are `#rrggbb`. A sensor is a CaseHUD source
  expression with `|` fallbacks (e.g. `Temperatures/GPU Core|Temperatures/GPU Package`).
* `path` (optional): `{mode: around|horizontal|vertical|radial, mirror, reverse}`; merged over `params`
  (`mode` is the engine key `path`).
* `palette`: preview swatches (max 6) for the gallery.
* `tags`: `calm`, `gaming`, `water`, `sensor`, `party`, `night`, `clean`, `neon`, `retro`, `cyberpunk`.
* `author`, `license` (`CC-BY-4.0`).

### Validate locally

```
pip install jsonschema
python tools/validate-library/validate.py .
```

It checks schemas, file name = id, LED count = number of positions, LEDs inside the part,
zone continuity, snap points inside the view, and that every file is listed in its index.

## Deutsch

Format Version **1**. Die JSON-Schemas in [`schema/`](../schema/) sind die verbindliche Definition,
diese Seite erklärt sie nur.

* **Ordner:** `components/<hersteller>/<id>.json` (Bauteile), `cases/<hersteller>/<id>.json`
  (Gehäuse), `lighting/<id>.json` (Lichtanimationen), je mit Index `components.json`, `cases.json`,
  `lighting.json`. `designs/` + `index.json` bleiben unverändert.
* **Einheiten:** alles in Millimetern, Ursprung oben links, x nach rechts, y nach unten. Bauteile
  werden in der Vorderansicht (Blick durchs Seitenfenster) beschrieben.
* **Formen:** `rect` (mit Radius `r`), `circle`, `ring`, `polygon`; Zeichenreihenfolge = Array-Reihenfolge.
* **Bauteil:** Maße (`dimensions_mm`), Umriss (`outline.front`, optional `side`), LEDs
  (`leds.positions_mm` in der Reihenfolge, in der das Gerät sie adressiert; optional `zones`),
  Anschluss, USB-IDs, Quellen und `verified_by` (`measured` = am eigenen Gerät gemessen,
  `manufacturer` = Herstellerangabe, `community`). `approximate: true` heißt: aus Fotos/Maßen
  abgeleitet, nicht veröffentlicht.
* **Gehäuse:** Außenmaße, optional `integrated_lighting` (fest verbaute Leisten, als Bauteil + Pfad), Ansichten (`front`/`side`) als Formen, `mounts` mit Lüfter-/Radiator-
  Einbauplätzen (`snap_mm` = Lüftermitten) und `areas` (Mainboard, Netzteil, Laufwerke).
* **Lichtanimationen:** ein Effekt mit seinen Parametern (`params` mit den Original-Schlüsseln der
  LED-Engine), optional `path`, `palette` (Vorschau), `tags`, Name/Beschreibung auf Deutsch und Englisch.
* **Prüfen:** `pip install jsonschema`, dann `python tools/validate-library/validate.py .`
