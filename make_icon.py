"""
make_icon.py  –  Generate url2html_gui.ico  (256x256 + 32x32 + 16x16)
Run once:  python make_icon.py
Requires:  Pillow   (pip install pillow)
"""

import math
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise SystemExit("Pillow is required: pip install pillow")

def draw_icon(size):
    img  = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background circle – dark blue
    margin = size // 16
    draw.ellipse([margin, margin, size - margin, size - margin],
                 fill=(21, 101, 192, 255))

    # Inner lighter circle
    m2 = size // 6
    draw.ellipse([m2, m2, size - m2, size - m2],
                 fill=(30, 136, 229, 255))

    # Arrow / link symbol  →  simple right-pointing arrow
    cx, cy = size // 2, size // 2
    aw = size * 0.38   # half-width of arrow
    ah = size * 0.18   # half-height

    # Arrow shaft
    shaft_top    = int(cy - ah * 0.4)
    shaft_bottom = int(cy + ah * 0.4)
    shaft_right  = int(cx + aw * 0.3)
    shaft_left   = int(cx - aw * 0.8)

    draw.rectangle([shaft_left, shaft_top, shaft_right, shaft_bottom],
                   fill=(236, 239, 241, 255))

    # Arrowhead (triangle)
    tip_x  = int(cx + aw)
    base_x = int(cx + aw * 0.2)
    pts = [
        (tip_x, cy),
        (base_x, int(cy - ah)),
        (base_x, int(cy + ah)),
    ]
    draw.polygon(pts, fill=(236, 239, 241, 255))

    # Small "H" letter at bottom-right quadrant
    if size >= 64:
        fs = max(12, size // 5)
        try:
            font = ImageFont.truetype("arial.ttf", fs)
        except Exception:
            font = ImageFont.load_default()
        draw.text((cx + aw * 0.05, cy + ah * 0.4), "H",
                  fill=(255, 236, 64, 255), font=font)

    return img


def make_ico():
    sizes  = [256, 64, 32, 16]
    frames = [draw_icon(s) for s in sizes]
    frames[0].save(
        "url2html_gui.ico",
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=frames[1:],
    )
    # Also save a 256-px PNG for README / GitHub
    frames[0].save("url2html_gui_256.png", format="PNG")
    print("Created: url2html_gui.ico  and  url2html_gui_256.png")


if __name__ == "__main__":
    make_ico()
