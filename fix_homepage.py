import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/tumbl/projects/tumbleewords/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace cities CSS with bestof CSS
old_css = '.cities-sec{background:var(--bg2);padding:7rem 2rem;border-bottom:1px solid var(--br)}.cities-inner{max-width:1100px;margin:0 auto}.cities-inner h2{font-family:var(--fd);font-size:clamp(1.6rem,3.5vw,2.4rem);font-weight:700;color:var(--ink);line-height:1.1;letter-spacing:-.02em;margin-bottom:2rem}.cities-inner h2 em{color:var(--p);font-style:italic}.cities-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:1.5rem}@media(max-width:800px){.cities-grid{grid-template-columns:1fr 1fr}}@media(max-width:500px){.cities-grid{grid-template-columns:1fr}}.city-card{padding:0 !important;overflow:hidden}.city-card-img{width:100%;height:190px;object-fit:cover;display:block;filter:grayscale(10%)}.city-card-body{padding:1.4rem 1.6rem;display:flex;flex-direction:column;gap:.5rem;flex:1}.city-card{background:var(--bg);border:1px solid var(--br);display:flex;flex-direction:column;text-decoration:none;transition:border-color .2s,box-shadow .2s;overflow:hidden}.city-card:hover{border-color:var(--p);box-shadow:0 4px 20px rgba(85,51,232,.08)}.city-card-lbl{font-family:var(--fm);font-size:.46rem;letter-spacing:.2em;text-transform:uppercase;color:var(--p)}.city-card-name{font-family:var(--fd);font-size:1.5rem;font-weight:700;color:var(--ink);line-height:1;letter-spacing:-.02em}.city-card-desc{font-family:var(--fd);font-size:.88rem;font-style:italic;color:var(--p3);line-height:1.6;flex:1;margin-top:.2rem}.city-card-cta{font-family:var(--fm);font-size:.46rem;letter-spacing:.12em;text-transform:uppercase;color:var(--p);margin-top:.5rem}'

new_css = '.bestof-sec{background:var(--bg2);padding:7rem 2rem;border-bottom:1px solid var(--br)}.bestof-inner{max-width:1100px;margin:0 auto}.bestof-inner h2{font-family:var(--fd);font-size:clamp(1.6rem,3.5vw,2.4rem);font-weight:700;color:var(--ink);line-height:1.1;letter-spacing:-.02em;margin-bottom:.6rem}.bestof-inner h2 em{color:var(--p);font-style:italic}.bestof-inner .sec-sub{font-size:.88rem;color:var(--mu);line-height:1.7;margin-bottom:2rem}.bestof-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-top:0}@media(max-width:800px){.bestof-grid{grid-template-columns:repeat(2,1fr)}}@media(max-width:500px){.bestof-grid{grid-template-columns:1fr}}.bestof-card{border:1px solid var(--br);background:var(--bg);padding:1.2rem;transition:background .15s,border-color .2s;display:flex;flex-direction:column;gap:.4rem;text-decoration:none}.bestof-card:hover{background:var(--bg);border-color:var(--p)}.bestof-img{width:calc(100% + 2.4rem);margin:-1.2rem -1.2rem 1rem;height:160px;object-fit:cover;display:block;filter:grayscale(10%)}.bestof-type{font-family:var(--fm);font-size:.44rem;letter-spacing:.12em;text-transform:uppercase;color:var(--p)}.bestof-title{font-family:var(--fd);font-size:.88rem;font-weight:600;color:var(--ink);line-height:1.3}.bestof-desc{font-size:.76rem;color:var(--mu);line-height:1.6;flex:1}.bestof-link{font-family:var(--fm);font-size:.48rem;letter-spacing:.1em;text-transform:uppercase;color:var(--p)}'

if old_css in content:
    content = content.replace(old_css, new_css)
    print('CSS replaced.')
else:
    print('ERROR: old CSS not found')

# 2. Replace the cities section HTML with bestof section
old_section_start = '<section class="cities-sec">'
old_section_end = '</section><section class="writer-sec">'

start_idx = content.find(old_section_start)
end_idx = content.find(old_section_end)
print(f'Cities section: start={start_idx}, end={end_idx}')

new_section = (
    '<section class="bestof-sec"><div class="bestof-inner">'
    '<div class="sec-label">Best Of &middot; Handpicked Fiction &amp; Poetry</div>'
    '<h2>Original work. <em>Twenty years</em> on the road.</h2>'
    '<p class="sec-sub">The most read and most loved pieces from twenty years of Tumbleweed Words. Published internationally. Start here.</p>'
    '<div class="bestof-grid">'
    '<a href="https://tumbleweedwords.substack.com/p/three-nomadic-poems" class="bestof-card" target="_blank" rel="noopener" style="color:inherit">'
    '<img src="IMG_20150317_132854.jpg" alt="Buenos Aires waterfront skyline \u2014 nomadic poem by David Moran" class="bestof-img" loading="lazy">'
    '<span class="bestof-type">Poetry &middot; Buenos Aires</span>'
    '<div class="bestof-title">nomadic | poem</div>'
    '<div class="bestof-desc">Written on a plane while flying away from love and loss. &ldquo;The final act of a born run away, moving through the world at good speed.&rdquo;</div>'
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

# Replace from start of cities section to end of </section>
old_chunk = content[start_idx : end_idx + len('</section>')]
content = content[:start_idx] + new_section + content[end_idx + len('</section>'):]

with open('C:/Users/tumbl/projects/tumbleewords/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done.')
