"""
Compress oversized card/city images for web.
Target: max 800px wide, quality 82, progressive JPEG.
Images already small (<400KB) are left alone.
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image

THRESHOLD = 400_000  # bytes — skip if already under this
MAX_WIDTH  = 900     # px
QUALITY    = 82

targets = [
    'city-edinburgh.jpg',
    'city-prague.jpg',
    'city-istanbul.jpg',
    'city-lisbon.jpg',
    'city-buenos-aires.jpg',
    'P1020216.JPG',
    'P1040311.JPG',
    'IMG_20221001_094917117.jpg',
    'IMG_20190418_152257_016.jpg',
    'IMG_20251030_115310956.jpg',
    'IMG_20150317_132854.jpg',
    'P1020237.JPG',
]

base = 'C:/Users/tumbl/projects/tumbleewords'

for fname in targets:
    path = os.path.join(base, fname)
    if not os.path.exists(path):
        print(f'  SKIP (not found): {fname}')
        continue
    size = os.path.getsize(path)
    if size < THRESHOLD:
        print(f'  OK ({size//1024}KB): {fname}')
        continue
    img = Image.open(path)
    # preserve EXIF orientation
    try:
        from PIL import ImageOps
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass
    w, h = img.size
    if w > MAX_WIDTH:
        new_h = int(h * MAX_WIDTH / w)
        img = img.resize((MAX_WIDTH, new_h), Image.LANCZOS)
    # Save as progressive JPEG
    out = path  # overwrite in place
    img = img.convert('RGB')
    img.save(out, 'JPEG', quality=QUALITY, optimize=True, progressive=True)
    new_size = os.path.getsize(out)
    print(f'  {fname}: {size//1024}KB -> {new_size//1024}KB')

print('Done.')
