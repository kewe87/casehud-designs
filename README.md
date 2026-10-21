# CaseHUD library

Community library for [CaseHUD](https://github.com/kewe87/CaseHUD): LCD dashboard
**designs**, hardware **components** and **case templates** (for the LED layout editor) and
ready-made **lighting presets**.

| Content | Folder | Index | Format |
|---|---|---|---|
| LCD designs | `designs/` | `index.json` | see below |
| Hardware components (fans, RAM, blocks, strips, displays, boards) | `components/<vendor>/` | `components.json` | [docs/components.md](docs/components.md), `schema/component.schema.json` |
| Case templates | `cases/<vendor>/` | `cases.json` | same, `schema/case.schema.json` |
| Lighting presets | `lighting/` | `lighting.json` | same, `schema/lighting.schema.json` |

Community designs for CaseHUD's LCD gallery:
CaseHUD's in-app gallery (Designs > Community) reads `index.json` from this
repository and renders previews locally, so no images are needed.

## Using a design

Open the community gallery in CaseHUD, pick a design, click **Import**. It is
saved as a normal design (`community-<id>`) that you can edit or put into a
rotation. Nothing is downloaded until you open the gallery.

## Contributing a design

1. In CaseHUD, build your design in the editor and export/copy its JSON
   (or take the file from your CaseHUD config folder, `designs\<id>.json`).
2. Fork this repository and add the file as `designs/<id>.json`.
3. Add an entry to `index.json`:

   ```json
   {"id": "my-design", "name": "My Design", "author": "your-github-name",
    "description": "One short sentence.", "round": true,
    "file": "designs/my-design.json"}
   ```

4. Open a pull request. CI checks it with the same parser the app uses.

### Rules

- `id`: lowercase `a-z`, `0-9` and `-`, at most 48 characters, unique.
- `file`: relative path `designs/<name>.json` (no URLs, no `..`).
- `round` in the index must match `"round"` in the design.
- Design file: at most 256 KiB, size 1-1024 px per side, 1-64 widgets.
- Sensor sources must be generic, e.g. `Load/CPU Total`, with fallbacks
  separated by `|`, so it works on other people's hardware.
- No `lhm_url` (the app ignores it anyway), no personal data.
- Keep text readable on small (about 2 inch) displays.
- Only designs you made yourself or that you may license under CC BY 4.0.

Check locally (needs a CaseHUD checkout and Go): copy `tools/validate/main.go`
to `<casehud>/cmd/validate-designs/main.go`, then run
`go run ./cmd/validate-designs <path-to-this-repo>`.

## Contributing components and cases

Components and cases describe real hardware to scale (millimetres), so accuracy and sources matter.
The full format is in [docs/components.md](docs/components.md).

1. Copy an existing file from `components/` (or `cases/`) as a template and put yours at
   `components/<vendor>/<id>.json`; `<id>` = file name = `id`, lowercase `a-z0-9-`.
2. Fill in dimensions, outline and LEDs (`positions_mm` in the order the device addresses them).
3. Record where the data comes from: `sources` (manufacturer pages first, reputable retailers second)
   and `verified_by`: `measured` (you measured it on your own hardware, say how in `notes`),
   `manufacturer` (published data) or `community`.
4. Positions you had to estimate from photos or dimensions: set `approximate: true`. If the
   manufacturer and your measurement disagree (for example the LED count), fill both
   `manufacturer_count` and `measured_count` and explain in `notes`.
5. Add the entry to `components.json` / `cases.json`, run
   `pip install jsonschema && python tools/validate-library/validate.py .` and open a pull request.

Do not copy files, drawings or data from other software or from manufacturer downloads you may not
redistribute: measure the part, or use dimensions from public specification pages, and draw the
outline yourself.

## Contributing lighting presets

Put `lighting/<id>.json` (one effect with its parameters, names/descriptions in German and English,
tags, `author` = your GitHub name, `license` = `CC-BY-4.0`), list it in `lighting.json`, validate with the
script above. Presets must be your own work.

## Licenses

- Designs, components, cases and lighting presets (`designs/`, `components/`, `cases/`, `lighting/`,
  the index files and `schema/`): [CC BY 4.0](LICENSE). They are
  creative data, not code, and CC BY keeps the author credited when a design
  is remixed. By contributing you agree to this license.
- `tools/`: GPL-3.0-or-later, like CaseHUD itself (it builds on CaseHUD code).
