# Sources

Google Fonts requires source files and build scripts here. A binary TTF alone is not sufficient for onboarding.

Add one of these source formats:

- `LunarBlob.glyphspackage` preferred for Git
- `LunarBlob.glyphs`
- `LunarBlob.ufo`
- another editor format plus a script that converts it to UFO

Also add one command to build the fonts:

- `sources/config.yaml` for `gftools builder`
- or `sources/build.sh` if the build needs more than one command internally

The generated output should land in `fonts/ttf/LunarBlob-Regular.ttf`.

