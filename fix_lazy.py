import sys
sys.stdout.reconfigure(encoding='utf-8')

# Fix all-writing.html popup david.jpg
with open('all-writing.html', 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace(
    '<img class="tw-popup__photo" src="david.jpg" alt="David">',
    '<img class="tw-popup__photo" src="david.jpg" alt="David" loading="lazy">'
)
with open('all-writing.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('all-writing done.')
