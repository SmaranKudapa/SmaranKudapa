#!/usr/bin/env python3
"""Build every image for the SmaranKudapa profile README.

    python3 tools/build_assets.py          # writes ./assets/*.svg

Change labels in TILES / AWARDS below and re-run. All assets are animated
SVGs (internal CSS only, no JS, no external fonts), so GitHub renders them
through <img>.
"""
import math
import os
import random

from pixel import (PAL, INK, CREAM, THEMES, BASE_CSS, text, text_w, shadow_text, sprite,
                   sprite_size, panel_path, poly, rect, bands, iso_cube, svg, frames_css, rect_d)
import sprites as S

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, '..', 'assets'))

k, w, y, o, p, m, b, v, r = (PAL[c] for c in 'kwyopmbvr')


def frame_panel(W, H, inner, css, defs='', title='', border=8, edge='#3a3366'):
    """Dark self-contained card (reads on both GitHub themes)."""
    clip = panel_path(border, border, W - 2 * border, H - 2 * border, border)
    defs = f'<clipPath id="c"><path d="{clip}"/></clipPath>' + defs
    body = (f'<path fill="{INK}" d="{panel_path(0, 0, W, H, border)}"/>'
            f'<g clip-path="url(#c)">{inner}</g>'
            f'<path fill="none" stroke="{edge}" stroke-width="4" d="{panel_path(border + 2, border + 2, W - 2 * border - 4, H - 2 * border - 4, border)}"/>')
    return svg(W, H, body, BASE_CSS + css, defs, title)


# ═════════════════════════════════════════════════════════════════════════
# HERO
# ═════════════════════════════════════════════════════════════════════════
def hero():
    W, H, HOR = 1600, 520, 420
    rnd = random.Random(3)
    css, s, defs = '', '', ''

    s += bands(0, 0, W, HOR, ['#0d0c1c', '#100e24', '#14102c', '#1a1236', '#221540', '#2d184c', '#3b1b58'])

    # stars
    for i in range(70):
        sx, sy = rnd.randrange(20, W - 20, 4), rnd.randrange(20, HOR - 120, 4)
        if 420 < sx < 1180 and 40 < sy < 300:  # keep the title area clean
            continue
        sz = rnd.choice([4, 4, 4, 8])
        col = rnd.choice([w, w, PAL['s'], b])
        s += rect(sx, sy, sz, sz, col, f' class="tw st{i % 4}"')
    css += ''.join(f".st{i}{{animation-delay:{-i * .6:.1f}s}}" for i in range(4))

    # synthwave sun
    cx, R, px = 800, 130, 10
    sun_cols = ['#ffe27a', '#ffc23d', '#ffa23d', '#ff7a52', '#ff5a78', '#ff4f8b']
    gaps = {9, 10, 11, 12, 13, 14}
    n = R // px
    for i in range(n):
        yy = HOR - R + i * px
        if i in {7, 9, 11, 12}:
            continue
        dy = HOR - (yy + px / 2)
        half = int(math.sqrt(max(R * R - dy * dy, 0)) / px) * px
        col = sun_cols[min(i * len(sun_cols) // n, len(sun_cols) - 1)]
        s += rect(cx - half, yy, 2 * half, px, col)

    # skyline
    x = 0
    while x < W:
        bw = rnd.randrange(40, 120, 8)
        mid = abs((x + bw / 2) - cx) < 260
        bh = rnd.randrange(12, 40, 4) if mid else rnd.randrange(24, 92, 4)
        s += rect(x, HOR - bh, bw, bh, '#120f26')
        s += rect(x, HOR - bh, bw, 4, '#2a1f4a')
        for wy in range(HOR - bh + 12, HOR - 8, 14):
            for wx in range(x + 8, x + bw - 8, 16):
                if rnd.random() < .22:
                    cls = ' class="tw st%d"' % rnd.randrange(4) if rnd.random() < .3 else ''
                    s += rect(wx, wy, 4, 6, y, cls)
        x += bw + rnd.choice([0, 0, 8])

    # ground grid (flipbook of 4 phases for scrolling perspective)
    s += rect(0, HOR, W, H - HOR, '#0b0a16')
    s += rect(0, HOR, W, 4, p)
    for kk in range(-9, 10):
        s += (f'<line x1="{cx + kk * 30}" y1="{HOR}" x2="{cx + kk * 190}" y2="{H}" '
              f'stroke="{p}" stroke-opacity=".45" stroke-width="3"/>')
    NF = 4
    for ph in range(NF):
        g = ''
        for i in range(6):
            t = (i + ph / NF) / 6
            gy = HOR + round((H - HOR) * t * t / 4) * 4
            g += rect(0, gy, W, 4, p, ' opacity=".55"')
        s += f'<g class="gl gl{ph}">{g}</g>'
    css += frames_css('gl', NF, 1.0)

    # title
    title, tpx = 'SMARAN', 18
    tw = text_w(title, tpx)
    tx, ty = round((W - tw) / 2 / 2) * 2, 104
    defs += ('<linearGradient id="tg" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{w}"/><stop offset=".4286" stop-color="{w}"/>'
             f'<stop offset=".4286" stop-color="{y}"/><stop offset=".7143" stop-color="{y}"/>'
             f'<stop offset=".7143" stop-color="{o}"/><stop offset="1" stop-color="{o}"/></linearGradient>')
    from pixel import text_d
    td = text_d(title, tx, ty, tpx)
    td_sh = text_d(title, tx + 8, ty + 8, tpx)
    outline = ''
    for dx in (-6, 0, 6):
        for dy in (-6, 0, 6, 14):
            outline += f'<path fill="{INK}" transform="translate({dx} {dy})" d="{td}"/>'
    defs += f'<clipPath id="tc"><path d="{td}"/></clipPath>'
    s += (f'<g class="tbob">{outline}'
          f'<path fill="#7a3ff0" d="{td_sh}"/>'
          f'<path fill="url(#tg)" d="{td}"/>'
          f'<g clip-path="url(#tc)"><rect class="shine" x="-200" y="{ty - 20}" width="70" height="200" '
          f'fill="#ffffff" opacity=".55" transform="skewX(-20)"/></g></g>')
    css += (".tbob{animation:tbob 3s ease-in-out infinite}"
            "@keyframes tbob{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}"
            ".shine{animation:shine 4.5s linear infinite}"
            "@keyframes shine{0%{transform:skewX(-20deg) translateX(0)}45%,100%{transform:skewX(-20deg) translateX(2000px)}}")

    # tagline

    # HUD corners
    def multi(segs, x, y_, px, anchor='start'):
        full = ''.join(t for t, _ in segs)
        if anchor == 'end':
            x -= text_w(full, px)
        out = ''
        for t, col in segs:
            out += shadow_text(t, x, y_, px, col, INK, off=(0, px))
            x += text_w(t, px) + px
        return out
    s += multi([('CS + MATH', y)], 44, 34, 5)
    s += multi([('UC BERKELEY', y)], W - 44, 34, 5, anchor='end')

    # floating power-ups (one per project)
    pups = [(S.DUMPLING, 190, 100, 6), (S.HOUSE, 262, 246, 6), (S.CUBE, 80, 236, 5),
            (S.INTEGRAL, 1330, 96, 6), (S.BUILDING, 1446, 226, 7), (S.THERMO, 1286, 262, 6)]
    pups = []
    css += (".pu{animation:pu 1.6s steps(1) infinite}"
            "@keyframes pu{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}")
    css += ''.join(f".pu{i}{{animation-delay:{-i * .27:.2f}s}}" for i in range(6))
    for i, (sx, sy) in enumerate([(300, 92), (380, 330), (1420, 80), (1520, 170), (130, 180), (1230, 220)]):
        s += f'<g class="tw st{i % 4}">{sprite(S.SPARK, sx, sy, 3)}</g>'

    # press start

    return frame_panel(W, H, s, css, defs, 'Smaran', border=8)


# ═════════════════════════════════════════════════════════════════════════
# PROJECT TILES
# ═════════════════════════════════════════════════════════════════════════
TW_, TH_, SCENE_H = 800, 500, 330


def tile(name, hook, accent, scene, scene_css='', defs='', award=None, cta='DEMO'):
    s = scene
    # caption area
    s += rect(0, SCENE_H, TW_, TH_ - SCENE_H, '#100e20')
    for i in range(0, TW_, 16):
        s += rect(i, SCENE_H, 8, 4, accent if (i // 16) % 2 == 0 else '#2a2650')
    s += shadow_text(name, 44, 358, 8, CREAM, accent, off=(4, 4))
    hpx = 5 if text_w(hook, 5) <= TW_ - 88 else 4
    s += text(hook, 44, 438 if hpx == 5 else 442, hpx, '#b4afd6')
    if award:
        place, pal = award
        msprite = S.medal(place[0])
        label = f'{place} PLACE'
        pw = 18 + 50 + 18 + text_w(label, 5) + 22
        s += f'<path fill="{INK}" opacity=".92" d="{panel_path(20, 20, pw, 90, 5)}"/>'
        s += sprite(msprite, 38, 30, 5, pal)
        s += text(label, 106, 48, 5, CREAM)
    return frame_panel(TW_, TH_, s, scene_css, defs, f'{name} — {hook.lower()}', border=8)


def scene_picky():
    s, css = bands(0, 0, TW_, SCENE_H, ['#1e1230', '#24142f', '#2c1630', '#371a32']), ''
    s += rect(0, 286, TW_, 44, '#22122a')
    s += rect(0, 286, TW_, 4, '#4a2440')
    # dumpling hero
    dw, dh = sprite_size(S.DUMPLING, 10)
    dx, dy = 400 - dw // 2, 176
    s += rect(dx + 20, dy + dh + 2, dw - 40, 8, '#120a18')
    s += f'<g class="dump">{sprite(S.DUMPLING, dx, dy, 10)}</g>'
    css += (".dump{transform-box:fill-box;transform-origin:50% 100%;animation:dump 1.1s ease-in-out infinite}"
            "@keyframes dump{0%,100%{transform:translateY(0) scale(1.07,.93)}15%{transform:translateY(0) scale(1,1)}50%{transform:translateY(-22px) scale(.96,1.05)}85%{transform:translateY(0) scale(1,1)}}")
    # pin pops over the winner
    s += f'<g class="pin">{sprite(S.PIN, 400 - 21, 70, 6)}</g>'
    css += (".pin{animation:pin 3s ease-in-out infinite}"
            "@keyframes pin{0%{opacity:0;transform:translateY(-20px)}20%{opacity:1;transform:translateY(0)}"
            "30%{transform:translateY(-8px)}40%,90%{opacity:1;transform:translateY(0)}91%,100%{opacity:0}}")
    # phones voting
    phones = [(64, 124, S.PIZZA), (190, 176, S.SUSHI), (660, 84, S.TACO), (552, 168, S.NOODLE)]
    for i, (px_, py_, food) in enumerate(phones):
        s += f'<g class="ph ph{i}">{sprite(S.PHONE, px_, py_, 6)}{sprite(food, px_ + 12, py_ + 30, 6)}</g>'
        s += f'<g class="ht ht{i}">{sprite(S.HEART, px_ + 12, py_ - 30, 6)}</g>'
    css += (".ph{animation:bob 1.4s ease-in-out infinite}"
            ".ht{opacity:0;animation:ht 3s ease-out infinite}"
            "@keyframes ht{0%{opacity:0;transform:translateY(0)}10%{opacity:1}55%{opacity:1;transform:translateY(-48px)}70%,100%{opacity:0;transform:translateY(-60px)}}")
    css += ''.join(f".ph{i}{{animation-delay:{-i * .3:.1f}s}}.ht{i}{{animation-delay:{i * .5:.1f}s}}" for i in range(4))
    for i, (sx, sy) in enumerate([(300, 110), (488, 140), (260, 250), (540, 260)]):
        s += f'<g class="tw st{i}">{sprite(S.SPARK, sx, sy, 3)}</g>'
    css += ''.join(f".st{i}{{animation-delay:{-i * .6:.1f}s}}" for i in range(4))
    return s, css


def scene_claim():
    s, css = bands(0, 0, TW_, SCENE_H, ['#0e1530', '#101a38', '#121f40', '#142548']), ''
    s += rect(0, 270, TW_, 60, '#0c1228')
    s += rect(0, 270, TW_, 4, '#26407a')
    # house
    s += sprite(S.HOUSE, 70, 150, 10)
    # document with stamp
    doc = ["kkkkkkkkkkk."] + ["kwwwwwwwwwkk"] * 0 + [
        "kwwwwwwwwwk.", "kwyywwwwwwk.", "kwwwwwwwwwk.", "kwggggggwwk.", "kwwwwwwwwwk.",
        "kwgggggggwk.", "kwwwwwwwwwk.", "kwggggwwwwk.", "kwwwwwwwwwk.", "kwgggggggwk.",
        "kwwwwwwwwwk.", "kwwwwwwwwwk.", "kkkkkkkkkkk."]
    s += sprite(doc, 320, 106, 10)
    s += f'<g class="stamp">{sprite(S.CHECK, 386, 186, 7)}</g>'
    css += (".stamp{transform-box:fill-box;transform-origin:center;animation:stamp 2.8s ease-out infinite}"
            "@keyframes stamp{0%,25%{opacity:0;transform:scale(2)}32%{opacity:1;transform:scale(.9)}"
            "38%,88%{opacity:1;transform:scale(1)}95%,100%{opacity:0;transform:scale(1)}}")
    # robot agents
    for i, rx in enumerate([548, 650]):
        s += f'<g class="rb rb{i}">{sprite(S.ROBOT, rx, 194 if i == 0 else 208, 7 if i == 0 else 6)}</g>'
    css += (".rb{animation:rb 1s ease-in-out infinite}"
            "@keyframes rb{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}"
            ".rb1{animation-delay:-.5s}")
    # tax going down
    s += text('$', 660, 70, 8, y)
    s += f'<g class="dn">{sprite(S.ARROW_DOWN, 712, 72, 6)}</g>'
    css += (".dn{animation:dn 1.4s ease-in-out infinite}"
            "@keyframes dn{0%,100%{transform:translateY(-6px)}50%{transform:translateY(12px)}}")
    # dotted path robot -> doc
    for i, dx in enumerate(range(452, 540, 16)):
        s += rect(dx, 236, 8, 8, b, f' class="dot dot{i}"')
    css += (".dot{animation:dot 1.2s steps(1) infinite}"
            "@keyframes dot{0%,100%{opacity:.2}50%{opacity:1}}")
    css += ''.join(f".dot{i}{{animation-delay:{-(6 - i) * .2:.1f}s}}" for i in range(6))
    return s, css


def scene_town():
    s, css = bands(0, 0, TW_, SCENE_H, ['#0f1424', '#111a2a', '#132230', '#142a30']), ''
    ox, oy, TW, TH, N = 400, 64, 32, 16, 7
    P = lambda i, j: (ox + (i - j) * TW, oy + (i + j) * TH)
    road = lambda i, j: i == 3 or j == 3
    rnd = random.Random(11)
    # ground
    for d in range(2 * N - 1):
        for i in range(N):
            j = d - i
            if not 0 <= j < N:
                continue
            x, y_ = P(i, j)
            col = '#2b2f48' if road(i, j) else ('#1f6b52' if (i + j) % 2 else '#24795c')
            s += poly([(x, y_), (x + TW, y_ + TH), (x, y_ + 2 * TH), (x - TW, y_ + TH)], col)
    # side lip of the board
    L0, B0, R0 = P(0, N), P(N, N), P(N, 0)
    s += poly([L0, B0, (B0[0], B0[1] + 16), (L0[0], L0[1] + 16)], '#14473a')
    s += poly([B0, R0, (R0[0], R0[1] + 16), (B0[0], B0[1] + 16)], '#0e3329')
    # buildings
    palettes = [('#c4adff', '#9b6bff', '#6a45c8'), ('#9fd8ff', '#4fb3ff', '#2f7fc4'),
                ('#ffd98a', '#ffc23d', '#c98d1c'), ('#ffa3c2', '#ff4f8b', '#c42e64'),
                ('#e8e4ff', '#c8c4e4', '#8a86a8')]
    flag_at = (5, 1)
    win_i = 0
    for d in range(2 * N - 1):
        for i in range(N):
            j = d - i
            if not 0 <= j < N or road(i, j):
                continue
            if (i, j) != flag_at and rnd.random() > .62:
                # trees instead
                x, y_ = P(i, j)
                s += rect(x - 3, y_ + 6, 6, 10, '#5a3a22') + rect(x - 9, y_ - 8, 18, 14, '#3ee6a8') + rect(x - 9, y_ - 8, 18, 4, '#8affd0')
                continue
            x, y_ = P(i, j)
            h = 72 if (i, j) == flag_at else rnd.choice([16, 24, 32, 40, 48])
            top, lft, rgt = rnd.choice(palettes)
            cube, (L, B, R, T) = iso_cube(x, y_, TW, TH, h, top, lft, rgt)
            s += cube
            for row in range(h // 14):
                for t in (.35, .7):
                    wx = L[0] + t * (B[0] - L[0])
                    wy = L[1] + t * (B[1] - L[1]) - 10 - row * 14
                    cls = f' class="tw st{win_i % 4}"' if win_i % 3 == 0 else ''
                    s += rect(round(wx) - 2, round(wy) - 3, 4, 6, '#fff1b0', cls)
                    win_i += 1
            if (i, j) == flag_at:
                fx, fy = T[0], T[1] - h
                s += rect(fx, fy - 40, 4, 40, w)
                s += f'<g class="fl fl0">{rect(fx + 4, fy - 40, 24, 14, p)}</g>'
                s += f'<g class="fl fl1">{rect(fx + 4, fy - 38, 24, 12, p)}{rect(fx + 20, fy - 40, 8, 4, p)}</g>'
                bub = text('!', fx - 30, fy - 44, 4, k)
                s += (f'<g class="bub"><path fill="{w}" d="{panel_path(fx - 42, fy - 54, 28, 46, 3)}"/>{bub}</g>')
    css += frames_css('fl', 2, .6)
    css += (".bub{animation:bub 3s steps(1) infinite}"
            "@keyframes bub{0%,55%{opacity:0}56%,95%{opacity:1}96%,100%{opacity:0}}")
    css += ''.join(f".st{i}{{animation-delay:{-i * .6:.1f}s}}" for i in range(4))
    # agents walking along both roads
    agents = [((3, 0), (3, 6), m, 0), ((3, 6), (3, 0), y, -2.5), ((0, 3), (6, 3), b, -1),
              ((6, 3), (0, 3), p, -4), ((3, 1), (3, 5), w, -5)]
    for n_, ((i0, j0), (i1, j1), col, dl) in enumerate(agents):
        x0, y0 = P(i0, j0); x1, y1 = P(i1, j1)
        y0 += TH; y1 += TH
        steps = 6 * 4
        s += f'<g class="ag ag{n_}">{sprite(S.PERSON, -5, -14, 3, {"w": col})}{rect(-5, 0, 9, 3, "#14182a", " opacity=\".6\"")}</g>'
        css += (f".ag{n_}{{animation:ag{n_} 7s steps({steps}) infinite;animation-delay:{dl}s}}"
                f"@keyframes ag{n_}{{0%{{transform:translate({x0}px,{y0}px)}}100%{{transform:translate({x1}px,{y1}px)}}}}")
    return s, css


def scene_rubish():
    s, css = bands(0, 0, TW_, SCENE_H, ['#18122a', '#1c142e', '#211631', '#271934']), ''
    # oblique cube
    st, gap = 34, 6
    face = 3 * st + 4 * gap  # 126
    fx, fy, depth = 400 - face // 2 - 20, 104, 44
    sk = lambda x, y_, t: (x + t, y_ - t)
    # body
    s += poly([(fx, fy), sk(fx, fy, depth), sk(fx + face, fy, depth), (fx + face, fy)], INK)
    s += poly([(fx + face, fy), sk(fx + face, fy, depth), sk(fx + face, fy + face, depth), (fx + face, fy + face)], INK)
    s += rect(fx, fy, face, face, INK)
    cols = {'w': '#f4f1ff', 'y': '#ffd23d', 'r': '#ff3d5a', 'o': '#ff8a3d', 'b': '#3d8bff', 'g': '#2fd38f'}
    # top face stickers (yellow), right face (blue/green)
    for a in range(3):
        for c in range(3):
            t0 = gap * .5 + a * (depth - gap) / 3 + gap / 2
            t1 = t0 + (depth - 2 * gap) / 3
            x0 = fx + gap + c * (st + gap)
            s += poly([sk(x0, fy, t0), sk(x0 + st, fy, t0), sk(x0 + st, fy, t1), sk(x0, fy, t1)],
                      cols['y' if (a + c) % 4 else 'o'])
            y0 = fy + gap + c * (st + gap)
            s += poly([sk(fx + face, y0, t0), sk(fx + face, y0, t1), sk(fx + face, y0 + st, t1), sk(fx + face, y0 + st, t0)],
                      cols['b' if (a * 3 + c) % 3 else 'g'])
    # front face flipbook: H I  [scramble]  C O O L  [scramble]
    L = {'H': ["X.X", "XXX", "X.X"], 'I': ["XXX", ".X.", "XXX"], 'C': ["XXX", "X..", "XXX"],
         'O': ["XXX", "X.X", "XXX"], 'L': ["X..", "X..", "XXX"]}
    rnd = random.Random(5)
    seq = ['H', 'I', None, 'C', 'O', 'O', 'L', None]
    for fi, ch in enumerate(seq):
        g = ''
        for rr in range(3):
            for cc in range(3):
                if ch:
                    col = cols['r'] if L[ch][rr][cc] == 'X' else cols['w']
                else:
                    col = cols[rnd.choice('wyrobg')]
                g += rect(fx + gap + cc * (st + gap), fy + gap + rr * (st + gap), st, st, col)
                g += rect(fx + gap + cc * (st + gap) + 4, fy + gap + rr * (st + gap) + 4, 8, 4, '#ffffff', ' opacity=".5"')
        s += f'<g class="cf cf{fi}">{g}</g>'
    css += frames_css('cf', len(seq), 7.2)
    # typed word beside the cube, synced to the flipbook
    words = ['H', 'HI', 'HI', 'C', 'CO', 'COO', 'COOL', 'COOL']
    for fi, wd in enumerate(words):
        s += f'<g class="cf cf{fi}">{text("> " + wd + "_", 96, 150, 5, PAL["m"])}</g>'
    # move notation ticker
    moves = "R U R' U' F2 L' D B2 U R2 F' L2 D' R U2 B' "
    tick = moves * 2
    tw_ = text_w(moves, 3)
    s += rect(0, 282, TW_, 48, '#140f22')
    s += f'<g class="tick">{text(tick, 20, 296, 3, "#8f86c0")}</g>'
    css += (f".tick{{animation:tick 9s steps(90) infinite}}"
            f"@keyframes tick{{0%{{transform:translateX(0)}}100%{{transform:translateX(-{tw_ + 12}px)}}}}")
    return s, css


def scene_multivis():
    s, css = bands(0, 0, TW_, SCENE_H, ['#0c1230', '#0e1636', '#101a3c', '#121e44']), ''
    ox, oy, TW, TH, N = 470, 168, 22, 11, 6
    P = lambda i, j: (ox + (i - j) * TW, oy + (i + j) * TH)
    # base plate
    s += poly([P(0, 0), P(N, 0), P(N, N), P(0, N)], '#1a2556')
    for i in range(N + 1):
        a, b_ = P(i, 0), P(i, N)
        s += f'<line x1="{a[0]}" y1="{a[1]}" x2="{b_[0]}" y2="{b_[1]}" stroke="#2c3c80" stroke-width="2"/>'
        a, b_ = P(0, i), P(N, i)
        s += f'<line x1="{a[0]}" y1="{a[1]}" x2="{b_[0]}" y2="{b_[1]}" stroke="#2c3c80" stroke-width="2"/>'
    # z axis
    zx, zy = P(0, 0)
    s += rect(zx - 2, zy - 126, 4, 126, '#c8c4e4') + poly([(zx - 8, zy - 126), (zx + 8, zy - 126), (zx, zy - 140)], '#c8c4e4')
    shades = [('#9fd8ff', '#4fb3ff', '#2f7fc4'), ('#c4adff', '#9b6bff', '#6a45c8'), ('#ffa3c2', '#ff4f8b', '#c42e64')]
    NF = 6
    for ph in range(NF):
        g = ''
        phase = ph * 2 * math.pi / NF
        for d in range(2 * N - 1):
            for i in range(N):
                j = d - i
                if not 0 <= j < N:
                    continue
                f = .5 + .5 * math.sin(.95 * i + phase) * math.cos(.75 * j - phase / 2)
                h = 14 + round(f * 100 / 4) * 4
                sh = shades[0 if f < .4 else (1 if f < .7 else 2)]
                x, y_ = P(i, j)
                cube, _ = iso_cube(x, y_, TW, TH, h, *sh, inset=.86)
                g += cube
        s += f'<g class="mv mv{ph}">{g}</g>'
    css += frames_css('mv', NF, 2.4)
    # big double integral glyph
    s += sprite(S.INTEGRAL, 86, 92, 9)
    s += sprite(S.INTEGRAL, 140, 92, 9)
    s += text('DXDY', 210, 196, 5, '#9fd8ff')
    return s, css


def scene_tempest():
    s, css = bands(0, 0, TW_, SCENE_H, ['#1a1222', '#1e1424', '#231626', '#2a1828']), ''
    s += rect(0, 262, TW_, 68, '#1a1020') + rect(0, 262, TW_, 4, '#4a2a3a')
    # arduino board
    bx, by = 48, 150
    s += rect(bx, by, 156, 104, INK) + rect(bx + 4, by + 4, 148, 96, '#1a8c8c') + rect(bx + 4, by + 4, 148, 6, '#2fb3b0')
    s += rect(bx - 14, by + 22, 30, 28, '#c8c4e4') + rect(bx - 14, by + 22, 30, 6, '#ffffff')
    s += rect(bx + 54, by + 44, 70, 32, INK)
    for i in range(7):
        s += rect(bx + 58 + i * 9, by + 38, 4, 6, '#8a86a8') + rect(bx + 58 + i * 9, by + 76, 4, 6, '#8a86a8')
    for i in range(12):
        s += rect(bx + 24 + i * 10, by + 14, 6, 6, INK)
    s += f'<g class="blink">{rect(bx + 20, by + 76, 8, 8, PAL["m"])}</g>'
    s += rect(bx + 34, by + 76, 8, 8, '#2a5a5a')
    # wires to sensor
    s += rect(bx + 156, by + 20, 64, 4, r) + rect(bx + 156, by + 30, 64, 4, INK) + rect(bx + 156, by + 40, 64, 4, y)
    sx_, sy_ = bx + 220, by + 2
    s += rect(sx_, sy_, 52, 60, INK) + rect(sx_ + 4, sy_ + 4, 44, 52, '#3d8bff')
    for gy in range(3):
        for gx in range(3):
            s += rect(sx_ + 10 + gx * 12, sy_ + 10 + gy * 14, 8, 8, '#bfe0ff')
    # thermometer
    s += sprite(S.THERMO, 342, 92, 6)
    # data packets flying to the monitor
    for i in range(3):
        s += f'<g class="pk pk{i}">{rect(0, 0, 8, 8, o)}</g>'
    css += (".pk{animation:pk 1.8s linear infinite}"
            "@keyframes pk{0%{transform:translate(388px,176px)}100%{transform:translate(460px,176px)}}")
    css += ''.join(f".pk{i}{{animation-delay:{-i * .6:.1f}s}}" for i in range(3))
    # monitor with live chart
    mx, my, mw, mh = 470, 44, 296, 214
    s += rect(mx, my, mw, mh, INK) + rect(mx + 8, my + 8, mw - 16, mh - 16, '#101a1e')
    s += rect(mx + mw // 2 - 30, my + mh, 60, 12, INK) + rect(mx + mw // 2 - 50, my + mh + 12, 100, 6, INK)
    for gy in range(my + 60, my + mh - 8, 30):
        s += rect(mx + 8, gy, mw - 16, 2, '#1c2c34')
    period, stepx = 280, 14
    pts, area = [], []
    X0 = mx + 8
    for n_ in range(0, 2 * period + stepx * 2, stepx):
        val = 150 + 26 * math.sin(2 * math.pi * n_ / period) + 10 * math.sin(6 * math.pi * n_ / period)
        yy = round(val / 4) * 4
        if pts:
            pts.append((X0 + n_, pts[-1][1]))
        pts.append((X0 + n_, yy))
    line = ' '.join(f'{a},{b_}' for a, b_ in pts)
    areap = f'{X0},{my + mh - 8} ' + line + f' {pts[-1][0]},{my + mh - 8}'
    css += (f".scr{{animation:scr 6s linear infinite}}"
            f"@keyframes scr{{0%{{transform:translateX(0)}}100%{{transform:translateX(-{period}px)}}}}")
    defs = f'<clipPath id="mon"><rect x="{mx + 8}" y="{my + 8}" width="{mw - 16}" height="{mh - 16}"/></clipPath>'
    s += (f'<g clip-path="url(#mon)"><g class="scr"><polygon points="{areap}" fill="{o}" opacity=".18"/>'
          f'<polyline points="{line}" fill="none" stroke="{o}" stroke-width="4"/></g></g>')
    # readout flipbook
    temps = ['71°F', '72°F', '72°F', '73°F']
    for i, t in enumerate(temps):
        s += f'<g class="rd rd{i}">{text(t, mx + 22, my + 22, 4, y)}</g>'
    css += frames_css('rd', 4, 4)
    s += f'<g class="blink">{rect(mx + mw - 74, my + 26, 10, 10, r)}</g>' + text('LIVE', mx + mw - 58, my + 26, 2, '#ffb3c0')
    return s, css, defs


from scenes2 import scene_rubish, scene_multivis, scene_town  # smooth versions

TILES = [
    # key, name, hook, accent, scene fn, award, cta, link
    ('rubish', 'RUBISH', 'SPELL WORDS ON A CUBE', y, scene_rubish, None, 'REPO'),
    ('town-trial', 'TOWN TRIAL', 'AGENTS TEST TOWN POLICY', PAL['m'], scene_town, None, 'REPO'),
    ('picky', 'PICKY', 'EVERYONE AGREES ON FOOD', p, scene_picky, ('2ND', S.SILVER), 'REPO'),
    ('claimos', 'CLAIM OS', 'AGENTS APPEAL YOUR TAXES', b, scene_claim, ('4TH', S.VIOLET), 'REPO'),
    ('multivis', 'MULTIVIS', 'SEE INTEGRALS IN 3D', v, scene_multivis, None, 'REPO'),
    ('tempest', 'TEMPEST', 'LIVE INDOOR CLIMATE', o, scene_tempest, None, 'REPO'),
]


# ═════════════════════════════════════════════════════════════════════════
# TRANSPARENT ASSETS (light + dark variants)
# ═════════════════════════════════════════════════════════════════════════
# These sit on GitHub's page background, so each carries its own dark panel
# and looks identical in light mode, dark mode and any Markdown viewer.
PANEL_BG, PANEL_EDGE, TXT, DIM = '#16142a', '#3a3366', '#f3efff', '#a9a4cc'


def plate(x, y, w, h, c=8):
    """Dark card with an ink border and bevel, like the project tiles."""
    return (f'<path fill="{INK}" d="{panel_path(x, y, w, h, c)}"/>'
            f'<path fill="{PANEL_BG}" d="{panel_path(x + c, y + c, w - 2 * c, h - 2 * c, c)}"/>'
            f'<path fill="none" stroke="{PANEL_EDGE}" stroke-width="4" d="{panel_path(x + c + 2, y + c + 2, w - 2 * c - 4, h - 2 * c - 4, c)}"/>')


def section_header(label):
    W, H, px = 1600, 104, 5
    s, css = '', BASE_CSS
    tw = text_w(label, px)
    aw = text_w('▶', px)
    pw = tw + 2 * (aw + 60) + 80
    s += plate((W - pw) / 2, 4, pw, H - 8)
    s += shadow_text(label, W / 2, 34, px, TXT, INK, off=(0, 5), anchor='middle')
    s += f'<g class="ar">{text("▶", W / 2 - tw / 2 - 60 - aw, 34, px, y)}</g>'
    s += f'<g class="ar">{text("◀", W / 2 + tw / 2 + 60, 34, px, y)}</g>'
    css += (".ar{animation:ar 1s ease-in-out infinite}"
            "@keyframes ar{0%,100%{opacity:1}50%{opacity:.35}}")
    return svg(W, H, s, css, title=label.title())


def award(place, line1, project, medal_pal, accent):
    W, H = 800, 240
    s, css = plate(0, 0, W, H), BASE_CSS
    mw, mh = sprite_size(S.MEDAL, 9)
    s += f'<g class="spin">{sprite(S.medal(place[0]), 66, (H - mh) // 2, 9, medal_pal)}</g>'
    css += (".spin{transform-box:fill-box;transform-origin:center;animation:spin 3s ease-in-out infinite}"
            "@keyframes spin{0%,55%{transform:scaleX(1)}77%{transform:scaleX(-1)}100%{transform:scaleX(1)}}")
    for i, (sx, sy) in enumerate([(40, 50), (160, 60), (150, 180)]):
        s += f'<g class="tw st{i}">{sprite(S.SPARK, sx, sy, 3, {"w": accent})}</g>'
    css += ''.join(f".st{i}{{animation-delay:{-i * .7:.1f}s}}" for i in range(3))
    tx = 210
    s += shadow_text(f'{place} PLACE', tx, 52, 7, TXT, accent, off=(0, 7))
    s += text(line1, tx, 130, 4, TXT)
    s += text(project, tx, 172, 3, accent)
    return svg(W, H, s, css, title=f'{place} place, {line1.title()}')


def footer():
    W, H = 1600, 280
    s, css = plate(0, 0, W, H), BASE_CSS
    s += shadow_text('THANKS FOR VIEWING', W / 2, 46, 6, TXT, INK, off=(0, 6), anchor='middle')
    s += rect(48, 236, W - 96, 4, PANEL_EDGE)
    for x in range(48, W - 48, 40):
        s += rect(x, 244, 16, 4, PANEL_EDGE)
    parade = [S.DUMPLING, S.ROBOT, S.CUBE, S.HOUSE, S.BUILDING, S.THERMO, S.ROBOT]
    scales = [6, 6, 5, 6, 6, 6, 5]
    defs = f'<clipPath id="fc"><rect x="20" y="100" width="{W - 40}" height="140"/></clipPath>'
    g, gap = '', 232
    total = gap * len(parade)
    for i, (sp, sc) in enumerate(zip(parade, scales)):
        sw, sh = sprite_size(sp, sc)
        g += f'<g class="hop hop{i}">{sprite(sp, i * gap, 236 - sh, sc)}</g>'
    s += f'<g clip-path="url(#fc)"><g class="march">{g}<g transform="translate({total} 0)">{g}</g></g></g>'
    css += (f".march{{animation:march 20s linear infinite}}"
            f"@keyframes march{{0%{{transform:translateX(0)}}100%{{transform:translateX(-{total}px)}}}}"
            ".hop{animation:hop .7s ease-in-out infinite}"
            "@keyframes hop{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}")
    css += ''.join(f".hop{i}{{animation-delay:{-i * .2:.1f}s}}" for i in range(len(parade)))
    tw = text_w('THANKS FOR VIEWING', 6)
    s += text('♥', W / 2 - tw / 2 - 50, 46, 6, p) + text('♥', W / 2 + tw / 2 + 20, 46, 6, p)
    return svg(W, H, s, css, defs, title='Thanks for viewing')


# ═════════════════════════════════════════════════════════════════════════
# DEMO BUTTONS (one under each tile that has a live site)
# ═════════════════════════════════════════════════════════════════════════
GIF_TILES = {'rubish', 'town-trial', 'multivis'}
DEMOS = ['rubish', 'town-trial', 'picky', 'multivis']


def _mix(hex_, t, to=(255, 255, 255)):
    c = [int(hex_[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{round(a + (b_ - a) * t):02x}' for a, b_ in zip(c, to))


def demo_button(accent):
    W, H, c = 800, 112, 6
    s, css = '', BASE_CSS
    s += f'<path fill="{INK}" d="{panel_path(0, 0, W, H, c)}"/>'
    inner = panel_path(6, 6, W - 12, H - 12, c)
    defs = f'<clipPath id="bc"><path d="{inner}"/></clipPath>'
    s += (f'<g clip-path="url(#bc)">{rect(0, 0, W, H, accent)}{rect(0, 6, W, 8, _mix(accent, .45))}'
          f'{rect(0, H - 18, W, 12, _mix(accent, .35, (11, 10, 20)))}'
          f'<rect class="shine" x="-120" y="0" width="60" height="{H}" fill="#ffffff" opacity=".35" transform="skewX(-20)"/></g>')
    label = 'PLAY DEMO'
    lw = text_w(label, 7)
    aw = text_w('▶', 7) + 24
    x0 = (W - lw - aw) / 2
    s += f'<g class="nudge">{text("▶", x0, 28, 7, INK)}</g>'
    s += text(label, x0 + aw, 28, 7, INK)
    css += (".shine{animation:shine 3.6s linear infinite}"
            "@keyframes shine{0%{transform:skewX(-20deg) translateX(0)}50%,100%{transform:skewX(-20deg) translateX(1100px)}}"
            ".nudge{animation:nudge 1s ease-in-out infinite}"
            "@keyframes nudge{0%,100%{transform:translateX(0)}50%{transform:translateX(8px)}}")
    return svg(W, H, s, css, defs, 'Play demo')


SPACER = svg(800, 112, '', title='')


def continue_button():
    W, H, c = 560, 112, 6
    s, css = '', BASE_CSS
    accent = y
    s += f'<path fill="{INK}" d="{panel_path(0, 0, W, H, c)}"/>'
    inner = panel_path(6, 6, W - 12, H - 12, c)
    defs = f'<clipPath id="bc"><path d="{inner}"/></clipPath>'
    s += (f'<g clip-path="url(#bc)">{rect(0, 0, W, H, accent)}{rect(0, 6, W, 8, _mix(accent, .45))}'
          f'{rect(0, H - 18, W, 12, _mix(accent, .35, (11, 10, 20)))}'
          f'<rect class="shine" x="-120" y="0" width="60" height="{H}" fill="#ffffff" opacity=".35" transform="skewX(-20)"/></g>')
    label = 'CONTINUE'
    lw = text_w(label, 7)
    aw = text_w('▶', 7) + 28
    x0 = (W - lw - aw) / 2
    s += text(label, x0, 28, 7, INK)
    s += f'<g class="nudge">{text("▶", x0 + lw + 28, 28, 7, INK)}</g>'
    css += (".shine{animation:shine 3.6s linear infinite}"
            "@keyframes shine{0%{transform:skewX(-20deg) translateX(0)}50%,100%{transform:skewX(-20deg) translateX(1000px)}}"
            ".nudge{animation:nudge 1s ease-in-out infinite}"
            "@keyframes nudge{0%,100%{transform:translateX(0)}50%{transform:translateX(8px)}}")
    return svg(W, H, s, css, defs, 'Continue')


from hero2 import hero  # animated banner (replaces the older hero above)


# ═════════════════════════════════════════════════════════════════════════
def main():
    os.makedirs(OUT, exist_ok=True)
    files = {}
    files['hero.svg'] = hero()
    for key, name, hook, accent, fn, aw, cta in TILES:
        res = fn()
        scene, css = res[0], res[1]
        defs = res[2] if len(res) > 2 else ''
        if key in GIF_TILES:   # rendered in 3D by build_gifs.py
            continue
        files[f'tile-{key}.svg'] = tile(name, hook, accent, scene, css, defs, aw, cta)
    accents = {t[0]: t[3] for t in TILES}
    for key in DEMOS:
        files[f'btn-demo-{key}.svg'] = demo_button(accents[key])
    files['spacer.svg'] = SPACER
    files['btn-continue.svg'] = continue_button()
    files['header-projects.svg'] = section_header('SELECT A PROJECT')
    files['header-trophies.svg'] = section_header('TROPHIES')
    files['award-picky.svg'] = award('2ND', 'HACK WITH CLAUDE', 'PICKY', S.SILVER, p)
    files['award-claimos.svg'] = award('4TH', 'YC X NAIVE HACKATHON', 'CLAIM OS', S.VIOLET, b)
    files['footer.svg'] = footer()
    for name, data in files.items():
        with open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(data)
        print(f'{name:32s} {len(data) / 1024:6.1f} KB')


if __name__ == '__main__':
    main()
