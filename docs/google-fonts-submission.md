# Google Fonts Submission Notes

Verified against the Google Fonts Guide on 2026-06-05.

## Official Requirements Summary

- The project must be wholly licensed under the SIL Open Font License v1.1.
- The OFL must not reserve the family name unless Google has explicit approval.
- The copyright line in `OFL.txt` must match the font name table copyright.
- The project must be hosted in a public VCS repository by completion.
- Source files must live in `sources/`.
- A one-command build must reproduce the binaries.
- TTF binaries must be available under `fonts/ttf/`.
- Fonts should meet at least the GF Latin Core glyph set.
- Fonts must pass Google Fonts QA checks before publication.
- The final contribution is usually a PR to `google/fonts` under `ofl/lunarblob`.

Official references:

- https://googlefonts.github.io/gf-guide/onboarding.html
- https://googlefonts.github.io/gf-guide/upstream.html
- https://googlefonts.github.io/gf-guide/production.html
- https://googlefonts.github.io/gf-guide/requirements.html
- https://googlefonts.github.io/gf-guide/license-file.html
- https://googlefonts.github.io/gf-guide/qa.html
- https://googlefonts.github.io/gf-guide/making-pr.html

## Current Font Audit

Working font:

- `fonts/ttf/LunarBlob-Regular.ttf`

Current known facts:

- Internal family name was changed from `Lunar Blob Grotesk` to `Lunar Blob`.
- Canonical Google Fonts filename is now `LunarBlob-Regular.ttf`.
- The font is static, Regular, weight 400, width class 5.
- The font contains 319 encoded codepoints.
- The encoded set exactly matches the installed `GF_Latin_Core.nam` set.
- The repaired font has an OFL license string and URL in name IDs 13 and 14.
- The repaired font has `OS/2.fsType` set to `0`, which is required for Google Fonts.
- The repaired font has `kern`, `mark`, and `mkmk` GPOS features.
- The repaired font currently has `TODO_REPO_URL` in name ID 0; replace this with the final public repository URL before submission.

## Google Fonts QA Failures

Initial audit summary before repairs:

- 12 FAIL
- 14 WARN
- 76 PASS

Post-rename command:

```sh
PATH=/tmp/lunar-blob-fontenv/bin:$PATH scripts/qa.sh
```

Post-rename summary before repairs:

- 10 FAIL
- 14 WARN
- 87 PASS

The canonical filename and Google Fonts font-name failures were fixed by the
rename.

Current repaired command:

```sh
LUNAR_BLOB_REPO_URL=https://github.com/YOUR_ACCOUNT/lunar-blob scripts/repair_current_ttf.py
PATH=/tmp/lunar-blob-fontenv/bin:$PATH scripts/qa.sh
```

Current repaired summary:

- 0 FAIL
- 12 WARN
- 102 PASS

Failures fixed by `scripts/repair_current_ttf.py`:

- No OS/2 code pages are defined.
- `head.fontRevision` is `1.00000`, but name ID 5 says `Version 0.001`.
- `OS/2.usWinAscent` is lower than `head.yMax`.
- `.notdef` is blank.
- Missing smart dropout control in `prep`.
- `kern` table has a malformed/oversized subtable warning during TTX roundtrip.
- `OS/2.fsType` is restricted and must be zero for Google Fonts.
- Missing `gasp` table.
- Name ID 5 must be `Version X.Y` with version at least `1.000`.
- `OS/2.fsSelection` bit 7, USE_TYPO_METRICS, is not set.
- Combining mark shaping failed for some Latin language tests.

Remaining warnings to review:

- Combining mark glyphs have nonzero advance widths.
- The caron variants should be manually checked.
- Contour counts differ from common reference expectations for a few glyphs.
- Math signs have inconsistent widths.
- `uni00D8` has overlapping path segments.
- Some unencoded helper glyphs are unreachable.
- The Google Fonts package article is still missing.
- Some combining marks are not covered by current subset metadata outside `latin` and `latin-ext`.
- Some auxiliary language glyphs are missing from broader trans-Latin checks.
- Soft-dotted mark behavior should be reviewed.
- `uni00FE` has a jaggy segment warning.
- Vendor ID is still `????`.

Submission blockers still open:

- Replace `TODO_REPO_URL` in `scripts/repair_current_ttf.py`, `OFL.txt`, `METADATA.pb`, and `upstream.yaml`.
- Add final `AUTHORS.txt` and `CONTRIBUTORS.txt`.
- Add real editable source files in `sources/`.
- Add a one-command source build, preferably `sources/config.yaml` for `gftools builder`.
- Replace templates in `templates/googlefonts/` with final files.
- Unknown vendor ID `????`.

## Submission Plan

1. Finalize licensing and authorship metadata.

   The project owner has confirmed rights to publish. Add the exact public repository URL, copyright holder list, designer/foundry name, and OFL files. Keep the OFL free of Reserved Font Names unless Google pre-approves an exception.

2. Add source files.

   Put real source files in `sources/` and add a one-command build. If there are no editable source files, recreate the font in a source format before submitting.

3. Port binary metadata fixes into source.

   Required values:

   - Family name: `Lunar Blob`
   - Full name: `Lunar Blob Regular`
   - PostScript name: `LunarBlob-Regular`
   - Version: `Version 1.000` or higher
   - Copyright: `Copyright 2026 The Lunar Blob Project Authors (REPO_URL)`
   - License: standard Google Fonts OFL string
   - License URL: `https://openfontlicense.org`
   - `OS/2.fsType`: `0`
   - `OS/2.fsSelection`: set USE_TYPO_METRICS

4. Port technical QA fixes into source.

   Rebuild with a proper libre toolchain, add/fix `.notdef`, vertical metrics, `gasp`, `prep`, code page bits, GPOS kerning, and mark/mkmk positioning. The current `scripts/repair_current_ttf.py` shows the decisions that need to move into source.

5. Run QA until clean enough for review.

   ```sh
   scripts/qa.sh
   ```

6. Prepare the Google Fonts package.

   In a fork of `google/fonts`, create:

   ```text
   ofl/lunarblob/
     LunarBlob-Regular.ttf
     OFL.txt
     METADATA.pb
     DESCRIPTION.en_us.html or article/ARTICLE.en_us.html
   ```

   Use `gftools add-font ofl/lunarblob`, then inspect and correct `METADATA.pb`.

7. Open the PR.

   Use a branch named `lunarblob`. One PR should affect only `ofl/lunarblob`.
