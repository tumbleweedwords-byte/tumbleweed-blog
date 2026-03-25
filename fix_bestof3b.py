import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/tumbl/projects/tumbleewords/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = '<section class="bestof-sec">'
end_marker   = '</section><section class="writer-sec">'

start = content.find(start_marker)
end   = content.find(end_marker)
print(f'start={start}, end={end}')

new_section = (
    '<section class="bestof-sec"><div class="bestof-inner">'
    '<div class="sec-label">Best Of &middot; Handpicked Fiction &amp; Poetry</div>'
    '<h2>Original work. <em>Twenty years</em> on the road.</h2>'
    '<p class="sec-sub">The most read and most loved pieces from twenty years of Tumbleweed Words. Published internationally. Start here.</p>'
    '<div class="bestof-grid">'

    '<a href="/street-legal.html" class="bestof-card" style="color:inherit">'
    '<img src="IMG_0175.JPG" alt="Night street lights through rain &mdash; train in vain, flash fiction by David Moran" class="bestof-img" loading="lazy">'
    '<span class="bestof-type">Fiction &middot; Berlin</span>'
    '<div class="bestof-title">train in vain | short fiction</div>'
    '<div class="bestof-desc">Written on a Berlin U-Bahn watching a stranger exit my life. Pushcart Prize nominated.</div>'
    '<span class="bestof-link">Read &rarr;</span></a>'

    '<a href="/an-expat-in-paris.html" class="bestof-card" style="color:inherit">'
    '<img src="P1040311.JPG" alt="Looking up through a European courtyard &mdash; an expat in paris, essay by David Moran" class="bestof-img" loading="lazy">'
    '<span class="bestof-type">Essay &middot; James Baldwin</span>'
    '<div class="bestof-title">an expat in paris</div>'
    '<div class="bestof-desc">On Baldwin&rsquo;s Giovanni&rsquo;s Room, expatriate life, and writing honestly about desire and exile.</div>'
    '<span class="bestof-link">Read &rarr;</span></a>'

    '<a href="/honest-pursuit.html" class="bestof-card" style="color:inherit">'
    '<img src="IMG_20190418_152257_016.jpg" alt="Hampi temple ruins, India &mdash; an honest pursuit, literary manifesto by David Moran" class="bestof-img" loading="lazy">'
    '<span class="bestof-type">Essay &middot; Manifesto</span>'
    '<div class="bestof-title">an honest pursuit</div>'
    '<div class="bestof-desc">A writer&rsquo;s manifesto. What the work is for and why it matters to keep writing badly before writing well.</div>'
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

old_chunk = content[start : end + len('</section>')]
content = content[:start] + new_section + content[end + len('</section>'):]

with open('C:/Users/tumbl/projects/tumbleewords/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done.')
