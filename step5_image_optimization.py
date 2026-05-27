"""
Step 5: Image optimization
A. Image format audit
B. Convert oversized JPG/PNG to WebP (only those referenced in HTML)
C. Add loading="lazy" to non-hero img tags
D. Add preconnect hints to all pages
"""
import os, re, glob
from PIL import Image

SITE_DIR = r"C:\Users\tumbl\projects\tumbleewords"

# === PART D: Preconnect hints ===
PRECONNECT = """<link rel="preconnect" href="https://uk.bookshop.org">
<link rel="preconnect" href="https://tumbleweedwords.substack.com">
<link rel="dns-prefetch" href="https://www.google-analytics.com">"""

html_files = glob.glob(os.path.join(SITE_DIR, "*.html"))
preconnect_added = 0

for fpath in html_files:
    fname = os.path.basename(fpath)
    if fname in ("hero-banner.html", "newsletter-popup.html", "REPLACE-photo-reel.html",
                 "tagline-snippet.html", "discover.html"):
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    if 'href="https://uk.bookshop.org"' not in content:
        # Insert before first </head> occurrence
        new_content = content.replace("</head>", PRECONNECT + "\n</head>", 1)
        if new_content != content:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            preconnect_added += 1

print(f"Preconnect hints added to {preconnect_added} pages")

# === PART A: Image format audit ===
jpg_files = glob.glob(os.path.join(SITE_DIR, "*.jpg")) + glob.glob(os.path.join(SITE_DIR, "*.jpeg"))
png_files = glob.glob(os.path.join(SITE_DIR, "*.png"))
webp_files = glob.glob(os.path.join(SITE_DIR, "*.webp"))

print(f"\nImage audit:")
print(f"  JPG/JPEG: {len(jpg_files)}")
print(f"  PNG: {len(png_files)}")
print(f"  WebP: {len(webp_files)}")
print(f"  Total: {len(jpg_files) + len(png_files) + len(webp_files)}")

# Find images over 500KB
large_images = []
for f in jpg_files + png_files + webp_files:
    size = os.path.getsize(f)
    if size > 500000:
        large_images.append((size, os.path.basename(f)))

large_images.sort(reverse=True)
print(f"\nImages over 500KB: {len(large_images)}")
for size, name in large_images[:20]:
    print(f"  {size//1024}KB - {name}")

# === PART B: Convert JPG/PNG files referenced in HTML to WebP ===
# First find which images are actually used
all_img_refs = set()
for fpath in html_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    refs = re.findall(r'src="([^"]*\.(jpg|jpeg|png))"', content, re.IGNORECASE)
    for ref, ext in refs:
        # Get just the filename (not path)
        fname = os.path.basename(ref)
        all_img_refs.add(fname)

print(f"\nJPG/PNG files referenced in HTML: {len(all_img_refs)}")

converted = 0
size_saved = 0
conversion_map = {}  # old_name -> new_name

for img_name in all_img_refs:
    img_path = os.path.join(SITE_DIR, img_name)
    if not os.path.exists(img_path):
        continue

    ext = img_name.rsplit(".", 1)[-1].lower()
    if ext not in ("jpg", "jpeg", "png"):
        continue

    # Skip small images that are already fine (under 200KB and already have a webp version)
    webp_name = img_name.rsplit(".", 1)[0] + ".webp"
    webp_path = os.path.join(SITE_DIR, webp_name)

    if os.path.exists(webp_path):
        print(f"  SKIP (webp exists): {img_name}")
        continue

    original_size = os.path.getsize(img_path)

    # Only convert if it's a content image (not a tiny icon)
    if original_size < 10000:
        print(f"  SKIP (tiny): {img_name}")
        continue

    try:
        with Image.open(img_path) as img:
            # Check dimensions
            w, h = img.size
            max_dim = max(w, h)

            if max_dim > 1920:
                scale = 1920 / max_dim
                new_w, new_h = int(w * scale), int(h * scale)
                img = img.resize((new_w, new_h), Image.LANCZOS)

            # Convert to RGB if needed (PNG can have RGBA)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Save as WebP
            backup_path = img_path.rsplit(".", 1)[0] + "-original." + ext
            os.rename(img_path, backup_path)

            img.save(img_path.rsplit(".", 1)[0] + ".webp", "WEBP", quality=85)
            new_size = os.path.getsize(img_path.rsplit(".", 1)[0] + ".webp")

            saved = original_size - new_size
            size_saved += saved
            converted += 1
            conversion_map[img_name] = webp_name
            print(f"  CONVERTED: {img_name} -> {webp_name} ({original_size//1024}KB -> {new_size//1024}KB)")
    except Exception as e:
        print(f"  ERROR converting {img_name}: {e}")

print(f"\nConverted {converted} images, saved {size_saved//1024//1024:.1f}MB")

# Update HTML references for converted images
if conversion_map:
    refs_updated = 0
    for fpath in html_files:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        original = content
        for old_name, new_name in conversion_map.items():
            content = content.replace(f'src="{old_name}"', f'src="{new_name}"')
            content = content.replace(f"src='{old_name}'", f"src='{new_name}'")
        if content != original:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            refs_updated += 1
    print(f"Updated image references in {refs_updated} pages")

# === PART C: Add loading="lazy" to non-hero images ===
# Hero image = first <img> in the page body (not inside popup)
# Strategy: find all <img> tags, skip the first one that's not inside #tw-popup-overlay

lazy_added = 0
lazy_pages = 0

for fpath in html_files:
    fname = os.path.basename(fpath)
    if fname in ("hero-banner.html", "newsletter-popup.html", "REPLACE-photo-reel.html",
                 "tagline-snippet.html", "discover.html"):
        continue

    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # Find all img tags that don't already have loading attribute
    # Add loading="lazy" to all of them EXCEPT:
    # 1. Images with loading="eager" already set
    # 2. The first non-popup img (hero image)

    # Split off the popup section
    popup_split = content.split('id="tw-popup-overlay"')
    body_before_popup = popup_split[0] if len(popup_split) > 1 else content

    # Find the first img tag in the main body (not popup)
    first_img_m = re.search(r'<img\s', body_before_popup)
    hero_img_pos = first_img_m.start() if first_img_m else -1

    def add_lazy(m):
        tag = m.group(0)
        pos = m.start()

        # Skip if already has loading attribute
        if 'loading=' in tag:
            return tag
        # Skip hero image (first img in main body)
        if pos == hero_img_pos:
            return tag
        # Skip tiny inline icons (width <= 20px)
        width_m = re.search(r'width="(\d+)"', tag)
        if width_m and int(width_m.group(1)) <= 20:
            return tag

        # Add loading="lazy" before the closing >
        return tag.rstrip('>').rstrip('/').rstrip() + ' loading="lazy">'

    new_content = re.sub(r'<img\s[^>]+/?>', add_lazy, content)

    if new_content != original:
        count = new_content.count('loading="lazy"') - original.count('loading="lazy"')
        lazy_added += count
        lazy_pages += 1
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)

print(f"\nLazy loading: added loading='lazy' to {lazy_added} images across {lazy_pages} pages")
