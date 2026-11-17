"""Trial assets: narrower hero + three square social buttons (generic pixel icons)."""
import os
from pixel import PAL, INK, CREAM, BASE_CSS, text, text_w, sprite, sprite_size, rect, panel_path, svg
from hero2 import hero_narrow

OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets'))

BRIEFCASE = [".....kkkk.....", "....kbbbbk....", "....kb..bk....", "kkkkkkkkkkkkkk", "kbbbbbbbbbbbbk",
             "kbbbbbbbbbbbbk", "kbbbbbkkbbbbbk", "kkkkkkwwkkkkkk", "kbbbbbkkbbbbbk", "kbbbbbbbbbbbbk",
             "kbbbbbbbbbbbbk", "kkkkkkkkkkkkkk"]
TV = ["...k......k...", "....k....k....", ".....k..k.....", "kkkkkkkkkkkkkk", "krrrrrrrrrrrrk",
      "krddddddddddrk", "krdddwddddddrk", "krdddwwwddddrk", "krdddwwwwwddrk", "krdddwwwddddrk",
      "krdddwddddddrk", "krddddddddddrk", "krrrrrrrrrrrrk", "kkkkkkkkkkkkkk", ".kk........kk."]
BUBBLE = [".kkkkkkkkkkkk.", "kwwwwwwwwwwwwk", "kwkkkkkkkwwwwk", "kwwwwwwwwwwwwk", "kwkkkkkkkkkkwk",
          "kwwwwwwwwwwwwk", "kwkkkkkwwwwwwk", "kwwwwwwwwwwwwk", ".kkkkwwkkkkkk.", "....kwk.......",
          "....kk........"]

SOCIAL = [  # key, label, icon, palette, accent for label/shine edge
    ('linkedin', 'LINKEDIN', BRIEFCASE, {'b': PAL['b']}, PAL['b']),
    ('youtube', 'YOUTUBE', TV, {'r': '#ff3d5a', 'd': '#1b1930'}, '#ff3d5a'),
    ('x', 'X', BUBBLE, {}, CREAM),
]


FRAME_ACCENT = {'linkedin': '#2f6db5', 'youtube': '#e8253a', 'x': '#f3efff'}


def social_button(label, icon, pal, accent):
    S, c = 256, 8
    s, css = '', BASE_CSS
    s += f'<path fill="{INK}" d="{panel_path(0, 0, S, S, c)}"/>'
    inner = panel_path(c, c, S - 2 * c, S - 2 * c, c)
    defs = f'<clipPath id="bc"><path d="{inner}"/></clipPath>'
    s += (f'<g clip-path="url(#bc)">{rect(0, 0, S, S, "#16142a")}{rect(0, S - 22, S, 14, accent)}'
          f'<rect class="shine" x="-140" y="0" width="50" height="{S}" fill="#ffffff" opacity=".12" transform="skewX(-20)"/></g>')
    s += f'<path fill="none" stroke="#3a3366" stroke-width="4" d="{panel_path(c + 2, c + 2, S - 2 * c - 4, S - 2 * c - 4, c)}"/>'
    if icon:   # icon=None gives an empty frame for a supplied logo image
        px = 11
        iw, ih = sprite_size(icon, px)
        s += f'<g class="bob">{sprite(icon, (S - iw) // 2, (S - 14 - ih) // 2, px, pal)}</g>'
    css += (f".shine{{animation:shine 4s linear infinite}}"
            f"@keyframes shine{{0%{{transform:skewX(-20deg) translateX(0)}}45%,100%{{transform:skewX(-20deg) translateX(560px)}}}}")
    return svg(S, S, s, css, defs, label.title())


def main():
    files = {'hero-narrow.svg': hero_narrow(1400)}
    for key, label, icon, pal, acc in SOCIAL:
        files[f'btn-social-{key}.svg'] = social_button(label, icon, pal, acc)
        files[f'btn-social-frame-{key}.svg'] = social_button(label, None, pal, FRAME_ACCENT.get(key, acc))
    for n, d in files.items():
        with open(os.path.join(OUT, n), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(d)
        print(n, len(d) // 1024, 'KB')


if __name__ == '__main__':
    main()
