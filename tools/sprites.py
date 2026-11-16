"""Pixel sprites shared across hero, tiles and footer (palette keys from pixel.PAL)."""

DUMPLING = [
    "......kk......",
    ".....kwwk.....",
    "...kkwtwwkk...",
    "..kwwtwwtwwk..",
    ".kwwwwwwwwwwk.",
    "kwwwwwwwwwwwwk",
    "kwwwkwwwwkwwwk",
    "kwwpwwkkwwpwwk",
    "kwwwwwwwwwwwwk",
    ".ktwwwwwwwwtk.",
    "..kkkkkkkkkk..",
]

HOUSE = [
    ".....kk.....",
    "....kppk....",
    "...kppppk...",
    "..kppppppk..",
    ".kppppppppk.",
    "kkkkkkkkkkkk",
    ".kwwwwwwwwk.",
    ".kwbbwwbbwk.",
    ".kwbbwwbbwk.",
    ".kwwwoowwwk.",
    ".kwwwooywwk.",
    ".kkkkkkkkkk.",
]

BUILDING = [
    ".kkkkkkkk.",
    ".kvvvvvvk.",
    ".kvyvvyvk.",
    ".kvvvvvvk.",
    ".kvyvvyvk.",
    ".kvvvvvvk.",
    ".kvvkkvvk.",
    ".kvvkkvvk.",
    "kkkkkkkkkk",
]

THERMO = [
    "..kk..",
    ".kwwk.",
    ".kwwk.",
    ".kwwk.",
    ".krrk.",
    ".krrk.",
    ".krrk.",
    ".krrk.",
    "krrrrk",
    "krwrrk",
    "krrrrk",
    ".kkkk.",
]

INTEGRAL = [
    ".....bbb",
    "....b...",
    "....b...",
    "....b...",
    "...bb...",
    "...b....",
    "...b....",
    "...b....",
    "...b....",
    "..bb....",
    "..b.....",
    "..b.....",
    "..b.....",
    "bbb.....",
]

ROBOT = [
    "....kk....",
    "....yk....",
    ".kkkkkkkk.",
    ".kssssssk.",
    ".ksmssmsk.",
    ".kssssssk.",
    ".kskkkksk.",
    ".kkkkkkkk.",
    "..kbbbbk..",
    "..kbbbbk..",
    "..kk..kk..",
]

PHONE = [
    "kkkkkkkkk",
    "kGGGGGGGk",
    "kGdddddGk",
    "kGdddddGk",
    "kGdddddGk",
    "kGdddddGk",
    "kGdddddGk",
    "kGdddddGk",
    "kGdddddGk",
    "kGdddddGk",
    "kGGGGGGGk",
    "kGGGsGGGk",
    "kkkkkkkkk",
]

PIZZA = ["ooooo", "yryry", ".yyy.", "..y.."]
SUSHI = [".kkk.", "kwpwk", "kwwwk", ".kkk."]
TACO = ["..yy.", ".ymmy", "yymmy", "yyyy."]
NOODLE = ["w.w.w", "w.w.w", "rrrrr", ".rrr."]

HEART = [".p.p.", "ppppp", "ppppp", ".ppp.", "..p.."]

PIN = [
    "..kkk..",
    ".krrrk.",
    "krrwrrk",
    "krwwwrk",
    "krrwrrk",
    ".krrrk.",
    ".krrrk.",
    "..krk..",
    "..krk..",
    "...k...",
]

MEDAL = [
    "kkk....kkk",
    "kaak..kcck",
    ".kaakkcck.",
    "..kaacck..",
    "..kkkkkk..",
    ".kLLLLLLk.",
    "kLLWLLLLMk",
    "kLWLLLLLMk",
    "kLLLLLLLMk",
    "kLLLLLLMMk",
    "kLLLLLLMDk",
    ".kLMMMMDk.",
    "..kDDDDk..",
    "...kkkk...",
]
DIGITS = {'2': ["DDD", "..D", "DDD", "D..", "DDD"], '4': ["D.D", "D.D", "DDD", "..D", "..D"]}


def medal(digit):
    rows = [list(r) for r in MEDAL]
    for ri, dr in enumerate(DIGITS[digit]):
        for ci, ch in enumerate(dr):
            if ch == 'D':
                rows[6 + ri][4 + ci] = 'D'
    return [''.join(r) for r in rows]


SILVER = {'L': '#e4e6f2', 'M': '#a9adc8', 'D': '#6c7096', 'W': '#ffffff', 'a': '#ff4f8b', 'c': '#4fb3ff'}
VIOLET = {'L': '#c4adff', 'M': '#8a63f0', 'D': '#5a3bb8', 'W': '#efe8ff', 'a': '#3ee6a8', 'c': '#ffc23d'}

CHECK = [
    "..mmmmm..",
    ".mmmmmmm.",
    "mmmmmmmkm",
    "mmmmmmkmm",
    "mkmmmkmmm",
    "mmkmkmmmm",
    "mmmkmmmmm",
    ".mmmmmmm.",
    "..mmmmm..",
]

ARROW_DOWN = [
    "..mmm..",
    "..mmm..",
    "..mmm..",
    "mmmmmmm",
    ".mmmmm.",
    "..mmm..",
    "...m...",
]

SPARK = ["..w..", "..w..", "ww.ww", "..w..", "..w.."]

PERSON = [".w.", "www", ".w.", "w.w"]


def cube_face(colors3x3):
    """13x13 front-facing cube sprite from 3x3 colour keys."""
    rows = []
    for r in range(13):
        if r % 4 == 0:
            rows.append('k' * 13)
            continue
        line = ''
        for c in range(13):
            line += 'k' if c % 4 == 0 else colors3x3[r // 4][c // 4]
        rows.append(line)
    return rows


CUBE = cube_face(["rwb", "ymo", "brw"])
