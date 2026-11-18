"""Animated hero banner: wave-bobbing title, rising striped sun with a pulsing
glow, two parallax skylines scrolling past, a ground grid rolling toward the
viewer, twinkling stars and the odd shooting star."""
import math
import random

from pixel import PAL, INK, BASE_CSS, text, text_w, text_d, shadow_text, sprite, rect, bands, panel_path, svg
import sprites as S

W, H, HOR = 1600, 520, 420
LBL = 7  # px size of the CS + MATH / UC BERKELEY labels
k, w, y, o, p, m, b = (PAL[c] for c in 'kwyopmb')


def skyline(rnd, color, edge, hmin, hmax, win_p, seed_win):
    out, x = '', 0
    while x < W:
        bw = rnd.randrange(40, 130, 8)
        bh = rnd.randrange(hmin, hmax, 4)
        bw = min(bw, W - x)
        out += rect(x, HOR - bh, bw, bh, color) + rect(x, HOR - bh, bw, 4, edge)
        for wy in range(HOR - bh + 12, HOR - 8, 14):
            for wx in range(x + 8, x + bw - 8, 16):
                if rnd.random() < win_p:
                    cls = f' class="tw st{rnd.randrange(4)}"' if rnd.random() < .3 else ''
                    out += rect(wx, wy, 4, 6, y, cls)
        x += bw + rnd.choice([0, 0, 8])
    return out


def hero():
    rnd = random.Random(3)
    css, s, defs = BASE_CSS, '', ''

    s += bands(0, 0, W, HOR, ['#0d0c1c', '#100e24', '#14102c', '#1a1236', '#221540', '#2d184c', '#3b1b58'])

    # stars
    for i in range(80):
        sx, sy = rnd.randrange(20, W - 20, 4), rnd.randrange(60, HOR - 140, 4)
        if 440 < sx < 1160 and 70 < sy < 280:
            continue
        sz = rnd.choice([4, 4, 4, 8])
        s += rect(sx, sy, sz, sz, rnd.choice([w, w, PAL['s'], b]), f' class="tw st{i % 4}"')
    css += ''.join(f".st{i}{{animation-delay:{-i * .6:.1f}s}}" for i in range(4))

    # shooting stars
    for n, (x0, y0, dl) in enumerate([(1180, 70, 0), (300, 90, 4.5)]):
        streak = ''.join(rect(x0 - i * 12, y0 - i * 6, 12, 4, w, f' opacity="{1 - i / 8:.2f}"') for i in range(8))
        s += f'<g class="ss ss{n}">{streak}</g>'
        css += (f".ss{n}{{opacity:0;animation:ss{n} 9s ease-in infinite;animation-delay:{dl}s}}"
                f"@keyframes ss{n}{{0%,86%{{opacity:0;transform:translate(0,0)}}87%{{opacity:1}}"
                f"96%{{opacity:1;transform:translate(260px,130px)}}97%,100%{{opacity:0;transform:translate(260px,130px)}}}}")

    # sun: glow + striped disc, slowly rising and sinking behind the city
    cx, R, px = W // 2, 140, 10
    glow = ''
    for i, (rr, op) in enumerate([(230, .10), (196, .14), (168, .2)]):
        for yy in range(HOR - rr, HOR, px):
            dy = HOR - (yy + px / 2)
            half = int(math.sqrt(max(rr * rr - dy * dy, 0)) / px) * px
            glow += rect(cx - half, yy, 2 * half, px, p, f' opacity="{op}"')
    sun_cols = ['#ffe27a', '#ffc23d', '#ffa23d', '#ff7a52', '#ff5a78', '#ff4f8b']
    disc = ''
    n = R // px
    for i in range(n):
        yy = HOR - R + i * px
        dy = HOR - (yy + px / 2)
        half = int(math.sqrt(max(R * R - dy * dy, 0)) / px) * px
        disc += rect(cx - half, yy, 2 * half, px, sun_cols[min(i * len(sun_cols) // n, 5)])
    bars = ''.join(rect(cx - R - 10, HOR - R + 60 + j * 22, 2 * R + 20, 8, '#000') for j in range(-2, 7))
    defs += (f'<clipPath id="above"><rect x="0" y="0" width="{W}" height="{HOR}"/></clipPath>'
             f'<clipPath id="lower"><rect x="0" y="{HOR - R + 66}" width="{W}" height="{R}"/></clipPath>'
             f'<mask id="stripes" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
             f'<rect x="0" y="0" width="{W}" height="{H}" fill="#fff"/>'
             f'<g clip-path="url(#lower)"><g class="bars">{bars}</g></g></mask>')
    s += (f'<g clip-path="url(#above)"><g class="glow">{glow}</g>'
          f'<g class="sun"><g mask="url(#stripes)">{disc}</g></g></g>')
    css += (".sun{animation:sun 10s ease-in-out infinite}"
            "@keyframes sun{0%,100%{transform:translateY(60px)}50%{transform:translateY(-36px)}}"
            ".bars{animation:bars 1.4s linear infinite}"
            "@keyframes bars{0%{transform:translateY(0)}100%{transform:translateY(22px)}}"
            ".glow{animation:glow 10s ease-in-out infinite}"
            "@keyframes glow{0%,100%{opacity:.5;transform:translateY(56px)}50%{opacity:1;transform:translateY(-30px)}}")

    # parallax skylines (each tile drawn twice for a seamless loop)
    far = skyline(random.Random(8), '#1e1640', '#2f2358', 24, 72, .08, 0)
    near = skyline(random.Random(5), '#120f26', '#2a1f4a', 12, 48, .22, 1)
    s += f'<g class="far">{far}<g transform="translate({W} 0)">{far}</g></g>'
    s += f'<g class="near">{near}<g transform="translate({W} 0)">{near}</g></g>'
    css += (f".far{{animation:far 60s linear infinite}}@keyframes far{{100%{{transform:translateX(-{W}px)}}}}"
            f".near{{animation:near 26s linear infinite}}@keyframes near{{100%{{transform:translateX(-{W}px)}}}}")

    # ground grid rolling toward the viewer
    s += rect(0, HOR, W, H - HOR, '#0b0a16') + rect(0, HOR, W, 4, p)
    for kk in range(-10, 11):
        s += (f'<line x1="{cx + kk * 30}" y1="{HOR}" x2="{cx + kk * 200}" y2="{H}" '
              f'stroke="{p}" stroke-opacity=".45" stroke-width="3"/>')
    NL, PER = 7, 2.8
    for i in range(NL):
        s += f'<g class="gl gl{i}">{rect(0, HOR, W, 4, p)}</g>'
    css += (f".gl{{opacity:0;animation:gl {PER}s cubic-bezier(.5,0,1,.6) infinite}}"
            f"@keyframes gl{{0%{{transform:translateY(0);opacity:.15}}100%{{transform:translateY({H - HOR}px);opacity:.85}}}}")
    css += ''.join(f".gl{i}{{animation-delay:{-i * PER / NL:.2f}s}}" for i in range(NL))

    # title: each letter bobs on a wave, with its own outline, extrusion and shine
    title, tpx = 'SMARAN', 18
    tw = text_w(title, tpx)
    tx, ty = round((W - tw) / 2 / 2) * 2, 104
    defs += ('<linearGradient id="tg" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{w}"/><stop offset=".4286" stop-color="{w}"/>'
             f'<stop offset=".4286" stop-color="{y}"/><stop offset=".7143" stop-color="{y}"/>'
             f'<stop offset=".7143" stop-color="{o}"/><stop offset="1" stop-color="{o}"/></linearGradient>')
    x = tx
    for li, ch in enumerate(title):
        d = text_d(ch, x, ty, tpx)
        dsh = text_d(ch, x + 8, ty + 8, tpx)
        outline = ''.join(f'<path fill="{INK}" transform="translate({dx} {dy})" d="{d}"/>'
                          for dx in (-6, 0, 6) for dy in (-6, 0, 6, 14))
        defs += f'<clipPath id="lc{li}"><path d="{d}"/></clipPath>'
        s += (f'<g class="lt lt{li}">{outline}<path fill="#7a3ff0" d="{dsh}"/><path fill="url(#tg)" d="{d}"/>'
              f'<g clip-path="url(#lc{li})"><rect class="shine" x="-200" y="{ty - 20}" width="70" height="200" '
              f'fill="#ffffff" opacity=".55" transform="skewX(-20)"/></g></g>')
        x += text_w(ch, tpx) + tpx
    css += (".lt{animation:lt 2.4s ease-in-out infinite}"
            "@keyframes lt{0%,100%{transform:translateY(6px)}50%{transform:translateY(-16px)}}"
            ".shine{animation:shine 4.5s linear infinite}"
            "@keyframes shine{0%{transform:skewX(-20deg) translateX(0)}45%,100%{transform:skewX(-20deg) translateX(2000px)}}")
    css += ''.join(f".lt{i}{{animation-delay:{-i * .16:.2f}s}}" for i in range(len(title)))

    # HUD corners
    s += shadow_text('CS + MATH', cx - 300, 282, LBL, y, INK, off=(0, LBL), anchor='end')
    s += shadow_text('UC BERKELEY', cx + 250, 282, LBL, y, INK, off=(0, LBL))

    clip = panel_path(8, 8, W - 16, H - 16, 8)
    defs = f'<clipPath id="c"><path d="{clip}"/></clipPath>' + defs
    body = (f'<path fill="{INK}" d="{panel_path(0, 0, W, H, 8)}"/>'
            f'<g clip-path="url(#c)">{s}</g>'
            f'<path fill="none" stroke="#3a3366" stroke-width="4" d="{panel_path(10, 10, W - 20, H - 20, 8)}"/>')
    return svg(W, H, body, css, defs, 'Smaran')


def hero_narrow(width=1400):
    """Same banner, narrower, for the layout with a social-button rail beside it."""
    global W, LBL
    old = (W, LBL)
    W, LBL = width, 6
    try:
        return hero()
    finally:
        W, LBL = old
