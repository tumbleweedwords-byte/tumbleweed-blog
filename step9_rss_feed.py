"""
Step 9: Create feed.xml at repo root.
Populate with 15 most recent pieces, ordered newest first.
Then add <link rel="alternate" type="application/rss+xml" ...> to every page's <head>.
"""
import os, re, glob, html
from datetime import datetime

SITE_DIR = r"C:\Users\tumbl\projects\tumbleewords"
FEED_PATH = os.path.join(SITE_DIR, "feed.xml")

# Skip non-content pages
SKIP = {
    "hero-banner.html", "newsletter-popup.html", "REPLACE-photo-reel.html",
    "tagline-snippet.html", "discover.html", "contact-thanks.html",
    "index.html", "all-writing.html", "reads.html", "craft-theory.html",
    "essays-and-culture.html", "about.html", "contact.html", "faq.html",
    "faq-flash-fiction.html", "faq-reading.html", "faq-writing-life.html",
    "faq-literary-craft.html", "sitemap.html", "search.html",
    "flash-fiction-prompts.html", "literary-style-quiz.html", "spot-the-typo.html",
    "flash-fiction-workshop.html", "literary-magazine-finder.html",
    "postcards.html", "famous-readings.html", "literary-interviews.html",
    "subscribe.html", "404.html", "robots.txt"
}

def get_page_info(fpath):
    """Extract title, description, date, category from HTML file."""
    fname = os.path.basename(fpath)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Title from <title> tag
    title_m = re.search(r'<title>([^<]+)</title>', content)
    title = title_m.group(1).strip() if title_m else fname

    # Description from meta
    desc_m = re.search(r'<meta name="description" content="([^"]+)"', content)
    description = desc_m.group(1).strip() if desc_m else ""

    # Date from JSON-LD datePublished (handles YYYY-MM-DD, YYYY-MM, YYYY formats)
    date_m = re.search(r'"datePublished"\s*:\s*"(\d{4}(?:-\d{2}(?:-\d{2})?)?)"', content)
    if not date_m:
        date_m = re.search(r'"dateModified"\s*:\s*"(\d{4}(?:-\d{2}(?:-\d{2})?)?)"', content)
    if date_m:
        date_str = date_m.group(1)
        try:
            if len(date_str) == 10:
                pub_date = datetime.strptime(date_str, "%Y-%m-%d")
            elif len(date_str) == 7:
                pub_date = datetime.strptime(date_str + "-01", "%Y-%m-%d")
            else:
                pub_date = datetime.strptime(date_str + "-01-01", "%Y-%m-%d")
        except:
            pub_date = datetime(2026, 1, 1)
    else:
        pub_date = datetime(2026, 1, 1)

    # Category from schema type or page classification
    schema_type_m = re.search(r'"@type"\s*:\s*"([^"]+)"', content)
    schema_type = schema_type_m.group(1) if schema_type_m else ""

    if any(x in fname for x in ['-review', 'review-']):
        category = "Book Reviews"
    elif any(x in fname for x in ['flash-fiction-', 'fiction-set-', 'starving', 'growing-pains',
                                    'street-legal', 'wake-up-call', 'honest-pursuit', 'cool-poem',
                                    'women-who-want', 'viral-poetry', 'indiscretion', 'a-man-with',
                                    'an-expat', 'kerouac', 'punch-drunk', 'a-love', 'drift',
                                    'jigsaw', 'some-things']):
        category = "Fiction & Poetry"
    elif any(x in fname for x in ['craft', 'influenced-by', 'iceberg', 'minimalist', 'show-dont',
                                    'how-to-write', 'how-to-end', 'prose-poetry', 'flash-fiction-vs',
                                    'what-is-flash', 'how-long', 'best-flash']):
        category = "Craft & Theory"
    elif any(x in fname for x in ['2026-', 'pulitzer', 'booker', 'pushcart', 'prize', 'womens-prize']):
        category = "Prize Coverage"
    else:
        category = "Essays & Culture"

    url = f"https://tumbleweedwords.com/{fname}"

    return {
        "title": title,
        "url": url,
        "description": description,
        "date": pub_date,
        "date_str": pub_date.strftime("%a, %d %b %Y 00:00:00 +0000"),
        "category": category
    }

# Gather all content pages
pages = []
html_files = glob.glob(os.path.join(SITE_DIR, "*.html"))
for fpath in html_files:
    fname = os.path.basename(fpath)
    if fname in SKIP:
        continue
    try:
        info = get_page_info(fpath)
        pages.append(info)
    except Exception as e:
        print(f"Error processing {fname}: {e}")

# Sort by date (newest first), take top 15
pages.sort(key=lambda x: x["date"], reverse=True)
recent = pages[:15]

now_rfc822 = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")

# Build RSS XML
items_xml = ""
for page in recent:
    # First unescape HTML entities, then re-escape for XML
    desc = html.escape(html.unescape(page["description"]))
    title = html.escape(html.unescape(page["title"]))
    items_xml += f"""
  <item>
    <title>{title}</title>
    <link>{page["url"]}</link>
    <guid isPermaLink="true">{page["url"]}</guid>
    <pubDate>{page["date_str"]}</pubDate>
    <description>{desc}</description>
    <category>{page["category"]}</category>
    <author>tumbleweedwords@gmail.com (David Moran)</author>
  </item>"""

feed_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>Tumbleweed Words</title>
    <link>https://tumbleweedwords.com</link>
    <atom:link href="https://tumbleweedwords.com/feed.xml" rel="self" type="application/rss+xml"/>
    <description>An independent literary publication featuring original fiction, poetry, book reviews, craft essays, and contemporary cultural commentary. Edited by David Moran in Edinburgh.</description>
    <language>en-GB</language>
    <copyright>Copyright 2026 Tumbleweed Words</copyright>
    <managingEditor>tumbleweedwords@gmail.com (David Moran)</managingEditor>
    <webMaster>tumbleweedwords@gmail.com (David Moran)</webMaster>
    <pubDate>{now_rfc822}</pubDate>
    <lastBuildDate>{now_rfc822}</lastBuildDate>
    <category>Literature</category>
    <category>Fiction</category>
    <category>Poetry</category>
    <category>Book Reviews</category>
    <category>Literary Criticism</category>
    <generator>Hand-maintained</generator>
    <image>
      <url>https://tumbleweedwords.com/tumbleweed-logo.webp</url>
      <title>Tumbleweed Words</title>
      <link>https://tumbleweedwords.com</link>
    </image>
{items_xml}
  </channel>
</rss>"""

with open(FEED_PATH, "w", encoding="utf-8") as f:
    f.write(feed_xml)

print(f"Created feed.xml with {len(recent)} items:")
for p in recent:
    print(f"  {p['date'].strftime('%Y-%m-%d')} | {p['category']} | {p['title'][:60]}")

# Add RSS link to all HTML pages
RSS_LINK = '<link rel="alternate" type="application/rss+xml" title="Tumbleweed Words RSS" href="/feed.xml">'
pages_updated = 0

for fpath in html_files:
    fname = os.path.basename(fpath)
    if fname in ("hero-banner.html", "newsletter-popup.html", "REPLACE-photo-reel.html",
                 "tagline-snippet.html", "discover.html"):
        continue

    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    if RSS_LINK not in content:
        content = content.replace("</head>", RSS_LINK + "\n</head>", 1)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        pages_updated += 1

print(f"\nAdded RSS link to {pages_updated} pages")
