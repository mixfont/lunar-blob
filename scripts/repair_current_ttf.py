#!/usr/bin/env python3
"""Repair the current Lunar Blob TTF for Google Fonts QA.

This is a bridge script for the current binary-only state. The final Google
Fonts submission should apply the same decisions in the editable sources and
rebuild from source.
"""

from __future__ import annotations

import unicodedata
import os
from pathlib import Path

from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables.ttProgram import Program


FONT_PATH = Path("fonts/ttf/LunarBlob-Regular.ttf")
FAMILY_NAME = "Lunar Blob"
STYLE_NAME = "Regular"
FULL_NAME = "Lunar Blob Regular"
POSTSCRIPT_NAME = "LunarBlob-Regular"
VERSION = "Version 1.000"
REPO_URL = os.environ.get("LUNAR_BLOB_REPO_URL", "TODO_REPO_URL")
COPYRIGHT = f"Copyright 2026 The Lunar Blob Project Authors ({REPO_URL})"
LICENSE = (
    "This Font Software is licensed under the SIL Open Font License, Version 1.1. "
    "This license is available with a FAQ at: https://openfontlicense.org"
)
LICENSE_URL = "https://openfontlicense.org"


def set_name(font: TTFont, name_id: int, value: str) -> None:
    name_table = font["name"]
    name_table.removeNames(nameID=name_id)
    name_table.setName(value, name_id, 3, 1, 0x409)
    name_table.setName(value, name_id, 1, 0, 0)


def draw_notdef(font: TTFont) -> None:
    glyph_order = font.getGlyphOrder()
    glyph_set = font.getGlyphSet()
    width = font["hmtx"].metrics.get(".notdef", (500, 0))[0]
    units = font["head"].unitsPerEm
    pad = max(40, round(width * 0.12))
    x_min = pad
    x_max = max(pad + 1, width - pad)
    y_min = round(-0.18 * units)
    y_max = round(0.72 * units)

    pen = TTGlyphPen(glyph_set)
    pen.moveTo((x_min, y_min))
    pen.lineTo((x_min, y_max))
    pen.lineTo((x_max, y_max))
    pen.lineTo((x_max, y_min))
    pen.closePath()

    inner_pad = max(24, round(width * 0.22))
    ix_min = inner_pad
    ix_max = max(ix_min + 1, width - inner_pad)
    iy_min = round(0.02 * units)
    iy_max = round(0.52 * units)
    pen.moveTo((ix_min, iy_min))
    pen.lineTo((ix_max, iy_min))
    pen.lineTo((ix_max, iy_max))
    pen.lineTo((ix_min, iy_max))
    pen.closePath()

    font["glyf"][".notdef"] = pen.glyph()
    if glyph_order[0] != ".notdef":
        glyph_order.remove(".notdef")
        font.setGlyphOrder([".notdef", *glyph_order])


def build_kern_feature(font: TTFont) -> list[str]:
    if "kern" not in font:
        return []

    pairs: dict[tuple[str, str], int] = {}
    for subtable in font["kern"].kernTables:
        for pair, value in subtable.kernTable.items():
            if value:
                pairs[pair] = value

    del font["kern"]

    if not pairs:
        return []

    lines = [
        "feature kern {",
    ]
    for (left, right), value in sorted(pairs.items()):
        lines.append(f"  pos {left} {right} {value};")
    lines.append("} kern;")
    return lines


def add_gasp(font: TTFont) -> None:
    gasp = newTable("gasp")
    gasp.version = 1
    gasp.gaspRange = {0xFFFF: 0x000F}
    font["gasp"] = gasp


def add_prep(font: TTFont) -> None:
    prep = newTable("prep")
    prep.program = Program()
    # PUSHW 0x01FF; SCANCTRL; PUSHB 0x04; SCANTYPE
    prep.program.fromBytecode([0xB8, 0x01, 0xFF, 0x85, 0xB0, 0x04, 0x8D])
    font["prep"] = prep


def add_meta(font: TTFont) -> None:
    meta = newTable("meta")
    meta.data = {"dlng": "Latn", "slng": "Latn"}
    font["meta"] = meta


def _bbox(font: TTFont, glyph_name: str) -> tuple[int, int, int, int]:
    glyph = font["glyf"][glyph_name]
    if glyph.numberOfContours == 0:
        width = font["hmtx"].metrics[glyph_name][0]
        return 0, 0, width, 0
    return glyph.xMin, glyph.yMin, glyph.xMax, glyph.yMax


def _center_x(font: TTFont, glyph_name: str) -> int:
    x_min, _, x_max, _ = _bbox(font, glyph_name)
    return round((x_min + x_max) / 2)


def build_mark_features(font: TTFont) -> list[str]:
    cmap = font.getBestCmap()
    top_marks = []
    bottom_marks = []
    base_glyphs = []

    for codepoint, glyph_name in sorted(cmap.items()):
        category = unicodedata.category(chr(codepoint))
        if category.startswith("M"):
            if codepoint in {0x0326, 0x0327, 0x0328}:
                bottom_marks.append(glyph_name)
            else:
                top_marks.append(glyph_name)
        elif glyph_name != ".notdef":
            base_glyphs.append(glyph_name)

    if not top_marks and not bottom_marks:
        return []

    lines = []

    for glyph_name in top_marks:
        x_min, y_min, x_max, _ = _bbox(font, glyph_name)
        lines.append(
            f"markClass {glyph_name} <anchor {round((x_min + x_max) / 2)} {y_min}> @MC_TOP;"
        )

    for glyph_name in bottom_marks:
        x_min, _, x_max, y_max = _bbox(font, glyph_name)
        lines.append(
            f"markClass {glyph_name} <anchor {round((x_min + x_max) / 2)} {y_max}> @MC_BOTTOM;"
        )

    lines.append("feature mark {")
    for glyph_name in base_glyphs:
        x_min, y_min, x_max, y_max = _bbox(font, glyph_name)
        x = round((x_min + x_max) / 2)
        anchors = []
        if top_marks:
            anchors.append(f"<anchor {x} {y_max + 40}> mark @MC_TOP")
        if bottom_marks:
            anchors.append(f"<anchor {x} {y_min - 40}> mark @MC_BOTTOM")
        lines.append(f"  pos base {glyph_name} {' '.join(anchors)};")
    lines.append("} mark;")

    lines.append("feature mkmk {")
    for glyph_name in top_marks:
        x_min, _, x_max, y_max = _bbox(font, glyph_name)
        x = round((x_min + x_max) / 2)
        lines.append(f"  pos mark {glyph_name} <anchor {x} {y_max + 40}> mark @MC_TOP;")
    for glyph_name in bottom_marks:
        x_min, y_min, x_max, _ = _bbox(font, glyph_name)
        x = round((x_min + x_max) / 2)
        lines.append(
            f"  pos mark {glyph_name} <anchor {x} {y_min - 40}> mark @MC_BOTTOM;"
        )
    lines.append("} mkmk;")

    return lines


def main() -> None:
    font = TTFont(FONT_PATH)

    set_name(font, 0, COPYRIGHT)
    set_name(font, 1, FAMILY_NAME)
    set_name(font, 2, STYLE_NAME)
    set_name(font, 3, "1.000;LunarBlob-Regular")
    set_name(font, 4, FULL_NAME)
    set_name(font, 5, VERSION)
    set_name(font, 6, POSTSCRIPT_NAME)
    set_name(font, 13, LICENSE)
    set_name(font, 14, LICENSE_URL)

    font["head"].fontRevision = 1.0

    os2 = font["OS/2"]
    os2.version = max(os2.version, 4)
    os2.fsType = 0
    os2.fsSelection |= 1 << 7
    os2.usWinAscent = max(os2.usWinAscent, font["head"].yMax)
    os2.usWinDescent = max(os2.usWinDescent, abs(font["head"].yMin))
    os2.ulCodePageRange1 = 1
    os2.ulCodePageRange2 = 0

    draw_notdef(font)
    if "kern" in font or "GPOS" not in font:
        feature_lines = [
            "languagesystem DFLT dflt;",
            "languagesystem latn dflt;",
        ]
        feature_lines.extend(build_kern_feature(font))
        feature_lines.extend(build_mark_features(font))
        if len(feature_lines) > 2:
            if "GPOS" in font:
                del font["GPOS"]
            addOpenTypeFeaturesFromString(font, "\n".join(feature_lines))

    add_gasp(font)
    add_prep(font)
    add_meta(font)

    font.save(FONT_PATH)


if __name__ == "__main__":
    main()
