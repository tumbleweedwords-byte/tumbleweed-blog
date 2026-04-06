import glob, re

# ── SEO CHANGES (5 priority pages) ──────────────────────────────────────────

SEO_CHANGES = {
    'what-is-flash-fiction.html': {
        'title_old': 'What Is Flash Fiction? Definition, History, and Complete Guide | Tumbleweed Words',
        'title_new': 'What Is Flash Fiction? Complete Guide | Tumbleweed Words',
        # desc is 152 chars and fine — no change needed
    },
    'how-to-write-flash-fiction.html': {
        'title_old': 'How to Write Flash Fiction: A Working Writer&rsquo;s Guide | Tumbleweed Words',
        'title_new': 'How to Write Flash Fiction | Tumbleweed Words',
        # desc is 142 chars — fine
    },
    'what-is-dirty-realism.html': {
        'title_old': 'What Is Dirty Realism? The American Short Story at Its Most Honest | Tumbleweed Words',
        'title_new': 'What Is Dirty Realism? The Complete Guide | Tumbleweed Words',
        # desc is 150 chars — fine
    },
    'best-flash-fiction-collections.html': {
        'title_old': 'The Best Flash Fiction Collections of All Time | Tumbleweed Words',
        'title_new': 'Best Flash Fiction Collections | Tumbleweed Words',
        'desc_old': 'The definitive list of flash fiction collections. From Amy Hempel and Raymond Carver to Carmen Maria Machado and Nana Kwame Adjei-Brenyah. Fifteen essential books for readers and writers.',
        'desc_new': 'The definitive list of flash fiction collections. Amy Hempel, Raymond Carver, Carmen Maria Machado. Fifteen essential books for readers and writers.',
    },
    'flash-fiction-vs-short-story.html': {
        'title_old': 'Flash Fiction vs Short Story: The Real Differences | Tumbleweed Words',
        'title_new': 'Flash Fiction vs Short Story | Tumbleweed Words',
        # desc is 149 chars — fine
    },
}

seo_modified = []
for filename, changes in SEO_CHANGES.items():
    with open(filename, encoding='utf-8') as f:
        c = f.read()
    orig = c
    c = c.replace(f'<title>{changes["title_old"]}</title>',
                  f'<title>{changes["title_new"]}</title>')
    if 'desc_old' in changes:
        c = c.replace(
            f'content="{changes["desc_old"]}"',
            f'content="{changes["desc_new"]}"'
        )
    if c != orig:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(c)
        seo_modified.append(filename)
        print(f'SEO OK: {filename}')

# ── NAV: ADD TOOLS LINK ──────────────────────────────────────────────────────

TOOLS_LINK_DESKTOP = '<a href="/essays-and-culture.html#tools" class="nlink hide-m">Tools</a>'
TOOLS_LINK_MOBILE  = '<a href="/essays-and-culture.html#tools">Tools</a>'

# Desktop nav — insert after FAQ link (two variants observed)
FAQ_DESKTOP = '<a href="/faq.html" class="nlink hide-m">FAQ</a>'
# Mobile menu — insert after FAQ link
FAQ_MOBILE  = '<a href="/faq.html">FAQ</a>'

nav_modified = []
already_done = []

for filepath in sorted(glob.glob('*.html')):
    with open(filepath, encoding='utf-8') as f:
        c = f.read()
    orig = c

    if TOOLS_LINK_DESKTOP in c:
        already_done.append(filepath)
        continue

    if FAQ_DESKTOP in c:
        c = c.replace(FAQ_DESKTOP, FAQ_DESKTOP + TOOLS_LINK_DESKTOP)

    if FAQ_MOBILE in c:
        c = c.replace(FAQ_MOBILE, FAQ_MOBILE + TOOLS_LINK_MOBILE)

    if c != orig:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(c)
        nav_modified.append(filepath)
        print(f'NAV OK: {filepath}')

print(f'\nSEO changes: {len(seo_modified)} files')
print(f'Nav changes: {len(nav_modified)} files')
if already_done:
    print(f'Nav already present (skipped): {len(already_done)} files')
