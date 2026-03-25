import os, re

BASE = 'C:/Users/tumbl/projects/tumbleewords'

# Image CSS to inject once into each page's <style> block
IMG_CSS = (
  '.book-cover{float:right;margin:0 0 1.4rem 2rem;max-width:170px;width:100%;'
  'box-shadow:0 4px 20px rgba(26,24,32,.18);border-radius:3px;display:block}'
  '@media(max-width:600px){.book-cover{float:none;margin:0 auto 1.6rem;max-width:140px}}'
)

# Map: filename -> (image src, alt text)
REVIEWS = {
  'ocean-vuong-emperor-of-gladness-review.html': (
    'VUONG.jpg',
    'The Emperor of Gladness by Ocean Vuong — book cover'
  ),
  'richie-hofmann-bronze-arms-review.html': (
    'hoffman.jpg',
    'The Bronze Arms by Richie Hofmann — book cover'
  ),
  'tara-menon-under-water-review.html': (
    'under water.jpg',
    'Under Water by Tara Menon — book cover'
  ),
  'kevin-young-night-watch-review.html': (
    'night watch.jpg',
    'Night Watch by Kevin Young — book cover'
  ),
  'kate-riley-ruth-review.html': (
    'kate riley.jpg',
    'Ruth by Kate Riley — book cover'
  ),
}

for fname, (img, alt) in REVIEWS.items():
    path = os.path.join(BASE, fname)
    with open(path, encoding='utf-8') as f:
        html = f.read()

    # Inject CSS before closing </style> of the second style block (byline style)
    # Find last </style> before <body> close and inject before it
    html = html.replace(
        '.byline{font-family:ui-monospace',
        IMG_CSS + '.byline{font-family:ui-monospace',
        1
    )

    # Insert <img> after the standfirst paragraph, before <div class="body">
    img_tag = f'<img src="{img}" alt="{alt}" class="book-cover" loading="lazy">\n  '
    html = html.replace(
        '  <div class="body">',
        f'  {img_tag}<div class="body">',
        1
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  Updated: {fname}')

# --- Remove Poor (Nelson) ---
nelson_file = os.path.join(BASE, 'caleb-azumah-nelson-poor-review.html')
if os.path.exists(nelson_file):
    os.remove(nelson_file)
    print('  Deleted: caleb-azumah-nelson-poor-review.html')

# Remove from all-writing.html
aw = os.path.join(BASE, 'all-writing.html')
with open(aw, encoding='utf-8') as f:
    aw_html = f.read()

aw_html = re.sub(
    r'\n<a href="/caleb-azumah-nelson-poor-review\.html"[^>]*>.*?</a>',
    '',
    aw_html
)
with open(aw, 'w', encoding='utf-8') as f:
    f.write(aw_html)
print('  Removed Nelson from all-writing.html')

# Remove from sitemap.xml
sm = os.path.join(BASE, 'sitemap.xml')
with open(sm, encoding='utf-8') as f:
    sm_xml = f.read()

sm_xml = re.sub(
    r'\s*<url>\s*<loc>[^<]*caleb-azumah-nelson-poor[^<]*</loc>.*?</url>',
    '',
    sm_xml,
    flags=re.DOTALL
)
with open(sm, 'w', encoding='utf-8') as f:
    f.write(sm_xml)
print('  Removed Nelson from sitemap.xml')

print('\nDone.')
