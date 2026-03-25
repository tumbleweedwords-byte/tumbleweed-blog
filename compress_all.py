"""
Compress all web-facing images above threshold.
Skips images already small. Overwrites in place.
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image, ImageOps

THRESHOLD = 300_000   # bytes
MAX_WIDTH  = 1200     # px — enough for retina card/hero use
QUALITY    = 80
BASE = 'C:/Users/tumbl/projects/tumbleewords'

# All images actually used on index.html or all-writing.html
targets = [
    # homepage
    'seoul-cherry.jpg', 'P1020204.JPG', 'P1010154.JPG', 'P1010204.JPG',
    'P1010970.JPG', 'P1020840.JPG', 'P1020901.JPG', 'P1030501.JPG',
    'ba-boca.jpg', 'ba-bodega.jpg', 'ba-cemetery.jpg',
    'berlin-bw.jpg', 'berlin-river.jpg', 'berlin-sculpture.jpg',
    'boat-wheel.jpg', 'card-berlin.jpg', 'card-england.jpg', 'card-london.jpg',
    'david.jpg', 'dazed_image.jpg', 'diary-desk.jpg',
    'hostel-fan.jpg', 'howl.jpg', 'istanbul-mosque.jpg', 'korea-go.jpg',
    'lake-bled.jpg', 'paris-bookshop.jpg', 'paris-street.jpg',
    'poetry_performance.jpg', 'scotland-coast.jpg',
    'travel-1.jpg', 'travel-2.jpg', 'travel-3.jpg',
    'vietnam-food.jpg', 'beach-sunset.jpg',
    'IMG-20220519-WA0044.jpg', 'IMG_20150321_163816.jpg',
    'IMG_20190217_180337.jpg', 'IMG_20190414_173711_308.jpg',
    'IMG_20190422_064326_895.jpg', 'IMG_20230622_194540619.jpg',
    'IMG_20240201_103315178_HDR.jpg', 'IMG_20240201_125031052.jpg',
    'IMG_20260305_112041095.jpg',
    # all-writing
    'IMG_0361.JPG', 'IMG_0423.JPG', 'S7002136.JPG',
    'howl.jpg', 'paris_images.jpg',
    # shared / recently added
    'P1010154.JPG', 'Gemini_Generated_Image_efsyskefsyskefsy.png',
]

total_saved = 0
for fname in sorted(set(targets)):
    path = os.path.join(BASE, fname)
    if not os.path.exists(path):
        continue
    size = os.path.getsize(path)
    if size < THRESHOLD:
        continue
    try:
        img = Image.open(path)
        try:
            img = ImageOps.exif_transpose(img)
        except Exception:
            pass
        w, h = img.size
        if w > MAX_WIDTH:
            new_h = int(h * MAX_WIDTH / w)
            img = img.resize((MAX_WIDTH, new_h), Image.LANCZOS)
        img = img.convert('RGB')
        # PNG → save as JPEG if it's not a logo/illustration with transparency
        out_path = path
        if fname.lower().endswith('.png'):
            # Keep as PNG but optimize
            img_orig = Image.open(path)
            img_orig = img_orig.convert('RGBA') if img_orig.mode in ('RGBA','P') else img_orig.convert('RGB')
            if w > MAX_WIDTH:
                img_orig = img_orig.resize((MAX_WIDTH, int(img_orig.height * MAX_WIDTH / w)), Image.LANCZOS)
            img_orig.save(out_path, 'PNG', optimize=True)
        else:
            img.save(out_path, 'JPEG', quality=QUALITY, optimize=True, progressive=True)
        new_size = os.path.getsize(out_path)
        saved = size - new_size
        total_saved += saved
        print(f'  {fname}: {size//1024}KB -> {new_size//1024}KB (saved {saved//1024}KB)')
    except Exception as e:
        print(f'  ERROR {fname}: {e}')

print(f'\nTotal saved: {total_saved//1024}KB ({total_saved//1048576}MB)')
