import os
import glob

BOOKSHOP_LINK = '<a href="https://uk.bookshop.org/shop/tumbleweedwords" target="_blank" rel="noopener">Browse the bookshop</a>'
DISCLOSURE = '<p style="width:100%;margin:.5rem 0 0;font-family:var(--fm);font-size:.42rem;letter-spacing:.05em;color:var(--fa);text-align:center;">Tumbleweed Words is a Bookshop.org affiliate. Book links on this site earn a small commission that supports the work, at no extra cost to you.</p>'

modified = []
skipped = []

html_files = glob.glob(r'C:\Users\tumbl\projects\tumbleewords\*.html')

for filepath in sorted(html_files):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already modified
    if 'uk.bookshop.org/shop/tumbleweedwords' in content:
        skipped.append(os.path.basename(filepath))
        continue

    # Must have footer nav
    if 'class="ft-l"' not in content:
        print(f"SKIP (no ft-l): {os.path.basename(filepath)}")
        continue

    original = content

    # Step 1: Insert bookshop link before </nav> inside footer
    # Find the ft-l nav, then find its closing </nav>
    nav_start = content.find('<nav class="ft-l"')
    if nav_start == -1:
        print(f"SKIP (nav not found): {os.path.basename(filepath)}")
        continue

    nav_end = content.find('</nav>', nav_start)
    if nav_end == -1:
        print(f"SKIP (</nav> not found): {os.path.basename(filepath)}")
        continue

    # Insert bookshop link before </nav>
    # Check if there's whitespace/newline before </nav> for formatting
    insert_pos = nav_end
    # Peek at what's before </nav>
    before_nav_close = content[nav_start:nav_end]
    if '\n' in before_nav_close:
        # Multi-line format: add with same indentation as other links
        # Find last newline before </nav>
        last_newline = content.rfind('\n', nav_start, nav_end)
        indent = ''
        pos = last_newline + 1
        while pos < nav_end and content[pos] in (' ', '\t'):
            indent += content[pos]
            pos += 1
        content = content[:nav_end] + indent + BOOKSHOP_LINK + '\n' + content[nav_end:]
    else:
        # Single-line format: just insert before </nav>
        content = content[:nav_end] + BOOKSHOP_LINK + content[nav_end:]

    # Step 2: Insert disclosure before </footer>
    # Find </footer> after the nav we just modified
    footer_end = content.find('</footer>', nav_start)
    if footer_end == -1:
        print(f"SKIP (</footer> not found): {os.path.basename(filepath)}")
        content = original  # revert
        continue

    # Check if multi-line footer
    footer_section = content[nav_start:footer_end]
    if '\n' in footer_section:
        # Multi-line: add disclosure on its own line before </footer>
        last_newline = content.rfind('\n', nav_start, footer_end)
        indent = ''
        pos = last_newline + 1
        while pos < footer_end and content[pos] in (' ', '\t'):
            indent += content[pos]
            pos += 1
        content = content[:footer_end] + indent + DISCLOSURE + '\n' + content[footer_end:]
    else:
        # Single-line: insert directly before </footer>
        content = content[:footer_end] + DISCLOSURE + content[footer_end:]

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        modified.append(os.path.basename(filepath))
        print(f"OK: {os.path.basename(filepath)}")

print(f"\nModified: {len(modified)} files")
print(f"Already done (skipped): {len(skipped)} files")
if modified:
    print("\nModified files:")
    for f in modified:
        print(f"  {f}")
