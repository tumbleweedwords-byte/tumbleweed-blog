import glob, re

# Font-size bump map (18px base):
#  .48rem=8.64px  -> .61rem=10.98px (+2.3px)
#  .50rem=9.00px  -> .61rem=10.98px (+2.0px)
#  .52rem=9.36px  -> .64rem=11.52px (+2.2px)
#  .58rem=10.44px -> .70rem=12.60px (+2.2px)
SIZE_MAP = {'.48rem': '.61rem', '.5rem': '.61rem', '.52rem': '.64rem', '.58rem': '.70rem'}

modified = []

for filepath in sorted(glob.glob(r'C:\Users\tumbl\projects\tumbleewords\*.html')):
    c = open(filepath, encoding='utf-8').read()
    orig = c

    # -- 1. Bump .ft-c font-size (exact pattern match)
    def bump_ftc(m):
        rule = m.group(0)
        for old, new in SIZE_MAP.items():
            rule = rule.replace('font-size:' + old, 'font-size:' + new)
        return rule
    c = re.sub(r'\.ft-c\{font-family:var\(--fm\);font-size:[^;]+;[^}]+\}', bump_ftc, c)

    # -- 2. Bump .ft-l a font-size (exact pattern match)
    def bump_ftla(m):
        rule = m.group(0)
        for old, new in SIZE_MAP.items():
            rule = rule.replace('font-size:' + old, 'font-size:' + new)
        return rule
    c = re.sub(r'\.ft-l a\{font-family:var\(--fm\);font-size:[^;]+;[^}]+\}', bump_ftla, c)

    # -- 3. Increase .ft padding (main rule only — must have display:flex to distinguish from mobile override)
    c = c.replace('padding:1.4rem 2rem;display:flex', 'padding:2rem 2rem;display:flex')
    c = c.replace('padding:1.5rem 2rem;display:flex', 'padding:2rem 2rem;display:flex')

    # -- 4. Update disclosure <p> inline style:
    #    - Set font-size to match the (now-bumped) .ft-c size for this file
    #    - Make margin .75rem (12px+) above
    #    - Colour stays var(--fa) — same as copyright line (Change 2)
    # Find what ft-c size is now in this file
    ftc_size_match = re.search(r'\.ft-c\{[^}]*font-size:([^;]+);', c)
    if ftc_size_match:
        ftc_size = ftc_size_match.group(1)  # e.g. .61rem
    else:
        ftc_size = '.61rem'  # fallback

    # Replace disclosure <p> inline style
    old_disc = r'<p style="width:100%;margin:[^;]+;font-family:var\(--fm\);font-size:[^;]+;letter-spacing:[^;]+;color:var\(--fa\);text-align:center;">'
    new_disc = f'<p style="width:100%;margin:.75rem 0 0;font-family:var(--fm);font-size:{ftc_size};letter-spacing:.08em;color:var(--fa);text-align:center;">'
    c = re.sub(old_disc, new_disc, c)

    if c != orig:
        with open(filepath, 'w', encoding='utf-8') as fh:
            fh.write(c)
        modified.append(filepath.split('\\')[-1])
        print(f'OK: {filepath.split(chr(92))[-1]}')

print(f'\nModified: {len(modified)} files')
