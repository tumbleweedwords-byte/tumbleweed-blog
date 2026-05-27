"""
Step 6: Add UTM parameters to all Bookshop.org affiliate links.
Format: https://uk.bookshop.org/a/17219/[isbn]?utm_source=tumbleweedwords&utm_medium=affiliate&utm_campaign=[page-slug]
Footer Bookshop link (/shop/tumbleweedwords): utm_campaign=footer
"""
import os, re, glob

SITE_DIR = r"C:\Users\tumbl\projects\tumbleewords"
UTM_SUFFIX = "utm_source=tumbleweedwords&utm_medium=affiliate&utm_campaign="

total_updated = 0
campaign_counts = {}
pages_updated = 0

html_files = glob.glob(os.path.join(SITE_DIR, "*.html"))

for fpath in html_files:
    fname = os.path.basename(fpath)
    # Skip template snippets
    if fname in ("hero-banner.html", "newsletter-popup.html", "REPLACE-photo-reel.html",
                 "tagline-snippet.html", "discover.html"):
        continue

    page_slug = fname.replace(".html", "")

    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    count = 0

    # Pattern 1: /a/17219/[isbn] links (no existing UTM)
    # These are like: href="https://uk.bookshop.org/a/17219/9781234567890"
    # Match href="https://uk.bookshop.org/a/17219/..." (no query string yet)
    # Must NOT already have utm_source
    content = re.sub(
        r'(href="https://uk\.bookshop\.org/a/17219/[^"?]+)"',
        lambda m: m.group(0) if "utm_source" in m.group(1) else
                  m.group(0).replace(m.group(1), m.group(1) + "?" + UTM_SUFFIX + page_slug),
        content
    )

    # Pattern 2: /shop/tumbleweedwords in footer - use utm_campaign=footer
    # This appears as: href="https://uk.bookshop.org/shop/tumbleweedwords"
    if 'href="https://uk.bookshop.org/shop/tumbleweedwords"' in original:
        shop_replacement = 'href="https://uk.bookshop.org/shop/tumbleweedwords?' + UTM_SUFFIX + 'footer"'
        content = content.replace(
            'href="https://uk.bookshop.org/shop/tumbleweedwords"',
            shop_replacement
        )
        if 'href="https://uk.bookshop.org/shop/tumbleweedwords"' not in content:
            count += 1
            total_updated += 1
            campaign_counts["footer"] = campaign_counts.get("footer", 0) + 1

    if content != original:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        pages_updated += 1

print(f"Pages updated: {pages_updated}")
print(f"Total Bookshop links tagged with UTM: {total_updated}")
print("\nBreakdown by campaign:")
for slug, count in sorted(campaign_counts.items()):
    print(f"  {slug}: {count}")
