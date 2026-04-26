"""
make_icon.py  -  Generate url2html_gui.ico and url2html_gui_256.png

Writes the ICO file manually from PNG byte buffers – this completely
avoids Pillow's ICO encoder, which can hang on Windows due to internal
GDI/quantization calls.

Run once:
    python make_icon.py

Requires:
    pip install pillow
"""

import io
import os
import struct
import sys


def _require_pillow():
    try:
        from PIL import Image, ImageDraw  # noqa: F401
    except ImportError:
        print("ERROR: Pillow is not installed.")
        print("       Run:  pip install pillow")
        sys.exit(1)


def _load_font(size):
    """Return an ImageFont using absolute paths; fall back to built-in."""
    from PIL import ImageFont

    candidates = [
        os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "arialbd.ttf"),
        os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "arial.ttf"),
        os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "segoeui.ttf"),
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    for path in candidates:
        if os.path.isfile(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def draw_icon(size):
    """Draw one icon frame and return an RGBA PIL Image."""
    from PIL import Image, ImageDraw

    img  = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background circle – dark blue
    m = max(1, size // 16)
    draw.ellipse([m, m, size - m - 1, size - m - 1], fill=(21, 101, 192, 255))

    # Inner circle – lighter blue
    m2 = size // 6
    draw.ellipse([m2, m2, size - m2 - 1, size - m2 - 1], fill=(30, 136, 229, 255))

    # Arrow shaft
    cx, cy = size / 2.0, size / 2.0
    aw, ah = size * 0.38, size * 0.18
    draw.rectangle(
        [int(cx - aw * 0.80), int(cy - ah * 0.40),
         int(cx + aw * 0.25), int(cy + ah * 0.40)],
        fill=(236, 239, 241, 255),
    )

    # Arrowhead
    draw.polygon(
        [(int(cx + aw),        int(cy)),
         (int(cx + aw * 0.20), int(cy - ah)),
         (int(cx + aw * 0.20), int(cy + ah))],
        fill=(236, 239, 241, 255),
    )

    # "H" label on larger sizes
    if size >= 64:
        font = _load_font(max(10, size // 5))
        draw.text(
            (cx + aw * 0.05, cy + ah * 0.35),
            "H",
            fill=(255, 236, 64, 255),
            font=font,
        )

    return img


def _frame_to_png_bytes(img):
    """Encode a PIL Image to PNG bytes via a BytesIO buffer (no disk I/O)."""
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def _build_ico(png_bytes_list):
    """
    Assemble a valid .ico file from a list of PNG byte strings.

    ICO format:
      Header  : 6 bytes  (reserved=0, type=1, count=N)
      DirEntry: 16 bytes per image
      Data    : concatenated PNG blobs

    Each directory entry:
      width   1 byte  (0 = 256)
      height  1 byte  (0 = 256)
      colors  1 byte  (0 = no palette)
      reserved 1 byte (0)
      planes  2 bytes (1)
      bit_count 2 bytes (32)
      size    4 bytes  (byte length of image data)
      offset  4 bytes  (byte offset from start of file)
    """
    count = len(png_bytes_list)
    header_size   = 6
    dir_entry_size = 16
    data_offset   = header_size + dir_entry_size * count

    # ICO header
    header = struct.pack("<HHH", 0, 1, count)

    dir_entries = b""
    image_data  = b""
    current_offset = data_offset

    for png_bytes in png_bytes_list:
        # Read actual dimensions from the PNG header (bytes 16-24)
        w = struct.unpack(">I", png_bytes[16:20])[0]
        h = struct.unpack(">I", png_bytes[20:24])[0]

        # ICO spec: width/height 0 means 256
        ico_w = 0 if w >= 256 else w
        ico_h = 0 if h >= 256 else h
        size  = len(png_bytes)

        dir_entries += struct.pack(
            "<BBBBHHII",
            ico_w, ico_h,
            0,           # color count
            0,           # reserved
            1,           # planes
            32,          # bits per pixel
            size,
            current_offset,
        )
        image_data     += png_bytes
        current_offset += size

    return header + dir_entries + image_data


def make_ico():
    """Generate the icon files and exit cleanly."""
    sizes = [256, 64, 32, 16]

    frames    = [draw_icon(s) for s in sizes]
    png_blobs = [_frame_to_png_bytes(f) for f in frames]

    # Close all image objects now – we have the bytes we need
    for img in frames:
        img.close()

    # Write ICO manually (no Pillow ICO encoder)
    ico_bytes = _build_ico(png_blobs)
    ico_path  = "url2html_gui.ico"
    with open(ico_path, "wb") as fh:
        fh.write(ico_bytes)
    print(f"Created: {ico_path}  ({len(ico_bytes):,} bytes)")

    # Write 256-px PNG using raw bytes (already encoded above)
    png_path = "url2html_gui_256.png"
    with open(png_path, "wb") as fh:
        fh.write(png_blobs[0])
    print(f"Created: {png_path}  ({len(png_blobs[0]):,} bytes)")


if __name__ == "__main__":
    _require_pillow()
    make_ico()
    sys.exit(0)
