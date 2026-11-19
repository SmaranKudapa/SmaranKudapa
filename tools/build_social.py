#!/usr/bin/env python3
"""Social buttons for the README as animated SVGs (light sweep included).

Each logo image in tools/logos/ (supplied by Smaran) is pixel art, so it is read
back onto its own pixel grid and redrawn as vector squares inside the button frame.
Transparent space above/below each square spaces the buttons when they stack.

    python3 tools/build_social.py
"""
import os
from PIL import Image
from pixel import INK, BASE_CSS, rect, panel_path, svg

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, '..', 'assets'))
S, GAP = 256, 6                       # square size; GAP split above/below
LOGO = {   # key: (cell px in the source image, colours, width fraction, label, strip colour, link)
    'linkedin': (28, [(39, 101, 160), (229, 229, 229)], .56, 'LinkedIn', '#2f6db5'),
    'youtube': (28, [(228, 30, 47), (229, 229, 229)], .64, 'YouTube', '#e8253a'),
    'x': (14, [(255, 255, 255)], .54, 'X', '#f3efff'),
}


def grid(key):
    cell, pal, *_ = LOGO[key]
    im = Image.open(os.path.join(HERE, 'logos', f'logo-{key}.png')).convert('RGBA')
    w, h = im.size
    cols, rows = round(w / cell), round(h / cell)
    cw, ch = w / cols, h / rows
    px = im.load()
    g = []
    for r in range(rows):
        line = []
        for c in range(cols):
            x, y = int((c + .5) * cw), int((r + .5) * ch)
            R, G, B, A = px[x, y]
            if A < 128 or (key == 'x' and R < 160):
                line.append(None)
            else:
                line.append(min(range(len(pal)), key=lambda i: sum((a - b) ** 2 for a, b in zip((R, G, B), pal[i]))))
        g.append(line)
    return g, pal


def social_svg(key):
    cell, pal0, frac, label, strip = LOGO[key]
    c = 8
    body = f'<path fill="{INK}" d="{panel_path(0, 0, S, S, c)}"/>'
    defs = f'<clipPath id="bc"><path d="{panel_path(c, c, S - 2 * c, S - 2 * c, c)}"/></clipPath>'
    body += f'<g clip-path="url(#bc)">{rect(0, 0, S, S, "#16142a")}{rect(0, S - 22, S, 14, strip)}</g>'
    body += f'<path fill="none" stroke="#3a3366" stroke-width="4" d="{panel_path(c + 2, c + 2, S - 2 * c - 4, S - 2 * c - 4, c)}"/>'
    g, pal = grid(key)
    rows, cols = len(g), len(g[0])
    u = S * frac / cols                                   # vector size of one logo pixel
    x0, y0 = (S - cols * u) / 2, S * .46 - rows * u / 2
    paths = {}
    for r, line in enumerate(g):
        c0 = 0
        while c0 < cols:
            v = line[c0]
            c1 = c0
            while c1 < cols and line[c1] == v:
                c1 += 1
            if v is not None:
                paths.setdefault(v, []).append(
                    f'M{x0 + c0 * u:.2f} {y0 + r * u:.2f}h{(c1 - c0) * u:.2f}v{u:.2f}h{-(c1 - c0) * u:.2f}z')
            c0 = c1
    for v, ds in paths.items():
        body += f'<path fill="#{"%02x%02x%02x" % pal[v]}" d="{"".join(ds)}"/>'
    # light sweep passes over the logo too
    body += (f'<g clip-path="url(#bc)"><rect class="shine" x="-140" y="0" width="50" height="{S}" '
             f'fill="#ffffff" opacity=".16" transform="skewX(-20)"/></g>')
    css = BASE_CSS + (".shine{animation:shine 4s linear infinite}"
                      "@keyframes shine{0%{transform:skewX(-20deg) translateX(0)}45%,100%{transform:skewX(-20deg) translateX(560px)}}")
    doc = svg(S, S + GAP, f'<g transform="translate(0 {GAP // 2})">{body}</g>', css, defs, label)
    return doc


def main():
    for key in LOGO:
        p = os.path.join(OUT, f'btn-social-{key}.svg')
        with open(p, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(social_svg(key))
        print(os.path.basename(p), os.path.getsize(p) // 1024, 'KB')


if __name__ == '__main__':
    main()
