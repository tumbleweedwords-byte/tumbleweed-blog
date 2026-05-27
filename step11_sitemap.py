"""
Step 11: Update sitemap.xml - set lastmod to today for all modified pages,
check for missing/extra pages.
"""
import os, glob, re
from datetime import date

SITE_DIR = r"C:\Users\tumbl\projects\tumbleewords"
SITEMAP = os.path.join(SITE_DIR, "sitemap.xml")
TODAY = date.today().isoformat()  # 2026-05-23

with open(SITEMAP, "r", encoding="utf-8") as f:
    sitemap = f.read()

# Get all URLs currently in sitemap
sitemap_urls = re.findall(r'<loc>(https://tumbleweedwords\.com/[^<]*)</loc>', sitemap)
print(f"URLs in sitemap before: {len(sitemap_urls)}")

# Get all actual HTML pages in repo (real pages only)
SKIP_FILES = {
    "hero-banner.html", "newsletter-popup.html", "REPLACE-photo-reel.html",
    "tagline-snippet.html", "discover.html", "contact-thanks.html"
}

actual_files = set()
for f in glob.glob(os.path.join(SITE_DIR, "*.html")):
    fname = os.path.basename(f)
    if fname not in SKIP_FILES:
        actual_files.add(fname)

# Build set of expected URLs
expected_urls = set()
for fname in actual_files:
    if fname == "index.html":
        expected_urls.add("https://tumbleweedwords.com/")
    else:
        expected_urls.add(f"https://tumbleweedwords.com/{fname}")

# Find URLs in sitemap not in actual files
sitemap_url_set = set(sitemap_urls)
extra_in_sitemap = sitemap_url_set - expected_urls
missing_from_sitemap = expected_urls - sitemap_url_set

print(f"\nURLs in sitemap but no corresponding file: {len(extra_in_sitemap)}")
for u in sorted(extra_in_sitemap):
    print(f"  EXTRA: {u}")

print(f"\nFiles missing from sitemap: {len(missing_from_sitemap)}")
for u in sorted(missing_from_sitemap):
    print(f"  MISSING: {u}")

# Update all lastmod dates to today
updated_count = 0
new_sitemap = re.sub(
    r'<lastmod>\d{4}-\d{2}-\d{2}</lastmod>',
    f'<lastmod>{TODAY}</lastmod>',
    sitemap
)
updated_count = len(re.findall(r'<lastmod>', sitemap))

# Add missing pages
for url in sorted(missing_from_sitemap):
    new_entry = f"""
  <url>
    <loc>{url}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>"""
    new_sitemap = new_sitemap.replace("</urlset>", new_entry + "\n</urlset>")

# Remove extra URLs (those without corresponding files)
for url in extra_in_sitemap:
    # Remove the entire <url>...</url> block for this URL
    pattern = r'\s*<url>\s*<loc>' + re.escape(url) + r'</loc>.*?</url>'
    new_sitemap = re.sub(pattern, '', new_sitemap, flags=re.DOTALL)

with open(SITEMAP, "w", encoding="utf-8") as f:
    f.write(new_sitemap)

final_urls = re.findall(r'<loc>', new_sitemap)
print(f"\nURLs in sitemap after: {len(final_urls)}")
print(f"lastmod dates updated: {updated_count}")
print(f"Added: {len(missing_from_sitemap)}")
print(f"Removed: {len(extra_in_sitemap)}")
print(f"Today's date used: {TODAY}")
