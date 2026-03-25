"""
SEO schema audit fix:
1. Add image field to all pages with schema (using og:image)
2. Add datePublished where missing
3. Add dateModified to all
4. Fix author "David" → "David Moran"
5. Add schema to content pages missing it
6. Update sitemap with missing pages
"""
import sys, re, json, glob
sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = 'https://tumbleweedwords.com'
DEFAULT_IMAGE = 'https://tumbleweedwords.com/hero-1.jpg'
DATE_MODIFIED = '2026-03-24'
AUTHOR = {"@type": "Person", "name": "David Moran", "url": "https://tumbleweedwords.com/about.html", "sameAs": ["https://tumbleweedwords.substack.com"]}
PUBLISHER = {"@type": "Organization", "name": "Tumbleweed Words", "url": BASE_URL}

# Default datePublished for pages missing it (best estimate)
DEFAULT_DATES = {
    'about.html':            '2025-01-01',
    'an-expat-in-paris.html':'2025-06-01',
    'craft-theory.html':     '2025-01-01',
    'discover.html':         '2025-01-01',
    'honest-pursuit.html':   '2025-06-01',
    'reads.html':            '2025-01-01',
    'street-legal.html':     '2025-06-01',
    'index.html':            '2025-01-01',
    'all-writing.html':      '2025-01-01',
}

# Pages to add schema to (missing entirely) — skip pure utility pages
NEEDS_SCHEMA = {
    'all-writing.html':           ('CollectionPage', 'Fiction & Poetry — All Writing', '2025-01-01'),
    'famous-readings.html':       ('Article', 'Famous Author Readings', '2026-01-01'),
    'flash-fiction-prompts.html': ('WebApplication', 'Flash Fiction Prompt Generator', '2026-01-01'),
    'flash-fiction-workshop.html':('WebApplication', 'Flash Fiction Workshop — AI Analysis', '2026-01-01'),
    'literary-interviews.html':   ('Article', 'Literary Interviews', '2026-01-01'),
    'literary-magazine-finder.html':('WebApplication', 'Literary Magazine Finder', '2026-01-01'),
    'literary-style-quiz.html':   ('WebApplication', 'Literary Style Quiz — Who Do You Write Like?', '2026-01-01'),
    'podcasts.html':              ('Article', 'Literary Podcasts', '2026-01-01'),
}

# Pages missing from sitemap
MISSING_FROM_SITEMAP = [
    'best-flash-fiction-stories.html',
    'famous-readings.html',
    'how-to-write-flash-fiction.html',
    'short-fiction-examples.html',
]

updated = 0
skipped = []

for fpath in sorted(glob.glob('C:/Users/tumbl/projects/tumbleewords/*.html')):
    fname = fpath.split('/')[-1]

    # Skip pure utility pages
    if fname in {'REPLACE-photo-reel.html','hero-banner.html','newsletter-popup.html','tagline-snippet.html','search.html'}:
        continue

    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()

    # Get og:image for this page
    og_m = re.search(r'<meta property="og:image" content="([^"]+)"', c)
    page_image = og_m.group(1) if og_m else DEFAULT_IMAGE

    # Get page title
    title_m = re.search(r'<title>([^<]+)</title>', c)
    page_title = title_m.group(1).replace(' | Tumbleweed Words','').replace(' — Tumbleweed Words','').strip() if title_m else fname

    page_url = f'{BASE_URL}/{fname}'

    # ── Case 1: page already has schema ──────────────────────────────────────
    schema_m = re.search(r'<script type="application/ld\+json">(.*?)</script>', c, re.DOTALL)
    if schema_m:
        try:
            d = json.loads(schema_m.group(1))
        except json.JSONDecodeError:
            skipped.append(fname)
            continue

        changed = False

        # Add image
        if 'image' not in d:
            d['image'] = page_image
            changed = True

        # Add datePublished
        if 'datePublished' not in d:
            d['datePublished'] = DEFAULT_DATES.get(fname, '2026-01-01')
            changed = True

        # Add/update dateModified
        if d.get('dateModified') != DATE_MODIFIED:
            d['dateModified'] = DATE_MODIFIED
            changed = True

        # Fix author name
        if isinstance(d.get('author'), dict) and d['author'].get('name') == 'David':
            d['author'] = AUTHOR
            changed = True

        if changed:
            new_schema = f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>'
            c = c[:schema_m.start()] + new_schema + c[schema_m.end():]
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(c)
            updated += 1

    # ── Case 2: page needs schema added ──────────────────────────────────────
    elif fname in NEEDS_SCHEMA:
        stype, headline, pub_date = NEEDS_SCHEMA[fname]
        schema = {
            "@context": "https://schema.org",
            "@type": stype,
            "headline": headline,
            "description": page_title,
            "author": AUTHOR,
            "publisher": PUBLISHER,
            "datePublished": pub_date,
            "dateModified": DATE_MODIFIED,
            "image": page_image,
            "url": page_url,
            "mainEntityOfPage": {"@type": "WebPage", "@id": page_url}
        }
        schema_tag = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>\n'
        # Insert before </head>
        if '</head>' in c:
            c = c.replace('</head>', schema_tag + '</head>', 1)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(c)
            updated += 1
            print(f'  Schema added: {fname}')
        else:
            skipped.append(fname)

print(f'\nSchema: {updated} pages updated.')
if skipped:
    print(f'Skipped (parse error): {skipped}')

# ── Update sitemap ────────────────────────────────────────────────────────────
with open('C:/Users/tumbl/projects/tumbleewords/sitemap.xml', 'r', encoding='utf-8') as f:
    sitemap = f.read()

sitemap_updated = 0
for page in MISSING_FROM_SITEMAP:
    url = f'{BASE_URL}/{page}'
    if url not in sitemap:
        entry = f'  <url>\n    <loc>{url}</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n'
        sitemap = sitemap.replace('</urlset>', entry + '</urlset>')
        sitemap_updated += 1
        print(f'  Sitemap: added {page}')

if sitemap_updated:
    with open('C:/Users/tumbl/projects/tumbleewords/sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap)
    print(f'Sitemap: {sitemap_updated} pages added.')
else:
    print('Sitemap: already up to date.')

print('\nAll done.')
