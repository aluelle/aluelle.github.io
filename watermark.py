"""
Batch watermark script for angela.luelle.me
Usage: python3 watermark.py
- Reads photos from the 'photos/' folder
- Fixes rotation using ImageOps.exif_transpose (most robust method)
- Adds logo watermark to bottom right
- Saves watermarked versions to 'photos_watermarked/' folder
- Original photos are never modified
"""

from PIL import Image, ImageOps
import os

# ── Settings ──────────────────────────────────────────────────────────────────
PHOTOS_DIR = "photos"               # folder with your original photos
OUTPUT_DIR = "photos_watermarked"   # folder for watermarked output
LOGO_FILE  = "logo4.png"            # your white transparent logo
OPACITY    = 0.55                   # 0.0 = invisible, 1.0 = fully opaque
LOGO_SCALE = 0.18                   # logo width as fraction of photo width
MARGIN     = 0.04                   # distance from edge as fraction of photo width
# ──────────────────────────────────────────────────────────────────────────────

def add_watermark(photo_path, logo, output_path):
    photo = Image.open(photo_path)
    photo = ImageOps.exif_transpose(photo)  # most robust EXIF rotation fix
    photo = photo.convert("RGBA")
    pw, ph = photo.size

    # Scale logo relative to photo width
    logo_w = int(pw * LOGO_SCALE)
    logo_h = int(logo.size[1] * logo_w / logo.size[0])
    logo_resized = logo.resize((logo_w, logo_h), Image.LANCZOS)

    # Apply opacity
    r, g, b, a = logo_resized.split()
    a = a.point(lambda x: int(x * OPACITY))
    logo_resized = Image.merge("RGBA", (r, g, b, a))

    # Position: bottom right with margin
    margin = int(pw * MARGIN)
    x = pw - logo_w - margin
    y = ph - logo_h - margin

    # Paste onto photo
    watermarked = photo.copy()
    watermarked.paste(logo_resized, (x, y), logo_resized)

    # Save as JPEG
    watermarked.convert("RGB").save(output_path, "JPEG", quality=95)
    print(f"  ✓ {os.path.basename(photo_path)}")

def main():
    if not os.path.exists(LOGO_FILE):
        print(f"Logo file '{LOGO_FILE}' not found.")
        return

    if not os.path.exists(PHOTOS_DIR):
        print(f"Photos folder '{PHOTOS_DIR}' not found.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    logo = Image.open(LOGO_FILE).convert("RGBA")

    extensions = (".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG")
    photos = [f for f in os.listdir(PHOTOS_DIR) if f.endswith(extensions)]

    if not photos:
        print("No photos found in the photos/ folder.")
        return

    print(f"Adding watermark to {len(photos)} photos...\n")
    for filename in sorted(photos):
        input_path  = os.path.join(PHOTOS_DIR, filename)
        output_name = os.path.splitext(filename)[0] + ".jpg"
        output_path = os.path.join(OUTPUT_DIR, output_name)
        add_watermark(input_path, logo, output_path)

    print(f"\nDone! Watermarked photos saved to '{OUTPUT_DIR}/'")
    print("Replace your 'photos/' folder with the contents of 'photos_watermarked/' when ready.")

if __name__ == "__main__":
    main()
