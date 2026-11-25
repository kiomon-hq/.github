#!/usr/bin/env python3
"""
Kiomon — organisation profile banner.

Draws the banner at the top of `profile/README.md` from the parts the landing page uses:
the bowtie mark, Bricolage Grotesque SemiBold for the wordmark, Inter for the supporting
line, and the hero's halftone dot field.

Two variants are written, because GitHub renders the profile page in both themes:

    banner-light.svg   cream ground  — shown when the reader is in light mode
    banner-dark.svg    ink ground    — shown when the reader is in dark mode

The wordmark and the tagline are outlined, not `<text>`: GitHub serves README images
through a proxy that has never seen the site's webfonts, so a font-family declaration
would silently fall back to Arial. Optical size is applied per string, the way a browser
does it, from the variable axes in tools/fonts/.

    pip install fonttools uharfbuzz
    python tools/build-banner.py                 # writes profile/assets/
    python tools/build-banner.py --preview out   # also writes PNG previews (Chrome)

Everything here is deliberately reproducible: no image editor, no exported mockup.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = Path(__file__).resolve().parent / "fonts"

# ── Brand ─────────────────────────────────────────────────────────────────────
# Paper and ink are the landing page's own tokens. The red is sampled from the only
# surviving artefact of the mark, public/logo-128x128.png in the landing bundle.
PAPER = "#F8F7F5"
INK = "#141413"
RED = "#FD262C"
RED_ON_INK = "#FF3238"  # one step brighter, so the mark holds on #141413

# ── The mark ──────────────────────────────────────────────────────────────────
# Traced from that same 128 px PNG: contours extracted at 8×, simplified back to their
# corners, then offset 0.2 units outwards to undo the half-pixel a contour loses to
# anti-aliasing (0.969 IoU against the source, which is the raster's own noise floor).
# Coordinates stay in the PNG's box; MARK_BOX is the ink bounds, what the lockup aligns to.
MARK_BOX = (14.81, 25.22, 112.09, 103.28)
MARK_PATHS = (
    "M15.63 25.34 L33.28 64.10 L14.81 103.17 L59.14 73.51 L47.41 64.10 L59.03 54.28 Z",
    "M111.68 25.22 L56.05 64.00 L112.09 103.28 L94.22 64.00 Z",
)

# ── Composition ───────────────────────────────────────────────────────────────
W, H = 1600, 380
WORD_SIZE = 232
WORD_TRACKING = -0.022  # em; display sizes need the negative, as the hero headline does
TAG = "Memory infrastructure for intelligent systems"
TAG_SIZE = 34
TAG_TRACKING = 0.004
MARK_TO_WORD = 0.54  # gap between mark and wordmark, × cap height
WORD_TO_TAG = 0.48  # gap below the wordmark, × cap height
RADIUS = 20  # the plate's corners, so it reads as a card on GitHub's page


def num(v: float) -> str:
    return f"{v:.2f}".rstrip("0").rstrip(".")


class Face:
    """One family at one weight, shaped by HarfBuzz and outlined by fontTools."""

    def __init__(self, path: Path, weight: int) -> None:
        self.ttf = TTFont(str(path), lazy=True)
        self.upem = self.ttf["head"].unitsPerEm
        axes = {}
        if "fvar" in self.ttf:
            axes = {a.axisTag: (a.minValue, a.maxValue) for a in self.ttf["fvar"].axes}
        self.axes = axes
        self.weight = weight
        self.cap = self.ttf["OS/2"].sCapHeight or int(0.70 * self.upem)
        self.hb_font = hb.Font(hb.Face(hb.Blob.from_file_path(str(path))))

    def location(self, size: float) -> dict[str, float]:
        """The variation location a browser would pick for text set at `size`."""
        loc = {"wght": self.weight}
        if "opsz" in self.axes:
            low, high = self.axes["opsz"]
            loc["opsz"] = max(low, min(size, high))
        return loc

    def shape(self, text: str, size: float, tracking: float) -> tuple[str, tuple[float, float, float, float]]:
        """Return (path data, ink bounds) for `text` with the pen left at the origin."""
        location = self.location(size)
        self.hb_font.set_variations(location)
        glyph_set = self.ttf.getGlyphSet(location={k: v for k, v in location.items() if k in self.axes})

        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hb_font, buf, {"kern": True, "liga": True, "calt": True})

        scale = size / self.upem
        path = SVGPathPen(glyph_set, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip(".") or "0")
        bounds = BoundsPen(glyph_set)
        x = 0.0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            name = self.ttf.getGlyphName(info.codepoint)
            matrix = (scale, 0, 0, -scale, x + pos.x_offset * scale, -pos.y_offset * scale)
            glyph_set[name].draw(TransformPen(path, matrix))
            glyph_set[name].draw(TransformPen(bounds, matrix))
            x += pos.x_advance * scale + tracking * size
        return path.getCommands(), bounds.bounds or (0, 0, 0, 0)


def placed(path: str, dx: float, dy: float, fill: str, opacity: float = 1.0) -> str:
    """Move a shaped string into place without touching its path data."""
    fade = "" if opacity == 1.0 else f' fill-opacity="{num(opacity)}"'
    return (
        f'<g transform="translate({num(dx)} {num(dy)})" fill="{fill}"{fade}>'
        f'<path d="{path}"/></g>'
    )


def field(variant: str) -> str:
    """The hero's halftone dot field, faded out behind the lockup so the type stays clean."""
    dot = INK if variant == "light" else PAPER
    dots = 0.58 if variant == "light" else 0.34
    return f"""  <defs>
    <pattern id="dots" width="15" height="15" patternUnits="userSpaceOnUse">
      <circle cx="7.5" cy="7.5" r="1.15" fill="{dot}"/>
    </pattern>
    <radialGradient id="fade" cx="50%" cy="50%" r="0.62">
      <stop offset="0.30" stop-color="#000"/>
      <stop offset="1" stop-color="#fff"/>
    </radialGradient>
    <mask id="field">
      <rect width="{W}" height="{H}" rx="{RADIUS}" fill="url(#fade)"/>
    </mask>
  </defs>
  <rect width="{W}" height="{H}" rx="{RADIUS}" fill="url(#dots)" opacity="{dots}" mask="url(#field)"/>"""


def build(variant: str, word_face: Face, tag_face: Face) -> str:
    light = variant == "light"
    ground = PAPER if light else INK
    text = INK if light else PAPER
    muted_opacity = 0.62 if light else 0.55  # 5.0:1 on cream, 5.8:1 on ink
    hairline = "#DED6D0" if light else "#2B2A29"
    mark = RED if light else RED_ON_INK

    word, (word_l, _, word_r, _) = word_face.shape("Kiomon", WORD_SIZE, WORD_TRACKING)
    tag, (tag_l, _, tag_r, _) = tag_face.shape(TAG, TAG_SIZE, TAG_TRACKING)

    cap = word_face.cap / word_face.upem * WORD_SIZE
    mark_h = 0.95 * cap
    mark_k = mark_h / (MARK_BOX[3] - MARK_BOX[1])
    mark_w = (MARK_BOX[2] - MARK_BOX[0]) * mark_k
    gap = MARK_TO_WORD * cap
    tag_cap = tag_face.cap / tag_face.upem * TAG_SIZE
    tag_gap = WORD_TO_TAG * cap

    # Centre the lockup — mark included — and the tagline under it, as one block.
    lockup_w = mark_w + gap + (word_r - word_l)
    lockup_x = (W - lockup_w) / 2
    block_h = cap + tag_gap + tag_cap
    # The tagline's descenders hang below the block, so lift it to look centred.
    top = (H - block_h) / 2 - cap * 0.02
    baseline = top + cap

    mark_x = lockup_x - MARK_BOX[0] * mark_k
    mark_y = baseline - cap / 2 - (MARK_BOX[1] + MARK_BOX[3]) / 2 * mark_k
    word_x = lockup_x + mark_w + gap - word_l
    tag_x = (W - (tag_r - tag_l)) / 2 - tag_l
    tag_y = baseline + tag_gap + tag_cap

    paths = "".join(f'\n    <path d="{d}"/>' for d in MARK_PATHS)
    label = f"Kiomon — {TAG[:1].lower()}{TAG[1:]}"  # the tagline, as a sentence
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{label}">
  <!-- Kiomon organisation profile banner. Generated by tools/build-banner.py; edit that,
       not this file. The wordmark and tagline are outlined — see the script's header. -->
  <title>Kiomon</title>
  <rect width="{W}" height="{H}" rx="{RADIUS}" fill="{ground}"/>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="{RADIUS - 0.5}" fill="none"
        stroke="{hairline}" stroke-width="1"/>
{field(variant)}
  <g transform="translate({num(mark_x)} {num(mark_y)}) scale({num(mark_k)})" fill="{mark}">{paths}
  </g>
  {placed(word, word_x, baseline, text)}
  {placed(tag, tag_x, tag_y, text, muted_opacity)}
</svg>
"""


def build_mark() -> str:
    x0, y0, x1, y1 = MARK_BOX
    pad = 2.0
    paths = "".join(f'\n  <path d="{d}"/>' for d in MARK_PATHS)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="{num(x0 - pad)} {num(y0 - pad)} {num(x1 - x0 + 2 * pad)} {num(y1 - y0 + 2 * pad)}" role="img" aria-label="Kiomon">
  <!-- The Kiomon mark on its own. Traced from public/logo-128x128.png in the landing
       bundle; generated by tools/build-banner.py. -->
  <title>Kiomon</title>
  <g fill="{RED}">{paths}
  </g>
</svg>
"""


def render_preview(files: dict[str, str], dest: Path) -> None:
    chrome = next(
        (
            p
            for p in (
                shutil.which("chrome"),
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            )
            if p and Path(p).exists()
        ),
        None,
    )
    if not chrome:
        print("no Chrome or Edge found — skipping previews", file=sys.stderr)
        return
    dest.mkdir(parents=True, exist_ok=True)
    for name, svg in files.items():
        width, height = (W, H) if name.startswith("banner") else (200, 170)
        page = dest / f"{name}.html"
        page.write_text(f'<body style="margin:0;line-height:0">{svg}</body>', encoding="utf-8")
        png = dest / name.replace(".svg", ".png")
        subprocess.run(
            [
                chrome,
                "--headless",
                "--disable-gpu",
                "--hide-scrollbars",
                "--force-device-scale-factor=1",
                f"--screenshot={png}",
                f"--window-size={width},{height}",
                page.resolve().as_uri(),
            ],
            check=True,
            capture_output=True,
        )
        print(png)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--out", default=str(ROOT / "profile" / "assets"))
    parser.add_argument("--preview", help="also write PNG previews here (needs Chrome or Edge)")
    args = parser.parse_args()

    word_face = Face(FONT_DIR / "BricolageGrotesque-SemiBold-var.ttf", 600)
    tag_face = Face(FONT_DIR / "Inter-Medium-var.ttf", 500)

    files = {
        "banner-light.svg": build("light", word_face, tag_face),
        "banner-dark.svg": build("dark", word_face, tag_face),
        "logo-mark.svg": build_mark(),
    }

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for name, svg in files.items():
        path = out / name
        path.write_text(svg, encoding="utf-8", newline="\n")
        print(f"{path}  ({path.stat().st_size / 1024:.1f} kB)")

    if args.preview:
        render_preview(files, Path(args.preview))


if __name__ == "__main__":
    main()
