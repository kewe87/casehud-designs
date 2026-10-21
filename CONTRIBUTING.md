# Contributing

- One design per pull request is easiest to review.
- Follow the rules in the [README](README.md#rules); CI must be green.
- Author in `index.json` is your GitHub user name.
- Maintainer review checks readability on small displays and that the
  sources are generic. Designs that are offensive, misleading or contain
  personal data are rejected.
- Changing an existing design: only by its author, or to fix a bug.
- Questions: open an issue.
- Components, cases and lighting presets: follow the
  [README](README.md#contributing-components-and-cases) and [docs/components.md](docs/components.md).
  Every entry needs `sources` (or a note on how it was measured) and an honest `verified_by`;
  mark estimated geometry `approximate: true`. CI runs `tools/validate-library/validate.py`.
- Never submit data copied from other software's files or from material you may not redistribute.
