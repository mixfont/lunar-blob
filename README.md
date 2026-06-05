![Lunar Blob header](https://static.mixfont.com/assets/20260605-234916-lunar-blob-header-p8jcvkej.webp)

# Lunar Blob

Lunar Blob is a draft Google Fonts candidate repository.

![Lunar Blob specimen](documentation/lunar-blob-specimen.png)

Current status:

- Renamed binary: `fonts/ttf/LunarBlob-Regular.ttf`
- GF Latin Core coverage: complete in the current binary
- Google Fonts QA status: 0 FAIL / 12 WARN after `scripts/repair_current_ttf.py`
- Google Fonts submission status: blocked until final authorship metadata, public repo URL, OFL files, and source files are resolved

## Required Before Submission

Google Fonts requires the project to be wholly licensed under the SIL Open Font License v1.1, with no Reserved Font Names unless pre-approved. The repaired binary currently uses `TODO_REPO_URL` in the copyright string; replace that with the final public repository URL before submission.

Add the real design sources to `sources/` in a supported format such as `.glyphspackage`, `.glyphs`, or UFO, plus a one-command build through `sources/config.yaml` or `sources/build.sh`.

After source and licensing are resolved, replace the templates in `templates/googlefonts/` with real files:

- `AUTHORS.txt`
- `CONTRIBUTORS.txt`
- `OFL.txt`
- `METADATA.pb`
- `upstream.yaml`

## QA

Install the development tools in a virtual environment:

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
```

Run the current QA helper:

```sh
LUNAR_BLOB_REPO_URL=https://github.com/YOUR_ACCOUNT/lunar-blob scripts/repair_current_ttf.py
scripts/qa.sh
```

See `docs/google-fonts-submission.md` for the active blocker list and next steps.
