# Pulp Governance

A starter LaTeX project for preparing a governance presentation and its
supporting textual draft. Replace the prompts and author details with project
content.

## Requirements

- GNU Make
- `uv` for the speech-time estimator; Rich and Watchfiles are declared in the
  script
- `latexmk`
- `rsvg-convert` for embedding the Pulp logo, mascot, and pattern cell SVGs in the PDF presentation
- `texcount` (usually included with TeX Live)
- A LaTeX installation with Beamer and the packages used by the draft
- `latexindent` for formatting
- A PDF viewer for live preview

## Commands

Run `make` or `make help` to see the available commands.

| Command | Purpose |
| --- | --- |
| `make presentation` | Build and continuously preview `presentation.tex` |
| `make presentation-build` | Build the presentation PDF |
| `make draft` | Build and continuously preview `draft.tex` |
| `make draft-build` | Build the draft PDF |
| `make speech-time REFERENCE_SECONDS=32` | Estimate speech time using the measured reference-speech duration in seconds |
| `make speech-time REFERENCE_SECONDS=32 SWITCH_COST_SECONDS=5` | Set the fixed cost of switching sections and subsections |
| `make speech-time REFERENCE_SECONDS=32 WATCH=1` | Refresh the colored estimate when the draft or calibration speech changes |
| `make format` | Format both LaTeX sources with `latexindent` |
| `make clean` | Remove generated files |

Read `references/reference-speech.txt` aloud, measure the time it takes in
seconds, then pass that duration to `make speech-time`. For example:
`make speech-time REFERENCE_SECONDS=32`. The estimator uses the reference
speech's word count to infer your speaking pace. It excludes the abstract,
Revision, and References sections from the draft estimate. TeX `%` comments and
text inside `comment` environments are ignored. `WATCH` defaults to `0`; set it
to `1` to refresh the count when `draft.tex` or the calibration speech changes.
Stop watching with `Ctrl-C`. The estimate displays section and
subsection times separately; each parent section includes the times of its
descendants, and the `Presentation` row is the simple total. The final total
adds `SWITCH_COST_SECONDS` for each transition between top-level sections and
between sibling subsections. The switch cost defaults to 5 seconds and can be
set to 0 to disable it.

Run the estimator directly with `uv run scripts/speech_time.py --reference-time
32 --switch-cost-seconds 5 --watch 1`. The script declares Rich and Watchfiles
inline, so `uv` creates the required environment automatically.

Preview commands keep watching their source until stopped with `Ctrl-C`. PDFs
and LaTeX build files are written to `_build/`.

## Files

- `presentation.tex` — Beamer slide outline
- `assets/pulp-logo.svg` — Pulp logo copied from the project branding assets
- `assets/pulp-mascot.svg` — vector mascot shown on the title slide
- `assets/pulp-leaves-cell.svg` — leaves-only pattern cell with one broad, smooth-edged leaf shape in varied sizes
- `assets/pulp-citrus-cell.svg` — citrus-only pattern cell with three slice sizes
- `assets/pulp-leaf-citrus-cell.svg` — mixed leaf and citrus pattern cell
- `draft.tex` — paper-style textual preparation
- `scripts/speech_time.py` — speech-time estimator using TeXcount
- `references/reference-speech.txt` — short speech for pacing calibration
- `Makefile` — build, preview, formatting, and help commands
