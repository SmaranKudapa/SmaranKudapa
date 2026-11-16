"""Smooth, eased scenes for rubish, Multivis and Town Trial."""
import math
import random

from pixel import PAL, INK, text, text_w, sprite, rect, poly, bands, iso_cube, frames_css, panel_path

TW_, SCENE_H = 800, 330
w, y, p, m, b = PAL['w'], PAL['y'], PAL['p'], PAL['m'], PAL['b']


def win_css(cls, t0, t1, T):
    """Visible only during [t0, t1) of a T-second loop."""
    a, b_ = 100 * t0 / T, 100 * t1 / T
    return (f".{cls}{{opacity:0;animation:{cls} {T:.3f}s steps(1) infinite}}"
            f"@keyframes {cls}{{0%{{opacity:0}}{a:.3f}%{{opacity:1}}{b_:.3f}%{{opacity:0}}100%{{opacity:0}}}}")


def slide_css(cls, t0, t1, T, dx, dy):
    a, b_ = 100 * t0 / T, 100 * t1 / T
    return (f".{cls}{{animation:{cls} {T:.3f}s linear infinite}}"
            f"@keyframes {cls}{{0%,{a:.3f}%{{transform:translate(0px,0px);animation-timing-function:cubic-bezier(.6,0,.3,1)}}"
            f"{b_:.3f}%,100%{{transform:translate({dx}px,{dy}px)}}}}")


# ══════════════════════════════════════════════════════════════════════════
# RUBISH: rows/columns turn in, scrambling, then resolving into letters
# ══════════════════════════════════════════════════════════════════════════
def scene_rubish():
    s, css = bands(0, 0, TW_, SCENE_H, ['#18122a', '#1c142e', '#211631', '#271934']), ''
    cols = {'w': '#f4f1ff', 'y': '#ffd23d', 'r': '#ff3d5a', 'o': '#ff8a3d', 'b': '#3d8bff', 'g': '#2fd38f'}
    st, gap = 34, 6
    face = 3 * st + 4 * gap
    D = 3 * (st + gap)
    fx, fy, depth = 470 - face // 2, 104, 44
    sk = lambda x, y_, t: (x + t, y_ - t)
    rnd = random.Random(9)

    L = {'H': ["X.X", "XXX", "X.X"], 'I': ["XXX", ".X.", "XXX"], 'C': ["XXX", "X..", "XXX"],
         'O': ["XXX", "X.X", "XXX"], 'L': ["X..", "X..", "XXX"]}
    letter = lambda ch: [['r' if L[ch][r][c] == 'X' else 'w' for c in range(3)] for r in range(3)]
    rand_line = lambda: [rnd.choice('wyrobg') for _ in range(3)]

    state = [rand_line() for _ in range(3)]
    phases = []  # (kind, dur, state_before, axis, idx, incoming, word)
    MOVE, HOLD = .34, .05

    def move(axis, idx, incoming, word):
        nonlocal state
        phases.append(('move', MOVE, [r[:] for r in state], axis, idx, incoming, word))
        if axis == 'row':
            state[idx] = incoming[:]
        else:
            for r in range(3):
                state[r][idx] = incoming[r]
        phases.append(('hold', HOLD, [r[:] for r in state], None, None, None, word))

    def hold(dur, word):
        phases.append(('hold', dur, [r[:] for r in state], None, None, None, word))

    def scramble(n, word):
        for _ in range(n):
            ax = rnd.choice(['row', 'col'])
            move(ax, rnd.randrange(3), rand_line(), word)

    for wi, word in enumerate(['HI', 'COOL']):
        scramble(4, '')
        for li, ch in enumerate(word):
            tgt = letter(ch)
            shown = word[:li + 1]
            axis = 'row' if (li + wi) % 2 == 0 else 'col'
            for k in range(3):
                inc = tgt[k] if axis == 'row' else [tgt[r][k] for r in range(3)]
                cur = state[k] if axis == 'row' else [state[r][k] for r in range(3)]
                if inc != cur:
                    move(axis, k, inc, shown)
            hold(.9 if li < len(word) - 1 else 1.6, shown)

    T = sum(ph[1] for ph in phases)

    def sticker(x, y_, c):
        return rect(x, y_, st, st, cols[c]) + rect(x + 4, y_ + 4, 8, 4, '#ffffff', ' opacity=".5"')

    pos = lambda r, c: (fx + gap + c * (st + gap), fy + gap + r * (st + gap))

    # cube body (top + right faces), floating
    body = poly([(fx, fy), sk(fx, fy, depth), sk(fx + face, fy, depth), (fx + face, fy)], INK)
    body += poly([(fx + face, fy), sk(fx + face, fy, depth), sk(fx + face, fy + face, depth), (fx + face, fy + face)], INK)
    body += rect(fx, fy, face, face, INK)
    for a in range(3):
        for c in range(3):
            t0 = gap * .5 + a * (depth - gap) / 3 + gap / 2
            t1 = t0 + (depth - 2 * gap) / 3
            x0 = fx + gap + c * (st + gap)
            body += poly([sk(x0, fy, t0), sk(x0 + st, fy, t0), sk(x0 + st, fy, t1), sk(x0, fy, t1)],
                         cols['y' if (a + c) % 4 else 'o'])
            y0 = fy + gap + c * (st + gap)
            body += poly([sk(fx + face, y0, t0), sk(fx + face, y0, t1), sk(fx + face, y0 + st, t1), sk(fx + face, y0 + st, t0)],
                         cols['b' if (a * 3 + c) % 3 else 'g'])

    front = ''
    t = 0.0
    words_txt = ''
    for n, (kind, dur, stt, axis, idx, inc, word) in enumerate(phases):
        g = ''
        if kind == 'hold':
            for r in range(3):
                for c in range(3):
                    g += sticker(*pos(r, c), stt[r][c])
        else:
            mv = ''
            for r in range(3):
                for c in range(3):
                    moving = (axis == 'row' and r == idx) or (axis == 'col' and c == idx)
                    (mv if moving else None) if False else None
                    if moving:
                        mv += sticker(*pos(r, c), stt[r][c])
                    else:
                        g += sticker(*pos(r, c), stt[r][c])
            for k in range(3):
                if axis == 'row':
                    x_, y_ = pos(idx, k)
                    mv += sticker(x_ + D, y_, inc[k])
                else:
                    x_, y_ = pos(k, idx)
                    mv += sticker(x_, y_ + D, inc[k])
            dx, dy = (-D, 0) if axis == 'row' else (0, -D)
            g += f'<g clip-path="url(#cf)"><g class="sl{n}">{mv}</g></g>'
            css += slide_css(f'sl{n}', t, t + dur, T, dx, dy)
        front += f'<g class="ph{n}">{g}</g>'
        css += win_css(f'ph{n}', t, t + dur, T)
        t += dur

    # typed word, one window per run of equal words
    t, start, cur = 0.0, 0.0, phases[0][6]
    k = 0
    for kind, dur, *_rest in phases + [('end', 0, None, None, None, None, None)]:
        word = _rest[-1] if kind != 'end' else None
        if word != cur or kind == 'end':
            s_txt = text('> ' + cur + '_', 70, 150, 5, m)
            words_txt += f'<g class="wd{k}">{s_txt}</g>'
            css += win_css(f'wd{k}', start, t, T)
            k += 1
            start, cur = t, word
        t += dur

    defs = f'<clipPath id="cf"><rect x="{fx + 3}" y="{fy + 3}" width="{face - 6}" height="{face - 6}"/></clipPath>'
    s += f'<rect class="shd" x="{fx + 10}" y="{fy + face + 26}" width="{face + 20}" height="8" fill="#0e0a18"/>'
    s += f'<g class="flt">{body}{front}</g>'
    s += words_txt
    css += (".flt{animation:flt 3.2s ease-in-out infinite}"
            "@keyframes flt{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}"
            ".shd{transform-box:fill-box;transform-origin:center;animation:shd 3.2s ease-in-out infinite}"
            "@keyframes shd{0%,100%{transform:scaleX(1)}50%{transform:scaleX(.85)}}")
    # move notation ticker (smooth)
    moves = "R U R' U' F2 L' D B2 U R2 F' L2 D' R U2 B' "
    tw_ = text_w(moves, 3)
    s += rect(0, 282, TW_, 48, '#140f22')
    s += f'<g class="tick">{text(moves * 2, 20, 296, 3, "#8f86c0")}</g>'
    css += (f".tick{{animation:tick 14s linear infinite}}"
            f"@keyframes tick{{0%{{transform:translateX(0)}}100%{{transform:translateX(-{tw_ + 12}px)}}}}")
    return s, css, defs


# ══════════════════════════════════════════════════════════════════════════
# MULTIVIS: a smooth travelling wave across iso columns
# ══════════════════════════════════════════════════════════════════════════
def scene_multivis():
    s, css = bands(0, 0, TW_, SCENE_H, ['#0c1230', '#0e1636', '#101a3c', '#121e44']), ''
    ox, oy, TW, TH, N = 480, 176, 22, 11, 6
    P = lambda i, j: (ox + (i - j) * TW, oy + (i + j) * TH)
    s += poly([P(0, 0), P(N, 0), P(N, N), P(0, N)], '#1a2556')
    for i in range(N + 1):
        a, b_ = P(i, 0), P(i, N)
        s += f'<line x1="{a[0]}" y1="{a[1]}" x2="{b_[0]}" y2="{b_[1]}" stroke="#2c3c80" stroke-width="2"/>'
        a, b_ = P(0, i), P(N, i)
        s += f'<line x1="{a[0]}" y1="{a[1]}" x2="{b_[0]}" y2="{b_[1]}" stroke="#2c3c80" stroke-width="2"/>'
    zx, zy = P(0, 0)
    s += rect(zx - 2, zy - 132, 4, 132, '#c8c4e4') + poly([(zx - 8, zy - 132), (zx + 8, zy - 132), (zx, zy - 146)], '#c8c4e4')

    tiers = [(44, ('#9fd8ff', '#4fb3ff', '#2f7fc4')), (64, ('#b8c2ff', '#7d8cff', '#5161d6')),
             (88, ('#c4adff', '#9b6bff', '#6a45c8')), (112, ('#ffa3c2', '#ff4f8b', '#c42e64'))]
    LO, PER = .28, 2.6
    for k, (hm, _) in enumerate(tiers):
        css += (f".cs{k}{{transform-box:fill-box;transform-origin:50% 100%;animation:cs{k} {PER}s ease-in-out infinite}}"
                f"@keyframes cs{k}{{0%,100%{{transform:scaleY({LO})}}50%{{transform:scaleY(1)}}}}"
                f".ct{k}{{animation:ct{k} {PER}s ease-in-out infinite}}"
                f"@keyframes ct{k}{{0%,100%{{transform:translateY({-LO * hm:.1f}px)}}50%{{transform:translateY({-hm}px)}}}}")
    inset, ang = .86, math.degrees(math.atan(TH / TW))
    used = set()
    for d in range(2 * N - 1):
        for i in range(N):
            j = d - i
            if not 0 <= j < N:
                continue
            dist = ((i - 2.5) ** 2 + (j - 2.5) ** 2) / 6.25
            k = min(3, int(4 * math.exp(-dist * .8)))
            hm, (top, lft, rgt) = tiers[k]
            x, y_ = P(i, j)
            cx, cy = x, y_ + TH
            Lp, Bp = (cx - TW * inset, cy), (cx, cy + TH * inset)
            Rp, Tp = (cx + TW * inset, cy), (cx, cy - TH * inset)
            wd = TW * inset
            rr = round(math.hypot(i - 2.5, j - 2.5) * 2)
            dl = f'dl{rr}'
            used.add(rr)
            s += (f'<g transform="translate({Lp[0]:g} {Lp[1]:g}) skewY({ang:.3f})">'
                  f'<rect class="cs{k} {dl}" x="0" y="{-hm}" width="{wd:g}" height="{hm}" fill="{lft}"/></g>')
            s += (f'<g transform="translate({Bp[0]:g} {Bp[1]:g}) skewY({-ang:.3f})">'
                  f'<rect class="cs{k} {dl}" x="0" y="{-hm}" width="{wd:g}" height="{hm}" fill="{rgt}"/></g>')
            s += f'<g class="ct{k} {dl}">{poly([Tp, Rp, Bp, Lp], top)}</g>'
    css += ''.join(f".dl{n}{{animation-delay:{n * .16 - 2 * PER:.2f}s}}" for n in sorted(used))

    from sprites import INTEGRAL
    s += sprite(INTEGRAL, 86, 92, 9) + sprite(INTEGRAL, 140, 92, 9)
    s += text('DXDY', 210, 196, 5, '#9fd8ff')
    return s, css


# ══════════════════════════════════════════════════════════════════════════
# TOWN TRIAL: turntable spin between four views; agents walk in, through, out
# ══════════════════════════════════════════════════════════════════════════
PERSON_A = [".kkk.", ".kwk.", "kkkkk", "kccck", "kccck", ".kkk.", ".k.k.", ".k.k."]
PERSON_B = [".kkk.", ".kwk.", "kkkkk", "kccck", "kccck", ".kkk.", ".k.k.", "k...k"]


def scene_town():
    s, css = bands(0, 0, TW_, SCENE_H, ['#0f1424', '#111a2a', '#132230', '#142a30']), ''
    ox, oy, TW, TH, N = 400, 56, 44, 22, 5
    P = lambda i, j: (ox + (i - j) * TW, oy + (i + j) * TH)
    road = lambda i, j: i == 2 or j == 2
    rnd = random.Random(4)
    diamond = lambda x, y_: [(x, y_), (x + TW, y_ + TH), (x, y_ + 2 * TH), (x - TW, y_ + TH)]

    g = ''
    # paths leading out of town
    for (i, j, op) in [(-2, 2, .3), (-1, 2, .65), (5, 2, .65), (6, 2, .3), (2, -2, .3), (2, -1, .65), (2, 5, .65), (2, 6, .3)]:
        g += poly(diamond(*P(i, j)), '#2b2f48', f' opacity="{op}"')
    # board
    for d in range(2 * N - 1):
        for i in range(N):
            j = d - i
            if 0 <= j < N:
                col = '#2b2f48' if road(i, j) else ('#1f6b52' if (i + j) % 2 else '#24795c')
                g += poly(diamond(*P(i, j)), col)
    L0, B0, R0 = P(0, N), P(N, N), P(N, 0)
    g += poly([L0, B0, (B0[0], B0[1] + 18), (L0[0], L0[1] + 18)], '#14473a')
    g += poly([B0, R0, (R0[0], R0[1] + 18), (B0[0], B0[1] + 18)], '#0e3329')
    for i in range(N):  # lane dashes
        for (a, c) in [(i, 2), (2, i)]:
            if (a, c) != (2, 2):
                x, y_ = P(a, c)
                g += rect(x - 2, y_ + TH - 1, 4, 2, '#5b6088')

    # base layout, then four rotated views
    palettes = [('#c4adff', '#9b6bff', '#6a45c8'), ('#9fd8ff', '#4fb3ff', '#2f7fc4'),
                ('#ffd98a', '#ffc23d', '#c98d1c'), ('#ffa3c2', '#ff4f8b', '#c42e64'),
                ('#e8e4ff', '#c8c4e4', '#8a86a8')]
    base = {}
    for i in range(N):
        for j in range(N):
            if road(i, j):
                continue
            if (i, j) == (4, 0):
                base[(i, j)] = ('flag', 84, palettes[2])
            elif rnd.random() < .7:
                base[(i, j)] = ('bld', rnd.choice([22, 34, 46, 58, 66]), rnd.choice(palettes))
            else:
                base[(i, j)] = ('tree', 0, None)
    rot = lambda i, j: (N - 1 - j, i)
    VIEW, NV = 4.0, 4
    T = VIEW * NV
    win = 0
    for v in range(NV):
        lay = {}
        for (i, j), val in base.items():
            a, c = i, j
            for _ in range(v):
                a, c = rot(a, c)
            lay[(a, c)] = val
        vg = ''
        for d in range(2 * N - 1):
            for i in range(N):
                j = d - i
                if (i, j) not in lay:
                    continue
                kind, h, pal = lay[(i, j)]
                x, y_ = P(i, j)
                if kind == 'tree':
                    vg += rect(x - 4, y_ + 10, 8, 14, '#5a3a22') + rect(x - 13, y_ - 8, 26, 20, m) + rect(x - 13, y_ - 8, 26, 5, '#8affd0')
                    continue
                cube, (Lp, Bp, Rp, Tp) = iso_cube(x, y_, TW, TH, h, *pal)
                vg += cube
                for row in range(h // 14):
                    for tt in (.35, .7):
                        wx = Lp[0] + tt * (Bp[0] - Lp[0])
                        wy = Lp[1] + tt * (Bp[1] - Lp[1]) - 10 - row * 14
                        cls = f' class="tw st{win % 4}"' if win % 3 == 0 else ''
                        vg += rect(round(wx) - 2, round(wy) - 3, 4, 6, '#fff1b0', cls)
                        win += 1
                if kind == 'flag':
                    fx_, fy_ = Tp[0], Tp[1] - h
                    vg += rect(fx_, fy_ - 40, 4, 40, w)
                    vg += f'<g class="fl fl0">{rect(fx_ + 4, fy_ - 40, 24, 14, p)}</g>'
                    vg += f'<g class="fl fl1">{rect(fx_ + 4, fy_ - 38, 24, 12, p)}{rect(fx_ + 20, fy_ - 40, 8, 4, p)}</g>'
        g += f'<g class="vw{v}">{vg}</g>'
        css += win_css(f'vw{v}', v * VIEW, (v + 1) * VIEW, T)
    css += frames_css('fl', 2, .6)
    css += ''.join(f".st{i}{{animation-delay:{-i * .6:.1f}s}}" for i in range(4))

    # agents: walk in from outside, through town, out the other side (or into town)
    C = lambda i, j: (P(i, j)[0], P(i, j)[1] + TH)
    routes = [
        ([(-2.6, 2), (6.6, 2)], m, 10, 0, 'through'),
        ([(6.6, 2), (-2.6, 2)], y, 10, -5, 'through'),
        ([(2, -2.6), (2, 6.6)], b, 11, -2, 'through'),
        ([(2, 6.6), (2, -2.6)], p, 11, -7.5, 'through'),
        ([(-2.6, 2), (2, 2), (2, 0.6)], w, 8, -3, 'in'),
        ([(2, 3.6), (2, 2), (6.6, 2)], '#ffa3c2', 8, -6, 'out'),
    ]
    agents = ''
    for n_, (pts, col, dur, dl, kind) in enumerate(routes):
        sp = [C(*q) for q in pts]
        segs = [math.dist(sp[k], sp[k + 1]) for k in range(len(sp) - 1)]
        tot = sum(segs)
        kf, acc = [], 0
        for k, q in enumerate(sp):
            pct = 100 * acc / tot
            op = 1
            if kind in ('through', 'in') and k == 0 or kind in ('through', 'out') and k == len(sp) - 1:
                op = 0
            kf.append((pct, q, op))
            if k < len(segs):
                acc += segs[k]
        frames = ''
        for k, (pct, q, op) in enumerate(kf):
            frames += f"{pct:.2f}%{{transform:translate({q[0]:.1f}px,{q[1]:.1f}px);opacity:{op}}}"
        # fade quickly near the ends instead of across the whole first leg
        if kind in ('through', 'in'):
            q = (sp[0][0] + (sp[1][0] - sp[0][0]) * .08 * tot / segs[0] * 0 + (sp[1][0] - sp[0][0]) * (40 / segs[0]),
                 sp[0][1] + (sp[1][1] - sp[0][1]) * (40 / segs[0]))
            frames += f"{100 * 40 / tot:.2f}%{{transform:translate({q[0]:.1f}px,{q[1]:.1f}px);opacity:1}}"
        if kind in ('through', 'out'):
            a_, b_ = sp[-2], sp[-1]
            q = (b_[0] - (b_[0] - a_[0]) * (40 / segs[-1]), b_[1] - (b_[1] - a_[1]) * (40 / segs[-1]))
            frames += f"{100 - 100 * 40 / tot:.2f}%{{transform:translate({q[0]:.1f}px,{q[1]:.1f}px);opacity:1}}"
        if kind == 'in':  # fade into the building at the end
            a_, b_ = sp[-2], sp[-1]
            q = (b_[0] - (b_[0] - a_[0]) * (16 / segs[-1]), b_[1] - (b_[1] - a_[1]) * (16 / segs[-1]))
            frames += f"{100 - 100 * 16 / tot:.2f}%{{transform:translate({q[0]:.1f}px,{q[1]:.1f}px);opacity:1}}"
            frames = frames.replace(f"100.00%{{transform:translate({sp[-1][0]:.1f}px,{sp[-1][1]:.1f}px);opacity:1}}",
                                    f"100.00%{{transform:translate({sp[-1][0]:.1f}px,{sp[-1][1]:.1f}px);opacity:0}}")
        if kind == 'out':  # step out of the building at the start
            frames = frames.replace(f"0.00%{{transform:translate({sp[0][0]:.1f}px,{sp[0][1]:.1f}px);opacity:1}}",
                                    f"0.00%{{transform:translate({sp[0][0]:.1f}px,{sp[0][1]:.1f}px);opacity:0}}")
            a_, b_ = sp[0], sp[1]
            q = (a_[0] + (b_[0] - a_[0]) * (16 / segs[0]), a_[1] + (b_[1] - a_[1]) * (16 / segs[0]))
            frames += f"{100 * 16 / tot:.2f}%{{transform:translate({q[0]:.1f}px,{q[1]:.1f}px);opacity:1}}"
        css += (f".ag{n_}{{animation:ag{n_} {dur}s linear infinite;animation-delay:{dl}s}}"
                f"@keyframes ag{n_}{{{frames}}}")
        pa = sprite(PERSON_A, -10, -31, 4, {'c': col})
        pb = sprite(PERSON_B, -10, -31, 4, {'c': col})
        agents += (f'<g class="ag{n_}"><rect x="-10" y="-2" width="20" height="5" fill="#0b0a14" opacity=".35"/>'
                   f'<g class="lg lg0">{pa}</g><g class="lg lg1">{pb}</g></g>')
    css += frames_css('lg', 2, .4)
    g += agents

    s += f'<g class="spin">{g}</g>'
    css += (f".spin{{transform-origin:{ox}px 180px;animation:spin {VIEW}s ease-in-out infinite}}"
            "@keyframes spin{0%{transform:scaleX(.02)}10%{transform:scaleX(1)}90%{transform:scaleX(1)}100%{transform:scaleX(.02)}}")
    return s, css
