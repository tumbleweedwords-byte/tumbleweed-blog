import re, os

TARGET_FILES = [
    # Fiction & Poetry — internal site pages
    "a-man-with-no-purpose.html",
    "women-who-want-a-man.html",
    "street-legal.html",
    "an-expat-in-paris.html",
    "honest-pursuit.html",
    "viral-poetry.html",
    # Book Reviews — book reviews
    "2026-international-booker-prize-shortlist.html",
    "2026-womens-prize-for-fiction-shortlist-prediction.html",
    "baudelaire-flowers-evil-review.html",
    "best-book-to-film-adaptations.html",
    "best-books-if-you-like-carver.html",
    "best-debut-novels-2026.html",
    "best-flash-fiction-2025.html",
    "best-flash-fiction-stories.html",
    "bukowski-love-dog-hell-review.html",
    "camus-outsider-review.html",
    "deborah-levy-gertrude-stein-review.html",
    "doris-lessing-fifth-child-review.html",
    "five-memoirs-to-read-before-you-die.html",
    "george-saunders-vigil-review.html",
    "gwendoline-riley-palm-house-review.html",
    "hemingway-old-man-sea-review.html",
    "james-baldwin-another-country-review.html",
    "john-fante-ask-the-dust-review.html",
    "kate-riley-ruth-review.html",
    "kevin-young-night-watch-review.html",
    "literary-interviews.html",
    "murakami-norwegian-wood-review.html",
    "ocean-vuong-emperor-of-gladness-review.html",
    "ocean-vuong-reading-guide.html",
    "poppick-the-copywriter-review.html",
    "post-literary-magazines.html",
    "richie-hofmann-bronze-arms-review.html",
    "short-fiction-examples.html",
    "tara-menon-under-water-review.html",
    "top-10-poetry-collections-to-read.html",
    "virginia-evans-the-correspondent-review.html",
    "what-i-am-reading.html",
    "women-who-changed-the-sentence.html",
    # City / place pieces
    "fiction-set-in-prague.html",
    "fiction-set-in-buenos-aires.html",
    "fiction-set-in-istanbul.html",
    "flash-fiction-about-trains.html",
    "flash-fiction-about-memory.html",
    "flash-fiction-about-strangers.html",
    "flash-fiction-prague.html",
    "flash-fiction-buenos-aires.html",
    "flash-fiction-istanbul.html",
]

NEW_CTA_SECTION = '''<section class="cta-sec">
<div class="cta-inner">
<h2>A slice of flash or poetry<br><em style="color:var(--p);font-style:normal">Sent from everywhere</em></h2>
<form class="inline-sub" action="https://tumbleweedwords.substack.com/api/v1/free" method="post" target="_blank"><input class="inline-sub__input" type="email" name="email" placeholder="Your email address" required autocomplete="email"><button class="inline-sub__btn" type="submit">Subscribe free &rarr;</button></form>
<p style="font-family:var(--fm);font-size:.46rem;letter-spacing:.1em;text-transform:uppercase;color:var(--fa);margin-top:.7rem">Free &middot; Weekly &middot; No spam &middot; Unsubscribe any time</p>
</div>
</section>'''

EXTRA_CSS = '<style>.cta-sec{background:#fff;padding:4.5rem 2rem;text-align:center;border-top:2px solid var(--p)}.cta-inner{max-width:580px;margin:0 auto}.cta-sec h2{font-family:var(--fd);font-size:clamp(1.3rem,2.8vw,1.8rem);font-weight:700;margin-bottom:.8rem;line-height:1.15}.inline-sub{display:flex;gap:.5rem;max-width:420px;margin:.6rem auto 0}.inline-sub__input{flex:1;background:#fff;border:1.5px solid #D4D0C4;color:#1a1820;font-family:var(--fb);font-size:.78rem;padding:.7rem 1rem;outline:none;transition:border-color .2s}.inline-sub__input:focus{border-color:var(--p)}.inline-sub__input::placeholder{color:#C4C0B0}.inline-sub__btn{background:var(--p);color:#fff;font-family:var(--fm);font-size:.56rem;letter-spacing:.1em;text-transform:uppercase;padding:.7rem 1.2rem;border:none;cursor:pointer;transition:background .15s;white-space:nowrap}.inline-sub__btn:hover{background:var(--p2)}</style>\n'

updated = []
skipped = []
errors = []

for fname in TARGET_FILES:
    if not os.path.exists(fname):
        errors.append(f"NOT FOUND: {fname}")
        continue

    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changed = False

    def needs_css(c):
        return '.cta-sec' not in c

    def replacement_block(c):
        return (EXTRA_CSS if needs_css(c) else '') + NEW_CTA_SECTION

    # Pattern 1: cband section
    m = re.search(r'<section class="cband"[^>]*>.*?</section>', content, re.DOTALL)
    if m:
        content = content[:m.start()] + replacement_block(content) + content[m.end():]
        changed = True

    # Pattern 2: old cta-sec (class-based, old heading)
    m = re.search(r'<section class="cta-sec"[^>]*>.*?</section>', content, re.DOTALL)
    if m:
        old = m.group(0)
        if 'A slice of flash or poetry' not in old:
            content = content[:m.start()] + NEW_CTA_SECTION + content[m.end():]
            content = content.replace(
                '.cta-sec{background:var(--bg2);',
                '.cta-sec{background:#fff;'
            )
            changed = True

    # Pattern 3: inline-styled section containing the Substack subscribe form
    m = re.search(
        r'<section style="[^"]*"[^>]*>(?:(?!</section>).)*substack\.com/api/v1/free(?:(?!</section>).)*</section>',
        content, re.DOTALL
    )
    if m:
        content = content[:m.start()] + replacement_block(content) + content[m.end():]
        changed = True

    if changed:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
        updated.append(fname)
    else:
        skipped.append(fname)

print(f"\nUpdated ({len(updated)}):")
for f in updated:
    print(f"  {f}")
print(f"\nSkipped - no old pattern / already updated ({len(skipped)}):")
for f in skipped:
    print(f"  {f}")
if errors:
    print(f"\nErrors ({len(errors)}):")
    for e in errors:
        print(f"  {e}")
