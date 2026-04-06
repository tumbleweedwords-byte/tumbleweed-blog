import glob

SWAPS = [
    ('city-buenos-aires.jpg', 'city-buenos-aires.webp'),
    ('city-istanbul.jpg',     'city-istanbul.webp'),
    ('city-prague.jpg',       'city-prague.webp'),
    ('david.jpg',             'david.webp'),
    ('hero-1.jpg',            'hero-1.webp'),
    ('howl.jpg',              'howl.webp'),
    ('lake-bled.jpg',         'lake-bled.webp'),
    ('paris-bookshop.jpg',    'paris-bookshop.webp'),
    ('quote-bg.jpg',          'quote-bg.webp'),
    ('scotland-coast.jpg',    'scotland-coast.webp'),
    ('viral-poetry.jpg',      'viral-poetry.webp'),
]

modified = []

for filepath in sorted(glob.glob(r'C:\Users\tumbl\projects\tumbleewords\*.html')):
    with open(filepath, encoding='utf-8') as f:
        c = f.read()
    orig = c
    for old, new in SWAPS:
        c = c.replace(old, new)
    if c != orig:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(c)
        modified.append(filepath.split('\\')[-1])

print(f'Modified: {len(modified)} files')
for f in modified:
    print(f'  {f}')
