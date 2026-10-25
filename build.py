import base64
import io
from pathlib import Path

from PIL import Image, ImageColor

HERE = Path(__file__).resolve().parent

LOGO = [
    '..............wg',
    '.............wwg',
    '............wwg.',
    '.kkkkkkkkkkwwgk.',
    '.kdBBBBBBBwwgpk.',
    '.kdbbbbbbwwgbpk.',
    '.kdbbbbbwwgbbpk.',
    '.kdbbbbwwgbbbpk.',
    '.kdbbbbggbbbbpk.',
    '.kdbbbiGbbbbbpk.',
    '.kdbbbbbbbbbbpk.',
    '.kdbbbbbbbbbbpk.',
    '.kdbbbbbbbbbbpk.',
    '.kdBBBBBBBBBBpk.',
    '.kkpppppppppppk.',
    '..kkkkkkkkkkkk..',
]
PALETTE = {'k': '#24160b', 'd': '#4a2a14', 'b': '#7a4a26', 'B': '#96603a', 'p': '#efe6cc',
           'w': '#fafafa', 'g': '#c4c4c4', 'G': '#6d6d6d', 'i': '#111111'}


def svg_icon():
    rects = []
    for y, row in enumerate(LOGO):
        x = 0
        while x < len(row):
            ch, w = row[x], 1
            while x + w < len(row) and row[x + w] == ch:
                w += 1
            if ch in PALETTE:
                rects.append(f'<rect x="{x}" y="{y}" width="{w}" height="1" fill="{PALETTE[ch]}"/>')
            x += w
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" shape-rendering="crispEdges">'
            + ''.join(rects) + '</svg>')


def png_icon(size, background=None):
    img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(LOGO):
        for x, ch in enumerate(row):
            if ch in PALETTE:
                img.putpixel((x, y), ImageColor.getrgb(PALETTE[ch]) + (255,))
    if background:
        pad = 2
        canvas = Image.new('RGBA', (16 + pad * 2, 16 + pad * 2), background)
        canvas.alpha_composite(img, (pad, pad))
        img = canvas
    img = img.resize((size, size), Image.NEAREST)
    buf = io.BytesIO()
    img.save(buf, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()


def main():
    svg = 'data:image/svg+xml;base64,' + base64.b64encode(svg_icon().encode()).decode()
    head = '\n'.join([
        '<!doctype html>',
        '<html lang="ru">',
        '<head>',
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">',
        '<meta name="theme-color" content="#1f160f">',
        f'<link rel="icon" type="image/svg+xml" href="{svg}">',
        f'<link rel="icon" type="image/png" sizes="32x32" href="{png_icon(32)}">',
        f'<link rel="apple-touch-icon" sizes="180x180" href="{png_icon(180, background="#c6c6c6")}">',
        '</head>',
        '<body>',
    ])
    page = head + '\n' + (HERE / 'book.html').read_text(encoding='utf-8') + '\n</body>\n</html>\n'
    for out in (HERE / 'index.html', HERE / 'deploy' / 'index.html'):
        out.parent.mkdir(exist_ok=True)
        out.write_text(page, encoding='utf-8')
        print('собрано:', out.relative_to(HERE))


if __name__ == '__main__':
    main()
