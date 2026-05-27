"""
Step 5B: Convert JPG/PNG to WebP without renaming originals (avoids Windows file lock).
Creates -original backup by copying (not moving), then writes WebP.
"""
import os, re, glob, shutil
from PIL import Image

SITE_DIR = r"C:\Users\tumbl\projects\tumbleewords"

html_files = glob.glob(os.path.join(SITE_DIR, "*.html"))

# Find all JPG/PNG files referenced in HTML
all_img_refs = set()
for fpath in html_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    refs = re.findall(r'src="([^"]*\.(jpg|jpeg|JPG|JPEG|png|PNG))"', content, re.IGNORECASE)
    for ref, ext in refs:
        fname = os.path.basename(ref)
        all_img_refs.add(fname)

converted = 0
size_saved = 0
conversion_map = {}  # old_name -> new_name (for updating HTML refs)

for img_name in sorted(all_img_refs):
    img_path = os.path.join(SITE_DIR, img_name)
    if not os.path.exists(img_path):
        continue

    ext = img_name.rsplit(".", 1)[-1].lower()
    if ext not in ("jpg", "jpeg", "png"):
        continue

    webp_name = img_name.rsplit(".", 1)[0] + ".webp"
    webp_path = os.path.join(SITE_DIR, webp_name)

    if os.path.exists(webp_path):
        # WebP already exists - just update HTML refs to point to webp
        conversion_map[img_name] = webp_name
        print(f"  WEBP EXISTS: {img_name} -> {webp_name} (updating refs)")
        continue

    original_size = os.path.getsize(img_path)
    if original_size < 10000:
        continue

    try:
        with Image.open(img_path) as img:
            w, h = img.size
            if max(w, h) > 1920:
                scale = 1920 / max(w, h)
                img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

            if img.mode in ("RGBA", "P", "LA"):
                img = img.convert("RGB")

            # Create backup by copying
            backup_name = img_name.rsplit(".", 1)[0] + "-original." + ext
            backup_path = os.path.join(SITE_DIR, backup_name)
            if not os.path.exists(backup_path):
                shutil.copy2(img_path, backup_path)

            # Save WebP (leave original in place)
            img.save(webp_path, "WEBP", quality=85)
            new_size = os.path.getsize(webp_path)

            saved = original_size - new_size
            size_saved += saved
            converted += 1
            conversion_map[img_name] = webp_name
            print(f"  CONVERTED: {img_name} -> {webp_name} ({original_size//1024}KB -> {new_size//1024}KB, saved {saved//1024}KB)")
    except Exception as e:
        print(f"  ERROR {img_name}: {e}")

print(f"\nConverted: {converted} new WebP files, saved {size_saved//1024//1024:.1f}MB")

# Update HTML references to use WebP where it exists
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

print(f"Updated HTML references in {refs_updated} pages")
print(f"\nConversion map ({len(conversion_map)} entries):")
for old, new in sorted(conversion_map.items())[:10]:
    print(f"  {old} -> {new}")
