#!/usr/bin/env python3
"""Social buttons for the README: a pixel frame with a logo image (tools/logos/,
supplied by Smaran) composited on top, saved as one PNG per button so each can
carry its own link. A transparent strip under each square gives the vertical gap
when they are stacked beside the banner.

    python3 tools/build_social.py
"""
import asyncio, os
from PIL import Image
from trial_assets import social_button, FRAME_ACCENT, SOCIAL

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, '..', 'assets'))
TMP = '/tmp/social_build'
SIZE, GAP = 512, 12                          # 2x of the 256px design; GAP split above/below (GitHub adds ~5px line spacing too)
LOGO_W = {'linkedin': .56, 'youtube': .64, 'x': .54}


async def shoot(paths):
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        br = await pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = await br.new_page(viewport={'width': SIZE, 'height': SIZE}, device_scale_factor=1)
        for svg_path, png_path in paths:
            html = f'{TMP}/f.html'
            open(html, 'w', encoding='utf-8', newline='\n').write(
                f'<body style="margin:0;background:transparent"><img id="i" src="file://{svg_path}" '
                f'style="width:{SIZE}px;height:{SIZE}px;display:block"></body>')
            await pg.goto('file://' + html)
            await pg.wait_for_timeout(100)
            await pg.locator('#i').screenshot(path=png_path, omit_background=True)
        await br.close()


def main():
    os.makedirs(TMP, exist_ok=True)
    jobs = []
    for key, label, icon, pal, acc in SOCIAL:
        p = f'{TMP}/frame-{key}.svg'
        # pause the light sweep off-panel so the still frame is clean
        data = social_button(label, None, pal, FRAME_ACCENT[key]).replace('x="-140"', 'x="-400"')
        open(p, 'w', encoding='utf-8', newline='\n').write(data)
        jobs.append((p, f'{TMP}/frame-{key}.png'))
    asyncio.run(shoot(jobs))
    for key, *_ in SOCIAL:
        frame = Image.open(f'{TMP}/frame-{key}.png').convert('RGBA')
        logo = Image.open(os.path.join(HERE, 'logos', f'logo-{key}.png')).convert('RGBA')
        lw = round(SIZE * LOGO_W[key])
        lh = round(logo.height * lw / logo.width)
        logo = logo.resize((lw, lh), Image.NEAREST)
        cy = round(SIZE * .46)
        frame.alpha_composite(logo, ((SIZE - lw) // 2, cy - lh // 2))
        out = Image.new('RGBA', (SIZE, SIZE + GAP), (0, 0, 0, 0))
        out.paste(frame, (0, GAP // 2))
        path = os.path.join(OUT, f'btn-social-{key}.png')
        out.save(path, optimize=True)
        print(os.path.basename(path), os.path.getsize(path) // 1024, 'KB')


if __name__ == '__main__':
    main()
