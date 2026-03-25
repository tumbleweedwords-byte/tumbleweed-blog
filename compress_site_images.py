#!/usr/bin/env python3
"""
Compress all site images over 200KB.
- JPEGs: resize to max 1400px wide, quality 82
- PNGs: resize to max 1400px wide, optimize
- Skips images already under 200KB
- Skips files that are clearly not site content (screenshots, docs)
"""

import os
import sys
from PIL import Image

SKIP_PATTERNS = [
    'Screenshot', 'background ', 'boilerplate', 'cookie example',
    'city images', 'put city images', 'box round', 'bocx round',
    'do the purple', 'example of boxes', 'top bar colour', 'populate with',
    'make the sub', 'fix.png', 'fixxx', 'redesign', 'mess', 'edit.png',
    'pale white', 'header move', 'tumbleweed words banner', 'purple.png',
    '5 years on road', 'CTA.png', 'paris images.jpg', 'dazed images.jpg',
    'paris image.jpg', 'dazed image.jpg'
]

MAX_WIDTH = 1400
JPEG_QUALITY = 82
MIN_SIZE_KB = 200

def should_skip(filename):
    for pattern in SKIP_PATTERNS:
        if pattern.lower() in filename.lower():
            return True
    return False

compressed = []
skipped = []
errors = []

image_extensions = ('.jpg', '.jpeg', '.JPG', '.JPEG', '.png', '.PNG')

files = [f for f in os.listdir('.') if f.endswith(image_extensions)]

for filename in sorted(files):
    if should_skip(filename):
        continue

    filepath = os.path.join('.', filename)
    size_kb = os.path.getsize(filepath) / 1024

    if size_kb < MIN_SIZE_KB:
        continue

    try:
        with Image.open(filepath) as img:
            original_size = size_kb
            w, h = img.size

            # Convert RGBA to RGB for JPEG
            if img.mode in ('RGBA', 'P') and filename.lower().endswith(('.jpg', '.jpeg')):
                img = img.convert('RGB')

            # Resize if wider than MAX_WIDTH
            if w > MAX_WIDTH:
                ratio = MAX_WIDTH / w
                new_h = int(h * ratio)
                img = img.resize((MAX_WIDTH, new_h), Image.LANCZOS)

            # Save
            if filename.lower().endswith(('.jpg', '.jpeg')):
                img.save(filepath, 'JPEG', quality=JPEG_QUALITY, optimize=True, progressive=True)
            else:
                img.save(filepath, 'PNG', optimize=True)

            new_size_kb = os.path.getsize(filepath) / 1024
            saving = original_size - new_size_kb
            compressed.append(f"{filename}: {original_size:.0f}KB → {new_size_kb:.0f}KB (saved {saving:.0f}KB)")

    except Exception as e:
        errors.append(f"{filename}: {e}")

print(f"\n=== COMPRESSION COMPLETE ===")
print(f"Compressed: {len(compressed)} files")
for line in compressed:
    print(f"  {line}")

if errors:
    print(f"\nErrors ({len(errors)}):")
    for e in errors:
        print(f"  {e}")

total_saved = sum(float(l.split('saved ')[1].split('KB')[0]) for l in compressed)
print(f"\nTotal saved: {total_saved:.0f}KB ({total_saved/1024:.1f}MB)")
