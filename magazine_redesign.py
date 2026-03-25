"""
Magazine redesign for all-writing.html
- Section labels: editorial top-rule style (no box)
- News & Craft: magazine lead + sidebar grid
- Best Of: hero horizontal card + secondary grid
- Featured: minor spacing tweak
- All content kept, no removals
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/tumbl/projects/tumbleewords/all-writing.html', 'r', encoding='utf-8') as f:
    c = f.read()

# ─────────────────────────────────────────────────────────
# 1. Replace sec-label override in second <style> block
#    Current: purple box/badge (inline-block + border)
#    New: editorial top-rule (block + border-top only)
# ─────────────────────────────────────────────────────────
old_label_css = (
    '.sec-label{font-size:.75rem!important;display:inline-block!important;'
    'border:1.5px solid #5533E8!important;padding:.26rem .9rem!important;'
    'padding-bottom:.26rem!important;margin-bottom:2.4rem!important}'
    '.sec-eye{border:1.5px solid #5533E8!important;padding:.26rem .85rem!important;'
    'display:inline-flex!important;gap:.6rem!important}'
)
new_label_css = (
    '.sec-label{font-size:.58rem!important;display:block!important;'
    'border:none!important;border-top:2px solid #5533E8!important;'
    'padding:.8rem 0 0!important;margin-bottom:2rem!important;letter-spacing:.18em!important}'
    '.sec-eye{border:none!important;border-top:2px solid #5533E8!important;'
    'padding:.8rem 0 0!important;display:flex!important;gap:.6rem!important}'
)
if old_label_css in c:
    c = c.replace(old_label_css, new_label_css)
    print('sec-label CSS updated.')
else:
    print('WARNING: sec-label CSS not found — check string')

# ─────────────────────────────────────────────────────────
# 2. Add magazine layout CSS block before closing </style>
#    of the second style block
# ─────────────────────────────────────────────────────────
mag_css = (
    # Magazine lead+sidebar grid for News & Craft
    '.mag-grid{display:grid;grid-template-columns:3fr 2fr;'
    'grid-template-areas:"lead side1" "lead side2";'
    'border:1px solid var(--br);margin-top:0}'
    '@media(max-width:700px){'
    '.mag-grid{grid-template-columns:1fr!important;'
    'grid-template-areas:"lead""side1""side2"!important}}'
    '.mag-grid .card-img{border:none!important}'
    '.mag-grid .card-img:first-child{'
    'grid-area:lead;border-right:1px solid var(--br)!important}'
    '.mag-grid .card-img:first-child img{height:300px!important}'
    '.mag-grid .card-img:first-child .card-title{'
    'font-size:1.05rem!important;font-weight:700!important;line-height:1.22!important}'
    '.mag-grid .card-img:first-child .card-img-body{padding:1.6rem!important}'
    '.mag-grid .card-img:nth-child(2){grid-area:side1;border-bottom:1px solid var(--br)!important}'
    '.mag-grid .card-img:nth-child(3){grid-area:side2}'
    '.mag-grid .card-img:nth-child(n+2) img{height:150px!important}'
    '@media(max-width:700px){'
    '.mag-grid .card-img:first-child{border-right:none!important;border-bottom:1px solid var(--br)!important}'
    '.mag-grid .card-img:nth-child(2){border-bottom:1px solid var(--br)!important}}'

    # Best Of hero: horizontal first card
    '.bestof-hero{display:flex;border:1px solid var(--br);background:var(--bg);'
    'text-decoration:none;overflow:hidden;transition:border-color .2s;margin-bottom:1rem}'
    '.bestof-hero:hover{border-color:var(--p)}'
    '.bestof-hero-img{width:42%;min-height:230px;object-fit:cover;'
    'display:block;flex-shrink:0;filter:grayscale(8%)}'
    '.bestof-hero-body{padding:2rem 2.2rem;display:flex;flex-direction:column;gap:.6rem}'
    '.bestof-hero-eyebrow{font-family:var(--fm);font-size:.46rem;letter-spacing:.13em;'
    'text-transform:uppercase;color:var(--p)}'
    '.bestof-hero-title{font-family:var(--fd);font-size:clamp(1.1rem,2vw,1.4rem);'
    'font-weight:700;color:var(--ink);line-height:1.2}'
    '.bestof-hero-desc{font-size:.82rem;color:var(--mu);line-height:1.7;flex:1}'
    '.bestof-hero-link{font-family:var(--fm);font-size:.48rem;letter-spacing:.1em;'
    'text-transform:uppercase;color:var(--p);margin-top:.3rem}'
    '.bestof-sub-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem}'
    '@media(max-width:700px){.bestof-sub-grid{grid-template-columns:repeat(2,1fr)}}'
    '@media(max-width:450px){.bestof-sub-grid{grid-template-columns:1fr}}'
    '@media(max-width:600px){'
    '.bestof-hero{flex-direction:column}'
    '.bestof-hero-img{width:100%;min-height:190px}'
    '.bestof-hero-body{padding:1.4rem}}'
)

# Insert before closing of second style block (before @media(max-width:800px))
insert_before = '@media(max-width:800px){.hide-m{display:none!important}}'
if insert_before in c:
    c = c.replace(insert_before, mag_css + insert_before)
    print('Magazine CSS inserted.')
else:
    print('WARNING: insertion point not found')

# ─────────────────────────────────────────────────────────
# 3. News & Craft: change card-grid class to mag-grid
# ─────────────────────────────────────────────────────────
# News section
c = c.replace(
    '<!-- NEWS & CULTURE -->\n<section class="sec" id="news">\n<div class="sec-inner">\n'
    '<div class="sec-label">News &amp; Culture</div>\n'
    '<div class="card-grid card-grid-3">',
    '<!-- NEWS & CULTURE -->\n<section class="sec" id="news">\n<div class="sec-inner">\n'
    '<div class="sec-label">News &amp; Culture</div>\n'
    '<div class="mag-grid">'
)
# Craft section
c = c.replace(
    '<!-- CRAFT -->\n<section class="sec sec-alt" id="craft">\n<div class="sec-inner">\n'
    '<div class="sec-label">Craft &amp; Theory</div>\n'
    '<div class="card-grid card-grid-3">',
    '<!-- CRAFT -->\n<section class="sec sec-alt" id="craft">\n<div class="sec-inner">\n'
    '<div class="sec-label">Craft &amp; Theory</div>\n'
    '<div class="mag-grid">'
)
print('News & Craft grids converted to mag-grid.')

# ─────────────────────────────────────────────────────────
# 4. Best Of: first card becomes horizontal hero
#    Remaining 7 wrapped in bestof-sub-grid
# ─────────────────────────────────────────────────────────
# The hero card is "three-nomadic-poems" (first in list)
old_bestof_section = (
    '<div class="bestof-grid">\n'
    '<a href="https://tumbleweedwords.substack.com/p/three-nomadic-poems" class="bestof-card" target="_blank" rel="noopener" style="color:inherit;text-decoration:none;">'
    '<img src="IMG_20150317_132854.jpg" alt="Buenos Aires waterfront skyline \u2014 nomadic poem by David Moran" class="bestof-img" loading="lazy">'
    '<span class="bestof-type">Poetry &middot; Buenos Aires</span>'
    '<div class="bestof-title">nomadic | poem</div>'
    '<div class="bestof-desc">Written on a plane while flying away from love and loss. &ldquo;The final act of a born run away, moving through the world at good speed.&rdquo;</div>'
    '<span class="bestof-link">Read &rarr;</span></a>\n'
)
new_bestof_hero = (
    # Hero card (horizontal)
    '<a href="https://tumbleweedwords.substack.com/p/three-nomadic-poems" class="bestof-hero" target="_blank" rel="noopener" style="color:inherit">'
    '<img src="IMG_20150317_132854.jpg" alt="Buenos Aires waterfront skyline \u2014 nomadic poem by David Moran" class="bestof-hero-img" loading="lazy">'
    '<div class="bestof-hero-body">'
    '<span class="bestof-hero-eyebrow">Poetry &middot; Buenos Aires</span>'
    '<div class="bestof-hero-title">nomadic | poem</div>'
    '<div class="bestof-hero-desc">Written on a plane while flying away from love and loss. &ldquo;The final act of a born run away, moving through the world at good speed.&rdquo;</div>'
    '<span class="bestof-hero-link">Read &rarr;</span>'
    '</div></a>\n'
    # Secondary grid starts
    '<div class="bestof-sub-grid">\n'
)

# Also need to close bestof-sub-grid before </div></div></section>
old_bestof_close = '</div>\n</div>\n</section>'  # closes bestof-grid, sec-inner, sec
new_bestof_close = '</div>\n</div>\n</div>\n</section>'  # closes bestof-sub-grid too

if old_bestof_section in c:
    c = c.replace(old_bestof_section, new_bestof_hero)
    print('Best Of hero card inserted.')
else:
    print('WARNING: bestof hero target not found — check HTML whitespace')

# Close the bestof-sub-grid: find the end of bestof section
# The bestof section ends at: </div>\n</div>\n</section>\n\n<!-- TOOLS
old_end = '</div>\n</div>\n</section>\n\n<!-- TOOLS'
new_end = '</div>\n</div>\n</div>\n</section>\n\n<!-- TOOLS'
if old_end in c:
    c = c.replace(old_end, new_end, 1)  # only first occurrence (bestof section)
    print('bestof-sub-grid closed.')
else:
    print('WARNING: bestof close not found')

with open('C:/Users/tumbl/projects/tumbleewords/all-writing.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('\nAll done — saved.')
