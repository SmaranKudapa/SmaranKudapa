"""Shared pixel-art toolkit: palette, 5x7 bitmap font, sprite + SVG helpers.

Every visual on the profile is built from these pieces so the whole page
shares one palette, one typeface and one pixel grid.
"""
import math
from xml.sax.saxutils import escape

# ── Palette ──────────────────────────────────────────────────────────────
PAL = {
    'k': '#0b0a14',  # ink / outline
    'K': '#16142a',  # panel
    'd': '#2a2650',  # dark violet
    'G': '#4a4670',  # slate
    'g': '#8a86a8',  # lavender grey
    's': '#c8c4e4',  # pale lavender
    'w': '#fff4e0',  # cream
    't': '#e8c9a0',  # tan
    'y': '#ffc23d',  # amber
    'o': '#ff8a3d',  # orange
    'p': '#ff4f8b',  # hot pink
    'r': '#e83b5a',  # red
    'm': '#3ee6a8',  # mint
    'b': '#4fb3ff',  # sky
    'v': '#9b6bff',  # violet
}
INK, CREAM = PAL['k'], PAL['w']

THEMES = {
    # colours for assets on a transparent background (picture light/dark)
    'dark':  {'accent': '#ffc23d', 'text': '#f3efff', 'dim': '#8b88a8', 'line': '#30363d', 'shadow': '#000000'},
    'light': {'accent': '#9a5b00', 'text': '#1b1930', 'dim': '#6e6a8a', 'line': '#d0d7de', 'shadow': '#dcd6f2'},
}

# ── 5x7 bitmap font ──────────────────────────────────────────────────────
_F = {
    'A': ".###. #...# #...# ##### #...# #...# #...#",
    'B': "####. #...# #...# ####. #...# #...# ####.",
    'C': ".###. #...# #.... #.... #.... #...# .###.",
    'D': "####. #...# #...# #...# #...# #...# ####.",
    'E': "##### #.... #.... ####. #.... #.... #####",
    'F': "##### #.... #.... ####. #.... #.... #....",
    'G': ".###. #...# #.... #.### #...# #...# .####",
    'H': "#...# #...# #...# ##### #...# #...# #...#",
    'I': ".###. ..#.. ..#.. ..#.. ..#.. ..#.. .###.",
    'J': "..### ...#. ...#. ...#. ...#. #..#. .##..",
    'K': "#...# #..#. #.#.. ##... #.#.. #..#. #...#",
    'L': "#.... #.... #.... #.... #.... #.... #####",
    'M': "#...# ##.## #.#.# #.#.# #...# #...# #...#",
    'N': "#...# #...# ##..# #.#.# #..## #...# #...#",
    'O': ".###. #...# #...# #...# #...# #...# .###.",
    'P': "####. #...# #...# ####. #.... #.... #....",
    'Q': ".###. #...# #...# #...# #.#.# #..#. .##.#",
    'R': "####. #...# #...# ####. #.#.. #..#. #...#",
    'S': ".#### #.... #.... .###. ....# ....# ####.",
    'T': "##### ..#.. ..#.. ..#.. ..#.. ..#.. ..#..",
    'U': "#...# #...# #...# #...# #...# #...# .###.",
    'V': "#...# #...# #...# #...# #...# .#.#. ..#..",
    'W': "#...# #...# #...# #.#.# #.#.# #.#.# .#.#.",
    'X': "#...# #...# .#.#. ..#.. .#.#. #...# #...#",
    'Y': "#...# #...# .#.#. ..#.. ..#.. ..#.. ..#..",
    'Z': "##### ....# ...#. ..#.. .#... #.... #####",
    '0': ".###. #...# #..## #.#.# ##..# #...# .###.",
    '1': "..#.. .##.. ..#.. ..#.. ..#.. ..#.. .###.",
    '2': ".###. #...# ....# ...#. ..#.. .#... #####",
    '3': "####. ....# ....# .###. ....# ....# ####.",
    '4': "...#. ..##. .#.#. #..#. ##### ...#. ...#.",
    '5': "##### #.... ####. ....# ....# #...# .###.",
    '6': ".###. #.... #.... ####. #...# #...# .###.",
    '7': "##### ....# ...#. ..#.. .#... .#... .#...",
    '8': ".###. #...# #...# .###. #...# #...# .###.",
    '9': ".###. #...# #...# .#### ....# ....# .###.",
    ' ': "... ... ... ... ... ... ...",
    '.': ". . . . . . #",
    ',': ".. .. .. .. .. .# #.",
    '·': ". . . # . . .",
    ':': ". . # . . # .",
    '!': "# # # # # . #",
    "'": "# # . . . . .",
    '-': ".... .... .... #### .... .... ....",
    '+': "..... ..#.. ..#.. ##### ..#.. ..#.. .....",
    '&': ".##.. #..#. #.#.. .#... #.#.# #..#. .##.#",
    '@': ".###. #...# #.### #.#.# #.### #.... .###.",
    '?': ".###. #...# ....# ...#. ..#.. ..... ..#..",
    '/': "....# ....# ...#. ..#.. .#... #.... #....",
    '°': ".#. #.# .#. ... ... ... ...",
    '>': "#... .#.. ..#. ...# ..#. .#.. #...",
    '<': "...# ..#. .#.. #... .#.. ..#. ...#",
    '▶': "#... ##.. ###. #### ###. ##.. #...",
    '◀': "...# ..## .### #### .### ..## ...#",
    '♥': "..... .#.#. ##### ##### .###. ..#.. .....",
    '_': "..... ..... ..... ..... ..... ..... #####",
    '$': "..#.. .#### #.#.. .###. ..#.# ####. ..#..",
    '(': ".# #. #. #. #. #. .#",
    ')': "#. .# .# .# .# .# #.",
    '=': "..... ..... ##### ..... ##### ..... .....",
    '^': "..#.. .#.#. #...# ..... ..... ..... .....",
    '²': "##. ..# .#. ### ... ... ...",
}
FONT = {ch: s.split() for ch, s in _F.items()}


def glyph(ch):
    return FONT.get(ch, FONT['?'])


def text_w(s, px, sp=1):
    s = s.upper()
    return (sum(len(glyph(c)[0]) + sp for c in s) - sp) * px


def _runs(row, on):
    i = 0
    while i < len(row):
        if row[i] in on:
            j = i
            while j < len(row) and row[j] == row[i]:
                j += 1
            yield i, j, row[i]
            i = j
        else:
            i += 1


def rect_d(x, y, w, h):
    return f"M{x:g} {y:g}h{w:g}v{h:g}h{-w:g}z"


def text_d(s, x, y, px, sp=1):
    """Path data for pixel text with top-left at (x, y)."""
    out, cx = [], round(x)
    for ch in s.upper():
        rows = glyph(ch)
        for ri, row in enumerate(rows):
            for a, b, _ in _runs(row, '#'):
                out.append(rect_d(cx + a * px, y + ri * px, (b - a) * px, px))
        cx += (len(rows[0]) + sp) * px
    return ''.join(out)


def text(s, x, y, px, fill, sp=1, cls='', anchor='start', extra=''):
    if anchor == 'middle':
        x = x - text_w(s, px, sp) / 2
    elif anchor == 'end':
        x = x - text_w(s, px, sp)
    c = f' class="{cls}"' if cls else ''
    return f'<path{c} fill="{fill}" d="{text_d(s, x, y, px, sp)}"{extra}/>'


def shadow_text(s, x, y, px, fill, shadow, off=(0, None), sp=1, anchor='start', cls=''):
    dx, dy = off
    dy = px if dy is None else dy
    return (text(s, x + dx, y + dy, px, shadow, sp, anchor=anchor) +
            text(s, x, y, px, fill, sp, cls=cls, anchor=anchor))


# ── sprites ──────────────────────────────────────────────────────────────
def sprite(rows, x, y, px, pal=None):
    """rows: list of equal-length strings; '.' is transparent; other chars map to colours."""
    p = dict(PAL)
    if pal:
        p.update(pal)
    w = len(rows[0])
    assert all(len(r) == w for r in rows), f"ragged sprite: {[len(r) for r in rows]}"
    by = {}
    for ri, row in enumerate(rows):
        for a, b, c in _runs(row, set(row) - {'.'}):
            by.setdefault(c, []).append(rect_d(x + a * px, y + ri * px, (b - a) * px, px))
    return ''.join(f'<path fill="{p[c]}" d="{"".join(v)}"/>' for c, v in by.items())


def sprite_size(rows, px):
    return len(rows[0]) * px, len(rows) * px


# ── shapes ───────────────────────────────────────────────────────────────
def panel_path(x, y, w, h, c):
    """Rectangle with stepped (pixel) corners, step size c."""
    return (f"M{x+2*c} {y}h{w-4*c}v{c}h{c}v{c}h{c}v{h-4*c}h{-c}v{c}h{-c}v{c}"
            f"h{-(w-4*c)}v{-c}h{-c}v{-c}h{-c}v{-(h-4*c)}h{c}v{-c}h{c}z")


def poly(pts, fill, extra=''):
    return f'<polygon fill="{fill}" points="{" ".join(f"{x:g},{y:g}" for x, y in pts)}"{extra}/>'


def rect(x, y, w, h, fill, extra=''):
    return f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" fill="{fill}"{extra}/>'


def bands(x, y, w, h, colors):
    """Hard-edged vertical colour bands (retro sky)."""
    n = len(colors)
    out = []
    for i, c in enumerate(colors):
        y0 = y + round(h * i / n)
        y1 = y + round(h * (i + 1) / n)
        out.append(rect(x, y0, w, y1 - y0, c))
    return ''.join(out)


def iso_cube(x, y, tw, th, h, top, left, right, inset=0.78):
    """Isometric box standing on the diamond whose top vertex is (x, y)."""
    cx, cy = x, y + th
    T = (cx, cy - th * inset)
    R = (cx + tw * inset, cy)
    B = (cx, cy + th * inset)
    L = (cx - tw * inset, cy)
    up = lambda p: (p[0], p[1] - h)
    return (poly([up(L), up(B), B, L], left) + poly([up(B), up(R), R, B], right) +
            poly([up(T), up(R), up(B), up(L)], top)), (L, B, R, T)


# ── svg document + animation helpers ─────────────────────────────────────
def svg(w, h, body, css='', defs='', title=''):
    t = f'<title>{escape(title)}</title>' if title else ''
    st = f'<style>{css}</style>' if css else ''
    df = f'<defs>{defs}</defs>' if defs else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" shape-rendering="crispEdges">{t}{st}{df}{body}</svg>')


BASE_CSS = (
    ".blink{animation:blink 1.1s steps(1) infinite}"
    "@keyframes blink{50%{opacity:0}}"
    ".bob{animation:bob 1.4s ease-in-out infinite}"
    "@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}"
    ".bob2{animation:bob 1.4s ease-in-out infinite;animation-delay:-.7s}"
    ".tw{animation:tw 2.4s steps(1) infinite}"
    "@keyframes tw{0%,100%{opacity:1}40%{opacity:.25}70%{opacity:.7}}"
)


def frames_css(cls, n, T):
    """Frame-by-frame flipbook: elements .{cls} .{cls}{i} show one at a time."""
    pct = 100 / n
    css = (f".{cls}{{opacity:0;animation:{cls}k {T}s steps(1) infinite}}"
           f"@keyframes {cls}k{{0%{{opacity:1}}{pct:.3f}%{{opacity:0}}100%{{opacity:0}}}}")
    css += ''.join(f".{cls}{i}{{animation-delay:{i * T / n:.3f}s}}" for i in range(n))
    return css


def delay(cls_base, i, step):
    return f".{cls_base}{i}{{animation-delay:{-i * step:.2f}s}}"
