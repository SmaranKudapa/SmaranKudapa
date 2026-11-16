"""Tiny flat-shaded 3D renderer for pixel-art GIF tiles.

Orthographic camera with yaw (turntable) + pitch, painter's algorithm per
object, back-face culling, 4-level quantized lighting fixed to the camera
(so faces brighten and darken as they turn), rendered without antialiasing
at half resolution and upscaled 2x for chunky pixels.
"""
import math
from PIL import Image, ImageDraw

from pixel import glyph


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def shade(c, k):
    return tuple(max(0, min(255, round(v * k))) for v in c)


LIGHT = (-0.45, 0.8, 0.4)
_n = math.sqrt(sum(v * v for v in LIGHT))
LIGHT = tuple(v / _n for v in LIGHT)
LEVELS = (0.58, 0.72, 0.86, 1.0)


class Cam:
    def __init__(self, yaw, pitch, scale, cx, cy):
        self.c, self.s = math.cos(yaw), math.sin(yaw)
        self.cp, self.sp = math.cos(pitch), math.sin(pitch)
        self.k, self.cx, self.cy = scale, cx, cy

    def rot(self, p):
        x, y, z = p
        return x * self.c - z * self.s, y, x * self.s + z * self.c

    def proj(self, p):
        x1, y, z1 = self.rot(p)
        return (self.cx + self.k * x1, self.cy + self.k * (z1 * self.sp - y * self.cp),
                z1 * self.cp + y * self.sp)

    def facing(self, n):
        x1, y, z1 = self.rot(n)
        return y * self.sp + z1 * self.cp

    def lit(self, col, n):
        x1, y, z1 = self.rot(n)
        d = max(0.0, x1 * LIGHT[0] + y * LIGHT[1] + z1 * LIGHT[2])
        return shade(col, LEVELS[min(3, int(d * 4))])


class Face:
    __slots__ = ('pts', 'n', 'col', 'deco', 'cull', 'flat')

    def __init__(self, pts, n, col, deco=None, cull=True, flat=False):
        self.pts, self.n, self.col = pts, n, col
        self.deco = deco or []   # [(pts3d, rgb)] drawn on top, unshaded
        self.cull, self.flat = cull, flat


class Obj:
    """A group drawn as one unit, sorted by the depth of `anchor`."""

    def __init__(self, anchor, faces=None, sprite=None, bias=0.0):
        self.anchor, self.faces, self.sprite, self.bias = anchor, faces or [], sprite, bias


def add(a, b): return (a[0] + b[0], a[1] + b[1], a[2] + b[2])
def mul(a, k): return (a[0] * k, a[1] * k, a[2] * k)


def box(x0, x1, y0, y1, z0, z1, col, top=None, bottom=True):
    f = [Face([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], (0, 1, 0), top or col),
         Face([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], (0, 0, 1), col),
         Face([(x1, y0, z0), (x0, y0, z0), (x0, y1, z0), (x1, y1, z0)], (0, 0, -1), col),
         Face([(x1, y0, z1), (x1, y0, z0), (x1, y1, z0), (x1, y1, z1)], (1, 0, 0), col),
         Face([(x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0)], (-1, 0, 0), col)]
    if bottom:
        f.append(Face([(x0, y0, z1), (x1, y0, z1), (x1, y0, z0), (x0, y0, z0)], (0, -1, 0), col))
    return f


def oriented_box(c, ax, ay, az, h, col, faces_col=None):
    """Box centred on c with unit axes ax, ay, az and half-size h."""
    out = []
    for axis, s in ((ax, 1), (ax, -1), (ay, 1), (ay, -1), (az, 1), (az, -1)):
        n = mul(axis, s)
        others = [a for a in (ax, ay, az) if a is not axis]
        u, v = others
        fc = add(c, mul(n, h))
        pts = [add(add(fc, mul(u, -h)), mul(v, -h)), add(add(fc, mul(u, h)), mul(v, -h)),
               add(add(fc, mul(u, h)), mul(v, h)), add(add(fc, mul(u, -h)), mul(v, h))]
        out.append(Face(pts, n, col))
    return out


def face_point(face_pts, a, b):
    p0, p1, _, p3 = face_pts
    return tuple(p0[i] + a * (p1[i] - p0[i]) + b * (p3[i] - p0[i]) for i in range(3))


def render(objs, cam, size, bg=None, pre=None, post=None):
    img = Image.new('RGB', size, bg or (0, 0, 0))
    dr = ImageDraw.Draw(img)
    if pre:
        pre(img, dr, cam)
    order = sorted(objs, key=lambda o: cam.proj(o.anchor)[2] + o.bias)
    for o in order:
        vis = []
        for f in o.faces:
            if f.cull and cam.facing(f.n) <= 1e-6:
                continue
            pp = [cam.proj(p) for p in f.pts]
            vis.append((sum(q[2] for q in pp) / len(pp), f, pp))
        vis.sort(key=lambda t: t[0])
        for _, f, pp in vis:
            col = f.col if f.flat else cam.lit(f.col, f.n)
            dr.polygon([(q[0], q[1]) for q in pp], fill=col)
            for dpts, dcol in f.deco:
                dr.polygon([cam.proj(p)[:2] for p in dpts], fill=dcol)
        if o.sprite:
            u, v, _ = cam.proj(o.anchor)
            o.sprite(img, dr, round(u), round(v))
    if post:
        post(img, dr, cam)
    return img


def ptext(dr, s, x, y, px, col, sp=1):
    cx = round(x)
    for ch in s.upper():
        rows = glyph(ch)
        for ri, row in enumerate(rows):
            for ci, c in enumerate(row):
                if c == '#':
                    dr.rectangle([cx + ci * px, y + ri * px, cx + ci * px + px - 1, y + ri * px + px - 1], fill=col)
        cx += (len(rows[0]) + sp) * px


def psprite(dr, rows, x, y, px, pal):
    for ri, row in enumerate(rows):
        for ci, c in enumerate(row):
            if c != '.':
                dr.rectangle([x + ci * px, y + ri * px, x + ci * px + px - 1, y + ri * px + px - 1], fill=pal[c])


def bands_img(dr, w, h, cols):
    n = len(cols)
    for i, c in enumerate(cols):
        dr.rectangle([0, round(h * i / n), w, round(h * (i + 1) / n)], fill=rgb(c))
