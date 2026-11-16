#!/usr/bin/env python3
"""Render the three 3D tiles (rubish, Town Trial, Multivis) as GIFs.

    python3 tools/build_gifs.py            # all three
    python3 tools/build_gifs.py rubish     # just one

Each tile = caption + frame from build_assets.tile() (rendered once with
Chrome), with a 3D scene rendered per frame by render3d.py and pasted in.
"""
import asyncio
import math
import os
import random
import sys

import numpy as np
from PIL import Image

import build_assets as BA
import sprites as S
from pixel import PAL, INK, panel_path, svg
from render3d import (Cam, Face, Obj, box, oriented_box, face_point, render, ptext, psprite,
                      bands_img, rgb, add, mul)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = BA.OUT
TMP = '/tmp/gif_build'
SW, SH = 400, 165          # scene render size (half res), upscaled 2x to 800x330
FPS = 20


# ── tile chrome (caption, border) rendered once via Chrome ────────────────
def chrome_pngs(key):
    os.makedirs(TMP, exist_ok=True)
    t = next(t for t in BA.TILES if t[0] == key)
    _, name, hook, accent, _, award, cta = t
    base = BA.tile(name, hook, accent, '', '', '', award, cta)
    W, H, b = 800, 500, 8
    over = svg(W, H,
               f'<path fill="{INK}" fill-rule="evenodd" d="{panel_path(0, 0, W, H, b)}{panel_path(b, b, W - 2 * b, H - 2 * b, b)}"/>'
               f'<path fill="none" stroke="#3a3366" stroke-width="4" d="{panel_path(b + 2, b + 2, W - 2 * b - 4, H - 2 * b - 4, b)}"/>')
    paths = {}
    for nm, data in (('base', base), ('over', over)):
        p = f'{TMP}/{key}-{nm}.svg'
        open(p, 'w').write(data)
        paths[nm] = p

    async def shoot():
        from playwright.async_api import async_playwright
        async with async_playwright() as pw:
            br = await pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
            pg = await br.new_page(viewport={'width': 800, 'height': 500}, device_scale_factor=1)
            for nm, p in paths.items():
                html = f'{TMP}/{nm}.html'
                open(html, 'w').write(f'<body style="margin:0;background:transparent">'
                                      f'<img id="i" src="file://{p}" style="width:800px;height:500px;display:block"></body>')
                await pg.goto('file://' + html)
                await pg.wait_for_timeout(150)
                await pg.locator('#i').screenshot(path=f'{TMP}/{key}-{nm}.png', omit_background=True)
            await br.close()
    asyncio.run(shoot())
    return (Image.open(f'{TMP}/{key}-base.png').convert('RGBA'),
            Image.open(f'{TMP}/{key}-over.png').convert('RGBA'))


def save_gif(key, scenes, delay_ms):
    base, over = chrome_pngs(key)
    frames = []
    for sc in scenes:
        f = base.copy()
        f.paste(sc.resize((800, 330), Image.NEAREST), (0, 0))
        f.alpha_composite(over)
        frames.append(f.convert('RGB'))
    # one global palette so colours never flicker
    sample = frames[::max(1, len(frames) // 12)]
    strip = Image.new('RGB', (800, 500 * len(sample)))
    for i, fr in enumerate(sample):
        strip.paste(fr, (0, 500 * i))
    pal = strip.quantize(colors=255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    q = [fr.quantize(palette=pal, dither=Image.Dither.NONE) for fr in frames]
    path = os.path.join(OUT, f'tile-{key}.gif')
    q[0].save(path, save_all=True, append_images=q[1:], duration=delay_ms, loop=0, optimize=False, disposal=1)
    print(f'tile-{key}.gif  {len(q)} frames  {os.path.getsize(path) / 1e6:.2f} MB')
    return path


# ═════════════════════════════════════════════════════════════════════════
# TOWN TRIAL: the whole town on a turntable, agents walking in and out
# ═════════════════════════════════════════════════════════════════════════
PERSON_A = [".kkk.", ".kwk.", "kkkkk", "kccck", "kccck", ".kkk.", ".k.k.", ".k.k."]
PERSON_B = [".kkk.", ".kwk.", "kkkkk", "kccck", "kccck", ".kkk.", ".k.k.", "k...k"]


def town_scenes(T=12.0):
    N, rnd = 5, random.Random(4)
    road = lambda i, j: i == 2 or j == 2
    C = lambda i: i - 2  # cell index -> centre coordinate
    grass, grass2, roadc = rgb('#24795c'), rgb('#1f6b52'), rgb('#2b2f48')
    pals = [('#c4adff', '#9b6bff'), ('#9fd8ff', '#4fb3ff'), ('#ffd98a', '#ffc23d'),
            ('#ffa3c2', '#ff4f8b'), ('#e8e4ff', '#c8c4e4')]
    win = rgb('#fff1b0')

    static = []
    # board slab with tiles painted on its top
    slab = box(-2.5, 2.5, -0.2, 0, -2.5, 2.5, rgb('#14473a'), top=grass, bottom=False)
    top = slab[0]
    top.flat = True
    for i in range(N):
        for j in range(N):
            x0, z0 = C(i) - .5, C(j) - .5
            col = roadc if road(i, j) else (grass if (i + j) % 2 else grass2)
            top.deco.append(([(x0, 0, z0), (x0 + 1, 0, z0), (x0 + 1, 0, z0 + 1), (x0, 0, z0 + 1)], col))
    for k in range(-2, 3):
        for (x, z) in [(k, 0), (0, k)]:
            if (x, z) != (0, 0):
                dx, dz = (.14, .03) if z == 0 else (.03, .14)
                top.deco.append(([(x - dx, 0, z - dz), (x + dx, 0, z - dz), (x + dx, 0, z + dz), (x - dx, 0, z + dz)], rgb('#5b6088')))
    static.append(Obj((0, -.1, 0), slab, bias=-50))
    # paths leading out of town
    for d, fade in ((3, .75), (4, .5), (5, .3)):
        for (x, z) in [(d, 0), (-d, 0), (0, d), (0, -d)]:
            c = tuple(round(v * fade + 16 * (1 - fade)) for v in roadc)
            f = Face([(x - .5, 0, z - .5), (x + .5, 0, z - .5), (x + .5, 0, z + .5), (x - .5, 0, z + .5)], (0, 1, 0), c, flat=True)
            static.append(Obj((x, 0, z), [f], bias=-20))

    doors = []
    flag_top = None
    for i in range(N):
        for j in range(N):
            if road(i, j):
                continue
            cx, cz = C(i), C(j)
            if (i, j) == (4, 0) or rnd.random() < .7:
                h = 1.55 if (i, j) == (4, 0) else rnd.choice([.45, .7, .95, 1.2])
                tp, sd = pals[2] if (i, j) == (4, 0) else rnd.choice(pals)
                fs = box(cx - .36, cx + .36, 0, h, cz - .36, cz + .36, rgb(sd), top=rgb(tp), bottom=False)
                for f in fs[1:]:
                    rows = int(h / .26)
                    for r_ in range(rows):
                        for a in (.25, .6):
                            b0 = (.12 + r_ * .26) / h
                            b1 = b0 + .13 / h
                            f.deco.append(([face_point(f.pts, a, b0), face_point(f.pts, a + .15, b0),
                                            face_point(f.pts, a + .15, b1), face_point(f.pts, a, b1)], win))
                static.append(Obj((cx, 0, cz), fs))
                if (i, j) == (4, 0):
                    flag_top = (cx, h, cz)
                if abs(cx) == 1 or abs(cz) == 1:
                    doors.append((cx, cz))
            else:
                fs = box(cx - .07, cx + .07, 0, .3, cz - .07, cz + .07, rgb('#5a3a22'), bottom=False)
                fs += box(cx - .3, cx + .3, .3, .75, cz - .3, cz + .3, rgb('#3ee6a8'), top=rgb('#8affd0'), bottom=False)
                static.append(Obj((cx, 0, cz), fs))

    # agent routes (world units), each loops every `per` seconds
    def door_route(dc, inbound, lane):
        cx, cz = dc
        # walk along the road beside the building, to its door
        if abs(cz) == 1:   # building beside the x road
            door = (cx, cz * .55)
            edge = (-5.2 if cx < 0 else 5.2, lane)
            mid = (cx, lane)
        else:
            door = (cx * .55, cz)
            edge = (lane, -5.2 if cz < 0 else 5.2)
            mid = (lane, cz)
        pts = [edge, mid, door]
        return pts if inbound else pts[::-1]

    cols = [PAL['m'], PAL['y'], PAL['b'], PAL['p'], PAL['w'], '#ffa3c2', '#c4adff', '#ffd98a']
    routes = [
        ([(-5.2, .2), (5.2, .2)], 12, 0.0, 'thru'),
        ([(5.2, -.2), (-5.2, -.2)], 12, .45, 'thru'),
        ([(-.2, -5.2), (-.2, 5.2)], 12, .2, 'thru'),
        ([(.2, 5.2), (.2, -5.2)], 12, .7, 'thru'),
        ([(-5.2, .2), (5.2, .2)], 12, .55, 'thru'),
        (door_route(doors[0], True, .2), 12, .1, 'in'),
        (door_route(doors[-1], False, -.2), 12, .6, 'out'),
        (door_route(doors[len(doors) // 2], True, -.2), 12, .35, 'in'),
    ]

    def where(pts, s):
        seg = [math.dist(pts[k], pts[k + 1]) for k in range(len(pts) - 1)]
        tot, d = sum(seg), s * sum(seg)
        for k, L in enumerate(seg):
            if d <= L:
                a = d / L if L else 0
                return (pts[k][0] + a * (pts[k + 1][0] - pts[k][0]), pts[k][1] + a * (pts[k + 1][1] - pts[k][1]))
            d -= L
        return pts[-1]

    scenes = []
    nf = int(T * FPS)
    for fi in range(nf):
        t = fi / FPS
        cam = Cam(2 * math.pi * t / T + .6, math.radians(32), 29, 200, 98)
        objs = list(static)
        # flag on the tallest building
        fx, fy, fz = flag_top
        pole = box(fx - .025, fx + .025, fy, fy + .55, fz - .025, fz + .025, rgb('#fff4e0'), bottom=False)
        wv = .05 * math.sin(t * 9)
        flag = Face([(fx, fy + .55, fz), (fx + .36, fy + .55 + wv, fz), (fx + .36, fy + .36 + wv, fz), (fx, fy + .36, fz)],
                    (0, 0, 1), rgb(PAL['p']), cull=False)
        objs.append(Obj((fx, 0, fz), pole + [flag], bias=.02))
        # agents
        for n, (pts, per, ph, kind) in enumerate(routes):
            s = ((t / per) + ph) % 1.0
            walk = .72 if kind in ('in', 'out') else 1.0
            if kind == 'out':
                if s > walk:
                    continue
                pos = where(pts, s / walk)
            elif kind == 'in':
                if s > walk:
                    continue
                pos = where(pts, s / walk)
            else:
                pos = where(pts, s)
            leg = PERSON_A if int(t * 6 + n) % 2 else PERSON_B
            pal = dict(k=rgb(INK), w=rgb('#fff4e0'), c=rgb(cols[n % len(cols)]))

            def spr(img, dr, u, v, leg=leg, pal=pal):
                dr.rectangle([u - 4, v - 1, u + 4, v], fill=(10, 12, 20))
                psprite(dr, leg, u - 5, v - 16, 2, pal)
            objs.append(Obj((pos[0], 0, pos[1]), sprite=spr, bias=.01))

        def pre(img, dr, cam):
            bands_img(dr, SW, SH, ['#0f1424', '#111a2a', '#132230', '#142a30'])
        scenes.append(render(objs, cam, (SW, SH), pre=pre))
    return scenes


# ═════════════════════════════════════════════════════════════════════════
# MULTIVIS: Riemann boxes of a moving, signed surface, on a turntable
# ═════════════════════════════════════════════════════════════════════════
def multivis_scenes(T=12.0):
    G, cell = 10, .5
    pos_cols = [(.3, '#9b6bff'), (.7, '#d35bd0'), (1.1, '#ff4f8b'), (9, '#ffc23d')]
    neg_cols = [(-.3, '#3ee6c8'), (-.7, '#2fb3d6'), (-9, '#2f7fe0')]

    def f(x, z, t):
        w = 2 * math.pi * t / T
        a, b = 1.3 * math.cos(w), 1.3 * math.sin(w)
        return (math.sin(1.25 * x + w) * math.cos(1.25 * z)
                + (.7 + .5 * math.sin(2 * w)) * math.exp(-((x - a) ** 2 + (z - b) ** 2) / .5))

    scenes = []
    nf = int(T * FPS)
    for fi in range(nf):
        t = fi / FPS
        cam = Cam(-2 * math.pi * t / T + .5, math.radians(26), 28, 266, 90)
        objs, vol = [], 0.0
        for i in range(G):
            for j in range(G):
                cx, cz = -2.5 + cell * (i + .5), -2.5 + cell * (j + .5)
                v = f(cx, cz, t)
                vol += v * cell * cell
                h = .95 * v
                if h >= 0:
                    col = next(c for lim, c in pos_cols if h <= lim)
                else:
                    col = next(c for lim, c in neg_cols if h >= lim)
                y0, y1 = (0, max(h, .02)) if h >= 0 else (min(h, -.02), 0)
                objs.append(Obj((cx, 0, cz), box(cx - .2, cx + .2, y0, y1, cz - .2, cz + .2, rgb(col))))

        def pre(img, dr, cam):
            bands_img(dr, SW, SH, ['#0c1230', '#0e1636', '#101a3c', '#121e44'])
            for k in range(G + 1):
                c = -2.5 + k * cell
                for a, b_ in (((c, 0, -2.5), (c, 0, 2.5)), ((-2.5, 0, c), (2.5, 0, c))):
                    pa, pb = cam.proj(a), cam.proj(b_)
                    dr.line([pa[:2], pb[:2]], fill=rgb('#2c3c80'), width=1)
            # labels
            psprite(dr, S.INTEGRAL, 14, 30, 3, {'b': rgb('#4fb3ff')})
            psprite(dr, S.INTEGRAL, 36, 30, 3, {'b': rgb('#4fb3ff')})
            ptext(dr, 'SIN(X)COS(Y)', 14, 84, 2, rgb('#9fd8ff'))
            ptext(dr, '+ E^-R²', 14, 102, 2, rgb('#9fd8ff'))

        def post(img, dr, cam, vol=vol):
            ptext(dr, f'= {vol:+.2f}', 14, 124, 2, rgb(PAL['y']))
        scenes.append(render(objs, cam, (SW, SH), pre=pre, post=post))
    return scenes


# ═════════════════════════════════════════════════════════════════════════
# RUBISH: a real 3x3 cube; outer layers turn in 3D until the face spells HI
# ═════════════════════════════════════════════════════════════════════════
AX = {'x': 0, 'y': 1, 'z': 2}


def qrot(axis, sign):
    a = AX[axis]
    m = np.zeros((3, 3), dtype=int)
    m[a, a] = 1
    b, c = [k for k in range(3) if k != a]
    # right-handed quarter turn about `a`, sign = +1 / -1
    if a == 1:   # y: x,z plane
        m[0, 0], m[0, 2], m[2, 0], m[2, 2] = 0, sign, -sign, 0
    else:
        m[b, b], m[b, c], m[c, b], m[c, c] = 0, -sign, sign, 0
    return m


def arot(axis, ang):
    a = AX[axis]
    c, s = math.cos(ang), math.sin(ang)
    if a == 0:
        return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    if a == 1:
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


class Cube:
    def __init__(self):
        self.cubies = []
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                for z in (-1, 0, 1):
                    stick = [tuple(int(v) for v in n) for n in
                             ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
                             if np.dot(n, (x, y, z)) == 1]
                    self.cubies.append({'pos': np.array([x, y, z]), 'R': np.eye(3, dtype=int), 'st': stick})

    def copy(self):
        c = Cube.__new__(Cube)
        c.cubies = [{'pos': q['pos'].copy(), 'R': q['R'].copy(), 'st': q['st']} for q in self.cubies]
        return c

    def apply(self, mv):
        axis, layer, sign = mv
        Q = qrot(axis, sign)
        for q in self.cubies:
            if q['pos'][AX[axis]] == layer:
                q['pos'] = Q @ q['pos']
                q['R'] = Q @ q['R']

    def front(self):
        """{(row, col): slot} for the +z face; row 0 is the top."""
        out = {}
        for ci, q in enumerate(self.cubies):
            if q['pos'][2] != 1:
                continue
            for n in q['st']:
                if tuple(q['R'] @ np.array(n)) == (0, 0, 1):
                    out[(1 - q['pos'][1], q['pos'][0] + 1)] = (ci, n)
        return out


def rubish_plan(seed=21):
    rnd = random.Random(seed)
    LET = {'H': ["X.X", "XXX", "X.X"], 'I': ["XXX", ".X.", "XXX"]}

    def rmove(prev):
        while True:
            m = (rnd.choice('xyz'), rnd.choice((-1, 1)), rnd.choice((-1, 1)))
            if prev is None or m[0] != prev[0]:
                return m

    for attempt in range(5000):
        cube, seq, cons, marks = Cube(), [], {}, []
        prev = None
        for _ in range(4):
            m = rmove(prev); seq.append(m); cube.apply(m); prev = m
        ok = True
        for ch in 'HI':
            found = False
            for _ in range(400):
                seg, c2, pv = [], cube.copy(), prev
                for _ in range(rnd.choice((4, 5))):
                    m = rmove(pv); seg.append(m); c2.apply(m); pv = m
                new = {}
                for (r_, c_), slot in c2.front().items():
                    col = 'r' if LET[ch][r_][c_] == 'X' else 'w'
                    new[slot] = col
                if all(cons.get(sl, col) == col for sl, col in new.items()):
                    # avoid spelling the letter early inside the segment
                    cons.update(new)
                    seq += seg; cube = c2; prev = pv
                    marks.append((len(seq), ch))
                    found = True
                    break
            if not found:
                ok = False
                break
        if ok:
            return seq, cons, marks
    raise RuntimeError('no plan')


def rubish_scenes():
    seq, cons, marks = rubish_plan()
    rnd = random.Random(3)
    COL = {'w': '#f4f1ff', 'y': '#ffd23d', 'r': '#ff3d5a', 'o': '#ff8a3d', 'b': '#3d8bff', 'g': '#2fd38f'}
    base = Cube()
    color = {}
    for ci, q in enumerate(base.cubies):
        for n in q['st']:
            color[(ci, n)] = cons.get((ci, n)) or rnd.choice('wyrobggboy')

    # timeline: (kind, duration, move or None, word shown)
    MV, RW = .42, .15
    tl, word, k = [], '', 0
    tl.append(('hold', .5, None, ''))
    mark_at = dict(marks)
    for idx, m in enumerate(seq, 1):
        tl.append(('move', MV, m, word))
        if idx in mark_at:
            word += mark_at[idx]
            tl.append(('hold', 1.3 if word != 'HI' else 2.0, None, word))
    for m in reversed(seq):
        a, l, s = m
        tl.append(('move', RW, (a, l, -s), ''))
    T = sum(d for _, d, _, _ in tl)
    nf = int(round(T * FPS))

    moves_txt = "R U R' U' F2 L' D B2 U R2 F' L2 D' R U2 B' "
    from pixel import text_w
    tick_w = text_w(moves_txt, 2)

    cube = Cube()
    seg_i, seg_t0 = 0, 0.0
    scenes = []
    for fi in range(nf):
        t = fi / FPS
        while seg_i < len(tl) - 1 and t >= seg_t0 + tl[seg_i][1]:
            kind, d, m, _ = tl[seg_i]
            if kind == 'move':
                cube.apply(m)
            seg_t0 += d
            seg_i += 1
        kind, d, m, word = tl[seg_i]
        prog = min(1.0, (t - seg_t0) / d)
        e = prog * prog * (3 - 2 * prog)
        A_layer = None
        if kind == 'move':
            axis, layer, sign = m
            A_layer = (axis, layer, arot(axis, sign * e * math.pi / 2))
        wob = 2 * math.pi * t / T
        cam = Cam(.45 + .14 * math.sin(wob), .42 + .05 * math.sin(2 * wob), 24, 262, 74)
        objs = []
        for ci, q in enumerate(cube.cubies):
            A = np.eye(3)
            if A_layer and q['pos'][AX[A_layer[0]]] == A_layer[1]:
                A = A_layer[2]
            c = tuple(A @ q['pos'])
            ax, ay, az = (tuple(A @ v) for v in np.eye(3))
            faces = oriented_box(c, ax, ay, az, .485, rgb('#0b0a14'))
            for n in q['st']:
                nw = A @ (q['R'] @ np.array(n))
                nw = tuple(nw)
                # tangent axes for the sticker quad
                tang = [v for v in (ax, ay, az) if abs(np.dot(v, nw)) < .5]
                u, v = tang
                fc = add(c, mul(nw, .495))
                h = .41
                pts = [add(add(fc, mul(u, -h)), mul(v, -h)), add(add(fc, mul(u, h)), mul(v, -h)),
                       add(add(fc, mul(u, h)), mul(v, h)), add(add(fc, mul(u, -h)), mul(v, h))]
                faces.append(Face(pts, nw, rgb(COL[color[(ci, n)]])))
            objs.append(Obj(c, faces))

        def pre(img, dr, cam, word=word, t=t):
            bands_img(dr, SW, SH, ['#18122a', '#1c142e', '#211631', '#271934'])
            # shadow
            dr.ellipse([200, 140 - 6, 324, 140], fill=(14, 10, 24))
            dr.rectangle([0, 141, SW, SH], fill=(20, 15, 34))
            off = (t / T) * tick_w * 2 % tick_w
            ptext(dr, moves_txt * 3, 8 - off, 149, 2, rgb('#8f86c0'))
            ptext(dr, '> ' + word + ('_' if int(t * 2.5) % 2 else ' '), 22, 60, 3, rgb(PAL['m']))
        scenes.append(render(objs, cam, (SW, SH), pre=pre))
    return scenes


if __name__ == '__main__':
    which = sys.argv[1:] or ['rubish', 'town-trial', 'multivis']
    for key in which:
        sc = {'rubish': rubish_scenes, 'town-trial': town_scenes, 'multivis': multivis_scenes}[key]()
        save_gif(key, sc, int(1000 / FPS))
