# CaseHUD community designs

Community-made dashboard designs for [CaseHUD](https://github.com/kewe87/CaseHUD).
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

## Licenses

- Designs (`designs/`, `index.json`): [CC BY 4.0](LICENSE). Designs are
  creative data, not code, and CC BY keeps the author credited when a design
  is remixed. By contributing you agree to this license.
- `tools/`: GPL-3.0-or-later, like CaseHUD itself (it builds on CaseHUD code).
