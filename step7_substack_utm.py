"""
Step 7: Add UTM parameters to Substack subscribe/homepage links.
Target: href="https://tumbleweedwords.substack.com" and href="https://tumbleweedwords.substack.com/subscribe"
NOT: /archive, /p/, /api/

UTM format: ?utm_source=tumbleweedwords-com&utm_medium=referral&utm_campaign=[page-slug]&utm_content=[location]

Location detection:
- class="ncta" -> nav
- class="mm-cta" -> mobile-menu
- style="color:inherit" (footer copyright) -> footer
- class="btn btn-p" or class="btn btn-g" -> mid-content
- everything else -> mid-content
"""
import os, re, glob

SITE_DIR = r"C:\Users\tumbl\projects\tumbleewords"
UTM_BASE = "utm_source=tumbleweedwords-com&utm_medium=referral"

total_updated = 0
location_counts = {}
pages_updated = 0

html_files = glob.glob(os.path.join(SITE_DIR, "*.html"))

# Substack base URL patterns to target (not /archive, /p/, /api)
SUBSTACK_TARGETS = [
    "https://tumbleweedwords.substack.com\"",
    "https://tumbleweedwords.substack.com/subscribe\"",
]

def detect_location(pre_context, link_attrs):
    """Detect the location of a Substack link based on its attributes and surrounding context."""
    if 'class="ncta"' in link_attrs:
        return "nav"
    if 'class="mm-cta"' in link_attrs:
        return "mobile-menu"
    # Footer copyright link: style="color:inherit" and "Tumbleweed Words" text typically
    if 'style="color:inherit"' in link_attrs:
        return "footer"
    # Check if we're inside popup overlay
    if 'tw-popup-overlay' in pre_context[-3000:] and '</div>' not in pre_context[-500:]:
        return "popup"
    return "mid-content"

def make_utm(page_slug, location):
    return f"{UTM_BASE}&utm_campaign={page_slug}&utm_content={location}"

for fpath in html_files:
    fname = os.path.basename(fpath)
    if fname in ("hero-banner.html", "newsletter-popup.html", "REPLACE-photo-reel.html",
                 "tagline-snippet.html", "discover.html"):
        continue

    page_slug = fname.replace(".html", "")

    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # Find all href="https://tumbleweedwords.substack.com[something]" attributes
    # We'll process with a regex that captures the full <a ...> tag context
    # Pattern: find href="https://tumbleweedwords.substack.com" or href="https://tumbleweedwords.substack.com/subscribe"
    # but NOT href="https://tumbleweedwords.substack.com/p/..." or /archive or /api

    def replace_substack_link(m):
        full_match = m.group(0)
        url = m.group(1)

        # Skip if already has UTM
        if "utm_source" in url:
            return full_match

        # Skip non-subscribe paths
        path_after_base = url.replace("https://tumbleweedwords.substack.com", "")
        if path_after_base.startswith("/p/") or path_after_base.startswith("/archive") or path_after_base.startswith("/api"):
            return full_match

        # Detect location from the full <a> tag attributes
        # Get the full tag by looking at the surrounding context
        start = m.start()
        # Look back up to 200 chars for the opening <a
        pre_tag = content[max(0, start-200):start]
        # Full tag attrs are in the match itself
        link_attrs = full_match

        location = detect_location(pre_tag, link_attrs)

        utm = make_utm(page_slug, location)
        new_url = url + "?" + utm

        return full_match.replace(url + '"', new_url + '"')

    # Match href="https://tumbleweedwords.substack.com[optional path]"
    # but we process based on what follows substack.com
    new_content = re.sub(
        r'href="(https://tumbleweedwords\.substack\.com[^"]*)"',
        replace_substack_link,
        content
    )

    if new_content != original:
        count = new_content.count(UTM_BASE) - original.count(UTM_BASE)
        total_updated += count
        # Track locations
        for loc in ["nav", "mobile-menu", "footer", "popup", "mid-content"]:
            added = new_content.count(f"utm_content={loc}") - original.count(f"utm_content={loc}")
            if added > 0:
                location_counts[loc] = location_counts.get(loc, 0) + added
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)
        pages_updated += 1
        content = new_content  # update for subsequent patterns

print(f"Pages updated: {pages_updated}")
print(f"Total Substack links tagged with UTM: {total_updated}")
print("\nBreakdown by content/location:")
for loc, count in sorted(location_counts.items()):
    print(f"  {loc}: {count}")
