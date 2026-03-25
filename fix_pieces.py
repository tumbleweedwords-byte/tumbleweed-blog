import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/tumbl/projects/tumbleewords/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the pieces CSS
old_css = '.pieces-sec{background:var(--bg2);padding:7rem 2rem;border-bottom:1px solid var(--br)}.pieces-inner{max-width:1100px;margin:0 auto}.pieces-grid{display:grid;grid-template-columns:1fr 1fr;border-radius:4px;overflow:hidden;margin-top:1.5rem}@media(max-width:600px){.pieces-grid{grid-template-columns:1fr}}.piece-card{padding:2rem;border-right:1px solid rgba(255,255,255,.15);border-bottom:1px solid rgba(255,255,255,.15);display:flex;flex-direction:column;gap:.5rem;background-size:cover;background-position:center;position:relative;transition:all .3s;min-height:200px}.piece-card::before{content:"";position:absolute;inset:0;background:rgba(20,14,30,.44);transition:background .3s}.piece-card:hover::before{background:rgba(20,14,30,.34)}.piece-card:nth-child(even)::before{background:rgba(20,14,30,.62)}.piece-card:nth-child(even):hover::before{background:rgba(20,14,30,.52)}.piece-card:nth-child(4)::before{background:rgba(20,14,30,.78)}.piece-card:nth-child(4):hover::before{background:rgba(20,14,30,.68)}.piece-card>*{position:relative;z-index:2}.piece-card:nth-child(even){border-right:none}.piece-card:nth-last-child(-n+2){border-bottom:none}.pc-city{font-family:var(--fm);font-size:.46rem;letter-spacing:.13em;text-transform:uppercase;color:rgba(255,255,255,.9);text-shadow:0 1px 6px rgba(0,0,0,.7)}.pc-line{font-family:var(--fd);font-size:.88rem;font-style:italic;font-weight:700;color:#fff;line-height:1.55;flex:1;text-shadow:0 1px 8px rgba(0,0,0,.8),0 2px 16px rgba(0,0,0,.5)}.pc-meta{font-family:var(--fm);font-size:.46rem;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.85);text-shadow:0 1px 6px rgba(0,0,0,.7)}'

new_css = '.pieces-sec{background:var(--bg2);padding:7rem 2rem;border-bottom:1px solid var(--br)}.pieces-inner{max-width:1100px;margin:0 auto}.pieces-grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1.5rem}@media(max-width:600px){.pieces-grid{grid-template-columns:1fr}}.piece-card{background:var(--bg);border:1px solid var(--br);display:flex;flex-direction:column;text-decoration:none;overflow:hidden;transition:border-color .2s}.piece-card:hover{border-color:var(--p)}.pc-img{width:100%;height:200px;object-fit:cover;display:block;filter:grayscale(8%)}.pc-body{padding:1.4rem;display:flex;flex-direction:column;gap:.5rem}.pc-city{font-family:var(--fm);font-size:.46rem;letter-spacing:.13em;text-transform:uppercase;color:var(--p)}.pc-line{font-family:var(--fd);font-size:.9rem;font-style:italic;color:var(--ink);line-height:1.6}.pc-meta{font-family:var(--fm);font-size:.46rem;letter-spacing:.08em;text-transform:uppercase;color:var(--mu)}'

if old_css in content:
    content = content.replace(old_css, new_css)
    print('CSS replaced.')
else:
    print('ERROR: old CSS not found')

# 2. Rebuild each piece-card: remove background-image inline style, add <img>, wrap text in pc-body
# Cards and their image sources
cards = [
    ("card-berlin.jpg", "Berlin U-Bahn in winter"),
    ("card-london.jpg", "London Whitechapel street"),
    ("card-england.jpg", "English council estate"),
    ("IMG_20251030_115310956.jpg", "Buenos Aires leaving"),
]

# Replace each card
replacements = [
    # Berlin
    (
        '<a href="https://tumbleweedwords.substack.com/p/street-legal-fiction" class="piece-card" target="_blank" rel="noopener" style="color:inherit;text-decoration:none;background-image:url(\'card-berlin.jpg\')"><span class="pc-city">Berlin &mdash; U-Bahn, winter</span><p class="pc-line">&ldquo;Everyone wears black so hard you don&rsquo;t notice after a while that there are differing shades.&rdquo;</p><span class="pc-meta">train in vain &middot; fiction</span></a>',
        '<a href="https://tumbleweedwords.substack.com/p/street-legal-fiction" class="piece-card" target="_blank" rel="noopener" style="color:inherit"><img src="card-berlin.jpg" alt="Berlin U-Bahn in winter" class="pc-img" loading="lazy"><div class="pc-body"><span class="pc-city">Berlin &mdash; U-Bahn, winter</span><p class="pc-line">&ldquo;Everyone wears black so hard you don&rsquo;t notice after a while that there are differing shades.&rdquo;</p><span class="pc-meta">train in vain &middot; fiction</span></div></a>'
    ),
    # London
    (
        '<a href="https://tumbleweedwords.substack.com/p/a-conversation-between-two-city-dwelling" class="piece-card" target="_blank" rel="noopener" style="color:inherit;text-decoration:none;background-image:url(\'card-london.jpg\')"><span class="pc-city">London &mdash; Whitechapel, summer</span><p class="pc-line">&ldquo;You&rsquo;re not a serious person anymore, Gabriel. Was I ever? Before the drink, yes.&rdquo;</p><span class="pc-meta">two city dwelling lovers &middot; fiction</span></a>',
        '<a href="https://tumbleweedwords.substack.com/p/a-conversation-between-two-city-dwelling" class="piece-card" target="_blank" rel="noopener" style="color:inherit"><img src="card-london.jpg" alt="London Whitechapel street in summer" class="pc-img" loading="lazy"><div class="pc-body"><span class="pc-city">London &mdash; Whitechapel, summer</span><p class="pc-line">&ldquo;You&rsquo;re not a serious person anymore, Gabriel. Was I ever? Before the drink, yes.&rdquo;</p><span class="pc-meta">two city dwelling lovers &middot; fiction</span></div></a>'
    ),
    # England
    (
        '<a href="https://tumbleweedwords.substack.com/p/growing-pains-fiction" class="piece-card" target="_blank" rel="noopener" style="color:inherit;text-decoration:none;background-image:url(\'card-england.jpg\')"><span class="pc-city">A council estate, England</span><p class="pc-line">&ldquo;Because our dads liked to get pissed up at the pub and smash things when home, there wasn&rsquo;t much money left to go round.&rdquo;</p><span class="pc-meta">growing pains &middot; published internationally</span></a>',
        '<a href="https://tumbleweedwords.substack.com/p/growing-pains-fiction" class="piece-card" target="_blank" rel="noopener" style="color:inherit"><img src="card-england.jpg" alt="English council estate" class="pc-img" loading="lazy"><div class="pc-body"><span class="pc-city">A council estate, England</span><p class="pc-line">&ldquo;Because our dads liked to get pissed up at the pub and smash things when home, there wasn&rsquo;t much money left to go round.&rdquo;</p><span class="pc-meta">growing pains &middot; published internationally</span></div></a>'
    ),
    # Buenos Aires
    (
        '<a href="https://tumbleweedwords.substack.com/p/three-nomadic-poems" class="piece-card" target="_blank" rel="noopener" style="color:inherit;text-decoration:none;background-image:url(\'IMG_20251030_115310956.jpg\')"><span class="pc-city">Buenos Aires &mdash; leaving</span><p class="pc-line">&ldquo;On a plane, on a plane rising the hostess refuses to smile.&rdquo;</p><span class="pc-meta">nomadic &middot; poetry</span></a>',
        '<a href="https://tumbleweedwords.substack.com/p/three-nomadic-poems" class="piece-card" target="_blank" rel="noopener" style="color:inherit"><img src="IMG_20251030_115310956.jpg" alt="Buenos Aires, leaving" class="pc-img" loading="lazy"><div class="pc-body"><span class="pc-city">Buenos Aires &mdash; leaving</span><p class="pc-line">&ldquo;On a plane, on a plane rising the hostess refuses to smile.&rdquo;</p><span class="pc-meta">nomadic &middot; poetry</span></div></a>'
    ),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f'Card replaced.')
    else:
        print(f'WARNING: card not found')

with open('C:/Users/tumbl/projects/tumbleewords/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done.')
