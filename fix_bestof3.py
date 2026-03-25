import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/tumbl/projects/tumbleewords/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_section = (
    '<section class="bestof-sec"><div class="bestof-inner">'
    '<div class="sec-label">Best Of &middot; Handpicked Fiction &amp; Poetry</div>'
    '<h2>Original work. <em>Twenty years</em> on the road.</h2>'
    '<p class="sec-sub">The most read and most loved pieces from twenty years of Tumbleweed Words. Published internationally. Start here.</p>'
    '<div class="bestof-grid">'
    '<a href="https://tumbleweedwords.substack.com/p/three-nomadic-poems" class="bestof-card" target="_blank" rel="noopener" style="color:inherit">'
    '<img src="IMG_20150317_132854.jpg" alt="Buenos Aires waterfront skyline \u2014 nomadic poem by David Moran" class="bestof-img" loading="lazy">'
    '<span class="bestof-type">Poetry &middot; Buenos Aires</span>'
    '<div class="bestof-title">nomadic | poem</div>'
    '<div class="bestof-desc">Written on a plane while flying away from love and loss. \u201cThe final act of a born run away, moving through the world at good speed.\u201d</div>'
    '<span class="bestof-link">Read &rarr;</span></a>'
    '<a href="/street-legal.html" class="bestof-card" style="color:inherit">'
    '<img src="IMG_0175.JPG" alt="City street at night \u2014 flash fiction from Berlin by David Moran" class="bestof-img" loading="lazy">'
    '<span class="bestof-type">Fiction &middot; Berlin</span>'
    '<div class="bestof-title">train in vain | short fiction</div>'
    '<div class="bestof-desc">Written on a train watching a passing stranger exit my life. Pushcart Prize nominated.</div>'
    '<span class="bestof-link">Read &rarr;</span></a>'
    '<a href="https://tumbleweedwords.substack.com/p/growing-pains-fiction" class="bestof-card" target="_blank" rel="noopener" style="color:inherit">'
    '<img src="IMG_0355.JPG" alt="Urban rooftop silhouette with dramatic sky \u2014 fiction set in England by David Moran" class="bestof-img" loading="lazy">'
    '<span class="bestof-type">Fiction &middot; England</span>'
    '<div class="bestof-title">growing pains | fiction</div>'
    '<div class="bestof-desc">Published in New York and Lisbon. Shortlisted for a Pushcart Prize nomination.</div>'
    '<span class="bestof-link">Read &rarr;</span></a>'
    '<a href="https://tumbleweedwords.substack.com/p/you-wanting-anything-from-the-shops" class="bestof-card" target="_blank" rel="noopener" style="color:inherit">'
    '<img src="IMG_20221001_094917117.jpg" alt="Scottish Highland road \u2014 poem from Glasgow by David Moran" class="bestof-img" loading="lazy">'
    '<span class="bestof-type">Poetry &middot; Glasgow</span>'
    '<div class="bestof-title">wanting anything from the shops?</div>'
    '<div class="bestof-desc">A poem set in Glasgow. Capturing the working class tone and lives of locals.</div>'
    '<span class="bestof-link">Read &rarr;</span></a>'
    '<a href="https://tumbleweedwords.substack.com/p/indescretion-poem" class="bestof-card" target="_blank" rel="noopener" style="color:inherit">'
    '<img src="IMG_0113.JPG" alt="Harbour reflected in still water \u2014 poem by David Moran, Tumbleweed Words" class="bestof-img" loading="lazy">'
    '<span class="bestof-type">Poetry &middot; International</span>'
    '<div class="bestof-title">indiscretions | poem</div>'
    '<div class="bestof-desc">An internationally published poem about the memory of growing up.</div>'
    '<span class="bestof-link">Read &rarr;</span></a>'
    '<a href="/an-expat-in-paris.html" class="bestof-card" style="color:inherit">'
    '<img src="P1040311.JPG" alt="European courtyard looking up \u2014 essay on Paris and James Baldwin by David Moran" class="bestof-img" loading="lazy">'
    '<span class="bestof-type">Essay &middot; James Baldwin</span>'
    '<div class="bestof-title">an expat in paris</div>'
    '<div class="bestof-desc">On Baldwin\u2019s Giovanni\u2019s Room, expatriate life, and what it means to write honestly about desire and exile.</div>'
    '<span class="bestof-link">Read &rarr;</span></a>'
    '<a href="/honest-pursuit.html" class="bestof-card" style="color:inherit">'
    '<img src="IMG_20190418_152257_016.jpg" alt="Hampi temple, India \u2014 literary manifesto by David Moran, Tumbleweed Words" class="bestof-img" loading="lazy">'
    '<span class="bestof-type">Essay &middot; Manifesto</span>'
    '<div class="bestof-title">an honest pursuit</div>'
    '<div class="bestof-desc">A literary writer\u2019s manifesto. What the work is for and why it matters to keep writing badly before writing well.</div>'
    '<span class="bestof-link">Read &rarr;</span></a>'
    '<a href="https://tumbleweedwords.substack.com/p/most-read-tumbleweed-words-shares" class="bestof-card" target="_blank" rel="noopener" style="color:inherit">'
    '<img src="P1020216.JPG" alt="Seoul Han River at dusk \u2014 best of Tumbleweed Words" class="bestof-img" loading="lazy">'
    '<span class="bestof-type">Collection</span>'
    '<div class="bestof-title">explore the best of</div>'
    '<div class="bestof-desc">Handpicked stories and poems from the most popular newsletters over twenty years.</div>'
    '<span class="bestof-link">Browse all &rarr;</span></a>'
    '</div></div></section>'
)

new_section = (
    '<section class="bestof-sec"><div class="bestof-inner">'
    '<div class="sec-label">Best Of &middot; Handpicked Fiction &amp; Poetry</div>'
    '<h2>Original work. <em>Twenty years</em> on the road.</h2>'
    '<p class="sec-sub">The most read and most loved pieces from twenty years of Tumbleweed Words. Published internationally. Start here.</p>'
    '<div class="bestof-grid">'

    '<a href="/street-legal.html" class="bestof-card" style="color:inherit">'
    '<img src="IMG_0175.JPG" alt="Night street lights through rain \u2014 train in vain, flash fiction by David Moran" class="bestof-img" loading="lazy">'
    '<span class="bestof-type">Fiction &middot; Berlin</span>'
    '<div class="bestof-title">train in vain | short fiction</div>'
    '<div class="bestof-desc">Written on a Berlin U-Bahn watching a passing stranger exit my life. Pushcart Prize nominated.</div>'
    '<span class="bestof-link">Read &rarr;</span></a>'

    '<a href="/an-expat-in-paris.html" class="bestof-card" style="color:inherit">'
    '<img src="P1040311.JPG" alt="Looking up through a European courtyard \u2014 an expat in paris, essay by David Moran" class="bestof-img" loading="lazy">'
    '<span class="bestof-type">Essay &middot; James Baldwin</span>'
    '<div class="bestof-title">an expat in paris</div>'
    '<div class="bestof-desc">On Baldwin\u2019s Giovanni\u2019s Room, expatriate life, and writing honestly about desire and exile.</div>'
    '<span class="bestof-link">Read &rarr;</span></a>'

    '<a href="/honest-pursuit.html" class="bestof-card" style="color:inherit">'
    '<img src="IMG_20190418_152257_016.jpg" alt="Hampi temple ruins, India \u2014 an honest pursuit, literary manifesto by David Moran" class="bestof-img" loading="lazy">'
    '<span class="bestof-type">Essay &middot; Manifesto</span>'
    '<div class="bestof-title">an honest pursuit</div>'
    '<div class="bestof-desc">A writer\u2019s manifesto. What the work is for and why it matters to keep writing badly before writing well.</div>'
    '<span class="bestof-link">Read &rarr;</span></a>'

    '</div>'
    '<div class="bestof-more">'
    '<span>More original work</span>'
    '<a href="/all-writing.html">Fiction &amp; Poetry &rarr;</a>'
    '<a href="/craft-theory.html">Craft &amp; Theory &rarr;</a>'
    '<a href="https://tumbleweedwords.substack.com" target="_blank" rel="noopener">Newsletter &rarr;</a>'
    '</div>'
    '</div></section>'
)

if old_section in content:
    content = content.replace(old_section, new_section)
    print('Bestof section replaced.')
else:
    print('ERROR: old section not found')

# Also add .bestof-more CSS — append before closing </style> of the bestof CSS block
old_bestof_css_end = '.bestof-link{font-family:var(--fm);font-size:.48rem;letter-spacing:.1em;text-transform:uppercase;color:var(--p)}'
new_bestof_css_end = (
    '.bestof-link{font-family:var(--fm);font-size:.48rem;letter-spacing:.1em;text-transform:uppercase;color:var(--p)}'
    '.bestof-more{display:flex;align-items:center;gap:1.5rem;flex-wrap:wrap;margin-top:1.8rem;padding-top:1.2rem;border-top:1px solid var(--br)}'
    '.bestof-more span{font-family:var(--fm);font-size:.5rem;letter-spacing:.1em;text-transform:uppercase;color:var(--mu)}'
    '.bestof-more a{font-family:var(--fm);font-size:.5rem;letter-spacing:.1em;text-transform:uppercase;color:var(--p)}'
    '.bestof-more a:hover{color:var(--p2)}'
)
if old_bestof_css_end in content:
    content = content.replace(old_bestof_css_end, new_bestof_css_end)
    print('CSS extended.')
else:
    print('ERROR: bestof CSS end not found')

with open('C:/Users/tumbl/projects/tumbleewords/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done.')
