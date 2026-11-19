"""Link-button iterations (demo / video / article) for the project tiles.

Option A, split bar: the bar under a tile divides evenly into 1-3 bright buttons.
Option B, chips: every link is the same small dark chip with a type icon.
"""
import os
from pixel import PAL, INK, CREAM, BASE_CSS, text, text_w, sprite, sprite_size, rect, panel_path, svg

OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets'))

CURSOR = ["k.......", "kk......", "kwk.....", "kwwk....", "kwwwk...", "kwwwwk..", "kwwwwwk.", "kwwwwwwk",
          "kwwwkkkk", "kwkkwk..", "kk..kwk.", "k....kk."]
CLAPPER = ["kkkkkkkkkkkk", "kwwkkwwkkwwk", "kkkkkkkkkkkk", "kwwwwwwwwwwk", "kwwwwwwwwwwk", "kwwwkwwwwwwk",
           "kwwwkkwwwwwk", "kwwwkwwwwwwk", "kwwwwwwwwwwk", "kkkkkkkkkkkk"]
PAGE = ["kkkkkkk...", "kwwwwwkk..", "kwwwwwkwk.", "kwkkkwkkkk", "kwwwwwwwwk", "kwkkkkkkwk", "kwwwwwwwwk",
        "kwkkkkkkwk", "kwwwwwwwwk", "kwkkkkwwwk", "kwwwwwwwwk", "kkkkkkkkkk"]
SCROLL = [".kkkkkkkkkk.", "kwwwwwwwwwwk", ".kkkkkkkkkk.", "..kwwwwwwk..", "..kwkkkkwk..", "..kwwwwwwk..",
          "..kwkkkkwk..", "..kwwwwwwk..", "..kwkkwwwk..", ".kkkkkkkkkk.", "kwwwwwwwwwwk", ".kkkkkkkkkk."]
ICON = {'demo': CURSOR, 'video': CLAPPER, 'article': PAGE}          # Option B chips
SEG_ICON = {'demo': CURSOR, 'video': CLAPPER, 'article': SCROLL}    # Option A split bar

ACCENT = {'rubish': PAL['y'], 'town-trial': PAL['m'], 'picky': PAL['p'], 'claimos': PAL['b'],
          'multivis': PAL['v'], 'tempest': PAL['o']}
LINKS = {  # key -> ordered link types the project has
    'rubish': ['demo'], 'town-trial': ['demo', 'video', 'article'], 'picky': ['demo', 'video'],
    'claimos': ['demo', 'video'], 'multivis': ['demo'], 'tempest': [],
}


def mix(h, t, to=(255, 255, 255)):
    c = [int(h[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{round(a + (b - a) * t):02x}' for a, b in zip(c, to))


def _frame(W, H, fill, c=6):
    s = f'<path fill="{INK}" d="{panel_path(0, 0, W, H, c)}"/>'
    defs = f'<clipPath id="bc"><path d="{panel_path(6, 6, W - 12, H - 12, c)}"/></clipPath>'
    return s, defs


def segment(kind, accent, W):
    """Option A: bright split-bar button. W = 800 (one link), 392 (two), 259 (three)."""
    H = 112
    fill, ink, iw_col = {
        'demo': (accent, INK, CREAM),
        'video': (mix(accent, .55, (11, 10, 20)), CREAM, mix(accent, .3)),
        'article': (CREAM, INK, '#c8c4e4'),
    }[kind]
    label = {'demo': 'DEMO', 'video': 'VIDEO', 'article': 'BLOG'}[kind]
    tpx = 5   # one label size for every split, so VIDEO fits in thirds
    s, defs = _frame(W, H, fill)
    s += (f'<g clip-path="url(#bc)">{rect(0, 0, W, H, fill)}{rect(0, 6, W, 8, mix(fill, .4))}'
          f'{rect(0, H - 18, W, 12, mix(fill, .3, (11, 10, 20)))}'
          f'<rect class="shine" x="-120" y="0" width="60" height="{H}" fill="#ffffff" opacity=".28" transform="skewX(-20)"/></g>')
    icon, ipx = SEG_ICON[kind], 5
    iw, ih = sprite_size(icon, ipx)
    lw = text_w(label, tpx)
    x0 = (W - iw - 14 - lw) / 2
    s += f'<g class="nudge">{sprite(icon, round(x0), (H - 6 - ih) // 2, ipx, {"k": INK, "w": iw_col})}</g>'
    s += text(label, x0 + iw + 14, (H - 6 - 7 * tpx) // 2, tpx, ink)
    css = BASE_CSS + (f".shine{{animation:shine 3.6s linear infinite}}"
                      f"@keyframes shine{{0%{{transform:skewX(-20deg) translateX(0)}}50%,100%{{transform:skewX(-20deg) translateX({W + 300}px)}}}}"
                      ".nudge{animation:nudge 1.2s ease-in-out infinite}"
                      "@keyframes nudge{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}")
    return svg(W, H, s, css, defs, label.title())


def chip(kind, accent):
    """Option B: same-size dark chip, type icon + label, colour strip by type."""
    W, H, c = 256, 104, 6
    col = {'demo': accent, 'video': '#ff3d5a', 'article': CREAM}[kind]
    label = {'demo': 'DEMO', 'video': 'VIDEO', 'article': 'READ'}[kind]
    s, defs = _frame(W, H, '#16142a')
    s += (f'<g clip-path="url(#bc)">{rect(0, 0, W, H, "#16142a")}{rect(0, H - 20, W, 14, col)}'
          f'<rect class="shine" x="-120" y="0" width="40" height="{H}" fill="#ffffff" opacity=".1" transform="skewX(-20)"/></g>')
    s += f'<path fill="none" stroke="#3a3366" stroke-width="4" d="{panel_path(c + 2, c + 2, W - 2 * c - 4, H - 2 * c - 4, c)}"/>'
    icon, ipx, tpx = ICON[kind], 5, 5
    iw, ih = sprite_size(icon, ipx)
    lw = text_w(label, tpx)
    x0 = (W - iw - 10 - lw) / 2
    s += f'<g class="bob">{sprite(icon, round(x0), (H - 20 - ih) // 2 + 2, ipx, {"k": "#0b0a14", "w": col})}</g>'
    s += text(label, x0 + iw + 10, (H - 20 - 7 * tpx) // 2 + 2, tpx, CREAM)
    css = BASE_CSS + (".shine{animation:shine 4.5s linear infinite}"
                      "@keyframes shine{0%{transform:skewX(-20deg) translateX(0)}45%,100%{transform:skewX(-20deg) translateX(560px)}}")
    return svg(W, H, s, css, defs, label.title())


def main():
    files = {}
    widths = {1: 800, 2: 392, 3: 259}
    for key, kinds in LINKS.items():
        n = len(kinds)
        for kind in kinds:
            files[f'seg-{kind}-{key}.svg'] = segment(kind, ACCENT[key], widths[n])
            files[f'chip-{kind}-{key}.svg'] = chip(kind, ACCENT[key])
    os.makedirs(os.path.join(OUT, 'iter'), exist_ok=True)
    for n, d in files.items():
        with open(os.path.join(OUT, 'iter', n), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(d)
    print(len(files), 'files')


if __name__ == '__main__':
    main()
