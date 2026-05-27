"""
Fix Step 7: UTM content values are all mid-content. Need to correctly categorize.
Strategy: Find <a> tags that have Substack UTMs and check their full attributes.
"""
import os, re, glob

SITE_DIR = r"C:\Users\tumbl\projects\tumbleewords"
pages_fixed = 0
changes_by_location = {}

html_files = glob.glob(os.path.join(SITE_DIR, "*.html"))

for fpath in html_files:
    fname = os.path.basename(fpath)
    if fname in ("hero-banner.html", "newsletter-popup.html", "REPLACE-photo-reel.html",
                 "tagline-snippet.html", "discover.html"):
        continue

    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # Match full <a> opening tags that contain Substack UTM URLs
    # Pattern: matches from <a to the end of the href="..." attribute
    # We need to capture the full tag attributes to detect location
    def fix_content_value(m):
        full_a_tag = m.group(0)  # entire <a ...> opening tag

        # Skip if no Substack UTM
        if "utm_source=tumbleweedwords-com" not in full_a_tag:
            return full_a_tag

        # Detect correct location
        if 'class="ncta"' in full_a_tag:
            correct_loc = "nav"
        elif 'class="mm-cta"' in full_a_tag:
            correct_loc = "mobile-menu"
        elif 'style="color:inherit"' in full_a_tag:
            correct_loc = "footer"
        else:
            correct_loc = "mid-content"

        # Replace utm_content=mid-content (or any current value) with correct one
        new_tag = re.sub(
            r'utm_content=[^&"]+',
            f"utm_content={correct_loc}",
            full_a_tag
        )
        return new_tag

    # Match opening <a> tags (from <a to the > or next tag)
    new_content = re.sub(r'<a\s[^>]*>', fix_content_value, content)

    # Now handle the footer more carefully:
    # The footer copyright link: href="...substack.com?...&utm_content=mid-content"
    # is wrapped by <footer class="ft"> so let me fix it specifically
    # Pattern: in the footer section, find the Substack link with style="color:inherit"
    # This should already be handled by the style="color:inherit" check above

    if new_content != original:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)
        pages_fixed += 1
        for loc in ["nav", "mobile-menu", "footer", "mid-content", "popup"]:
            n_old = original.count(f"utm_content={loc}")
            n_new = new_content.count(f"utm_content={loc}")
            if n_new > n_old:
                changes_by_location[loc] = changes_by_location.get(loc, 0) + (n_new - n_old)

# Now count totals correctly
total_links = {}
for fpath in html_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    for loc in ["nav", "mobile-menu", "footer", "mid-content", "popup"]:
        total_links[loc] = total_links.get(loc, 0) + content.count(f"utm_content={loc}")

print(f"Pages fixed: {pages_fixed}")
print("\nCurrent distribution:")
for loc, count in sorted(total_links.items()):
    if count > 0:
        print(f"  {loc}: {count}")
