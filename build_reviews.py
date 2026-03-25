"""
Build 6 book review pages from tumbleweed-book-reviews.md.docx
"""
import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

BASE = 'C:/Users/tumbl/projects/tumbleewords'

# ── Extract boilerplate from template ─────────────────────────────────────────
with open(f'{BASE}/george-saunders-vigil-review.html', 'r', encoding='utf-8') as f:
    TPL = f.read()

GA        = re.search(r'(<!-- Google tag.*?</script>)', TPL, re.DOTALL).group(1)
FONTS     = re.search(r'(<link rel="preconnect" href="https://fonts\.googleapis.*?rel="stylesheet">)', TPL).group(1)
STYLE1    = re.search(r'(<style>\s*\*,\*::before.*?</style>)', TPL, re.DOTALL).group(1)
STYLE2    = re.search(r'(<style>\s*\.nav\{position:sticky.*?</style>)', TPL, re.DOTALL).group(1)
BC_STYLE  = re.search(r'(<style>\.breadcrumb\{.*?</style>)', TPL).group(1)
NSEARCH   = re.search(r'(<style id="nsearch-css">.*?</style>)', TPL).group(1)
NAV       = re.search(r'(<nav class="nav">.*?</nav>)', TPL).group(1)
SUB_SEC   = re.search(r'(<section style="background:var\(--bg2.*?</section>)', TPL, re.DOTALL).group(1)
FOOTER    = re.search(r'(<footer class="ft">.*?</footer>)', TPL, re.DOTALL).group(1)
POPUP     = re.search(r'(<style>#tw-popup-overlay.*?</script>)', TPL, re.DOTALL).group(1)
SEARCH_JS = re.search(r'(<script>\(function\(\)\{var t=document\.getElementById\(\'searchToggle.*?</script>)', TPL).group(1)
SUBBAR    = re.search(r'(<style id="sub-bar-css">.*?display:none.*?></div>)', TPL, re.DOTALL).group(1)
CONSENT   = re.search(r'(<div id="tw-consent".*?display:none.*?></div>)', TPL).group(1)

def schema(title, desc, url, image, keywords, pub_date='2026-03-24'):
    return json.dumps({
        "@context":"https://schema.org","@type":"Article",
        "headline":title,"description":desc,
        "datePublished":pub_date,"dateModified":"2026-03-24",
        "author":{"@type":"Person","name":"David Moran","url":"https://tumbleweedwords.com/about.html","sameAs":["https://tumbleweedwords.substack.com"]},
        "publisher":{"@type":"Organization","name":"Tumbleweed Words","url":"https://tumbleweedwords.com"},
        "mainEntityOfPage":{"@type":"WebPage","@id":url},
        "keywords":keywords,"image":image,"url":url
    }, ensure_ascii=False)

def build(fname, title, desc, keywords, og_image, tag, h1, standfirst,
          body_html, verdict, related_links, pub_date='2026-03-24'):

    url = f'https://tumbleweedwords.com/{fname}'
    ld  = schema(title, desc, url, og_image, keywords, pub_date)
    rel = ''.join(f'<li><a href="{u}">{l}</a></li>' for l, u in related_links)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
{GA}
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Tumbleweed Words</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<meta name="author" content="David Moran — Tumbleweed Words">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Tumbleweed Words">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:creator" content="@tumbleweedwords">
<script type="application/ld+json">{ld}</script>
{FONTS}
{STYLE1}
{STYLE2}
{BC_STYLE}
{NSEARCH}
</head>
<body>
<div class="wrap">
{NAV}
<main>
  <nav class="breadcrumb" aria-label="breadcrumb"><a href="/">Tumbleweed Words</a><span class="bc-sep">&rsaquo;</span><a href="/reads.html">Must Reads</a></nav>
  <span class="tag">{tag}</span>
  <h1>{h1}</h1>
  <p class="byline">By David Moran &middot; <time datetime="{pub_date}">{pub_date}</time></p>
  <p class="standfirst">{standfirst}</p>
  <div class="body">
{body_html}
  <div class="verdict"><div class="verdict-l">Verdict</div><p>{verdict}</p></div>
  <div class="cta-box">
    <div class="lbl">Tumbleweed Words &middot; Newsletter</div>
    <p>Flash fiction and poetry in the tradition of what you just read. Written on the road. Over 1,200 readers. Free.</p>
    <a href="https://tumbleweedwords.substack.com" target="_blank" rel="noopener">Read and subscribe &rarr;</a>
  </div>
  <div class="related"><span class="lbl">Keep reading</span><ul>{rel}</ul></div>
  </div>
</main>
{SUB_SEC}
{FOOTER}
</div>
{POPUP}
{SEARCH_JS}
{SUBBAR}
{CONSENT}
<script>(function(){{var b=document.querySelector('.body');var bl=document.querySelector('.byline');if(!b||!bl)return;var words=b.innerText.trim().split(/\s+/).length;var mins=Math.max(1,Math.round(words/200));var sp=document.createElement('span');sp.textContent=' \u00b7 '+mins+' min read';bl.appendChild(sp);}})();</script>
</body>
</html>"""

    with open(f'{BASE}/{fname}', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  Written: {fname}')


# ══════════════════════════════════════════════════════════════════════════════
# 1. The Emperor of Gladness — Ocean Vuong
# ══════════════════════════════════════════════════════════════════════════════
build(
    'ocean-vuong-emperor-of-gladness-review.html',
    'Ocean Vuong\u2019s The Emperor of Gladness \u2014 Review',
    'A review of Ocean Vuong\u2019s second novel \u2014 the most tender exploration of American working-class life published in a decade, and a significant shift from On Earth We\u2019re Briefly Gorgeous.',
    'Ocean Vuong Emperor of Gladness review, Ocean Vuong second novel, Emperor of Gladness 2025',
    'https://tumbleweedwords.com/paris-bookshop.jpg',
    'Book Review',
    'Ocean Vuong\u2019s <em>The Emperor of Gladness</em>',
    'Vuong\u2019s second novel opens on a bridge. A boy about to jump is stopped by an elderly woman with dementia asking him to carry her groceries. What follows is the most tender exploration of American working-class life published in a decade.',
    """<p>Ocean Vuong\u2019s second novel opens on a bridge in Connecticut. A nineteen-year-old boy named Hai is about to jump. An elderly Lithuanian woman with dementia stops him \u2014 not with wisdom or a speech, but by asking him to carry her groceries. What follows is a year of caregiving, fast-food shifts, and quiet reckoning that somehow becomes the most tender exploration of American working-class life published in a decade.</p>

<h2>Not the expected book</h2>
<p>This is not the book people expected after <em>On Earth We\u2019re Briefly Gorgeous</em>. It is bigger, messier, funnier. Vuong has always been a poet first, and the sentences here still land with that compressed, held-breath precision and mystifying fluidity of his earlier work. But <em>The Emperor of Gladness</em> earns something new: patience. The novel breathes. It lets its characters sit with each other in silence. It finds beauty in a man scrubbing a fryer at midnight, in a woman forgetting her own name but remembering how to laugh.</p>

<h2>The relationship at its centre</h2>
<p>Hai\u2019s relationship with Grazina \u2014 based on a real woman Vuong cared for \u2014 is drawn without a single drop of sentimentality. Their bond is built on proximity and repetition. He bathes her. She tells him stories that may not have happened. They eat together. The novel understands that love is often just showing up, day after day, for someone who cannot repay you.</p>

<h2>What Vuong set out to write</h2>
<p>Vuong has said he wanted to write a book about people for whom the American Dream means keeping the same job for thirty years and driving the same car. He has done that. He has also written a book about grief, about the immigrant body at work, and about the strange holiness of ordinary life. It was named a Best Book of 2025 by nearly every major publication, and it deserves every word of that praise.</p>""",
    'Essential. Vuong has expanded what he can do without losing what makes him singular. This is his finest prose work.',
    [
        ('Best Books If You Like Carver', '/best-books-if-you-like-carver.html'),
        ('What Is Flash Fiction?', '/what-is-flash-fiction.html'),
        ('George Saunders\u2019 Vigil \u2014 Review', '/george-saunders-vigil-review.html'),
        ('Must Reads', '/reads.html'),
    ],
    '2026-03-24'
)

# ══════════════════════════════════════════════════════════════════════════════
# 2. The Bronze Arms — Richie Hofmann
# ══════════════════════════════════════════════════════════════════════════════
build(
    'richie-hofmann-bronze-arms-review.html',
    'Richie Hofmann\u2019s The Bronze Arms \u2014 Review',
    'A review of Richie Hofmann\u2019s third poetry collection \u2014 precise, erotic, elegiac. The image that opens it, of armless statues and a father\u2019s rescuing grip, drives every poem in the book.',
    'Richie Hofmann Bronze Arms review, The Bronze Arms poetry, Richie Hofmann poetry 2026',
    'https://tumbleweedwords.com/paris-bookshop.jpg',
    'Poetry Review',
    'Richie Hofmann\u2019s <em>The Bronze Arms</em>',
    'Hofmann\u2019s third collection begins with a near-drowning. As a boy on Crete, he was pulled from the water by his father\u2019s arms. He had noticed, before going under, that the statues around him had no arms at all. That image drives every poem in this extraordinary book.',
    """<p>Richie Hofmann\u2019s third collection begins with a near-drowning. As a boy on Crete, Hofmann was pulled from the water by his father\u2019s arms. He had noticed, before going under, that the statues around him had no arms at all. That image \u2014 the armless body, the rescuing grip, the space between survival and beauty \u2014 drives every poem in this extraordinary book.</p>

<h2>Between classical myth and contemporary desire</h2>
<p><em>The Bronze Arms</em> moves between classical myth and contemporary desire with a control that feels almost dangerous. Hofmann writes about the male body with the precision of a sculptor and the hunger of someone who has studied every surface. These poems are explicit without being confessional. They hold the erotic and the elegiac in the same line, the same breath.</p>
<p>There is a quality here that recalls Cavafy \u2014 the quiet devastation of desire remembered from a distance \u2014 but Hofmann is doing something entirely his own. The formal range is striking. Fragments sit beside longer lyric poems. Some pieces are listed by first line rather than title, a nod to Sappho\u2019s recovered shards. Others, like the harrowing centrepiece set in Crete, build narrative tension across pages. Throughout, the language stays precise, hushed, and lethal.</p>

<h2>Beneath the marble surface</h2>
<p>Publishers Weekly was right to call these poems pristine. But beneath the white marble surface, there is real blood. What makes this collection essential is its refusal to separate beauty from pain. Hofmann writes about desire as a force that rescues and destroys in equal measure. The arms that saved him are the arms that hold him down. Every poem in this book knows it.</p>
<p>If you care about what contemporary poetry can still do \u2014 how it can compress an entire mythology of longing into a single image \u2014 read this.</p>""",
    'One of the most formally accomplished poetry collections of the year. Precise, erotic, and quietly devastating.',
    [
        ('Prose Poetry vs Flash Fiction', '/prose-poetry-vs-flash-fiction.html'),
        ('Influenced by Amy Hempel', '/influenced-by-amy-hempel.html'),
        ('Must Reads', '/reads.html'),
        ('George Saunders\u2019 Vigil \u2014 Review', '/george-saunders-vigil-review.html'),
    ],
    '2026-03-24'
)

# ══════════════════════════════════════════════════════════════════════════════
# 3. Under Water — Tara Menon
# ══════════════════════════════════════════════════════════════════════════════
build(
    'tara-menon-under-water-review.html',
    'Tara Menon\u2019s Under Water \u2014 Review',
    'A review of Tara Menon\u2019s debut novel \u2014 a luminous, structurally precise book about two disasters and their long aftermaths, told with a restraint that trusts the reader completely.',
    'Tara Menon Under Water review, Under Water novel 2026, Tara Menon debut novel',
    'https://tumbleweedwords.com/paris-bookshop.jpg',
    'Book Review',
    'Tara Menon\u2019s <em>Under Water</em>',
    'Menon\u2019s debut moves between two disasters \u2014 the 2004 Boxing Day tsunami and Hurricane Sandy \u2014 and the decades of ordinary life that follow. A novel about aftermath, written with a restraint that trusts the reader completely.',
    """<p>Tara Menon\u2019s debut moves between two disasters: the 2004 Boxing Day tsunami in Thailand and Hurricane Sandy\u2019s landfall in 2012. Between them, two women \u2014 a marine biologist and her estranged daughter \u2014 circle each other across years and oceans, trying to find language for what the water took.</p>

<h2>A novel about aftermath</h2>
<p>This is a novel about aftermath. Not the dramatic moment of the wave, but the decades that follow it. Menon writes about survivor\u2019s guilt with a clinical specificity that feels earned rather than performed. Her descriptions of tropical marine life are vivid and strange \u2014 coral bleaching as metaphor, tidal patterns as emotional architecture \u2014 and the science never overwhelms the human story. It sits underneath it, the way the ocean sits underneath everything.</p>

<h2>Restraint as a formal choice</h2>
<p>The prose is careful and luminous. Menon, a Harvard professor making her fiction debut, writes with a restraint that trusts the reader to feel what the characters cannot say. Katie Kitamura called it a novel of remarkable delicacy and power, and that captures it exactly. There is power here, but it never raises its voice.</p>

<h2>The structure</h2>
<p>What makes <em>Under Water</em> exceptional is its structure. The two timelines do not mirror each other \u2014 they pull apart, creating a space in the middle that the reader must cross alone. That gap is where the grief lives. Menon understands that the worst thing about catastrophe is not the event itself but the long, ordinary years that follow, in which you must decide whether to rebuild or keep treading water.</p>
<p>This is a debut that arrives fully formed. The writing is assured, the emotional landscape is vast, and the ending \u2014 quiet, devastating, unresolved in exactly the right way \u2014 will stay with you for weeks. One of the most impressive first novels of the year.</p>""",
    'A debut that arrives fully formed. Luminous, structurally precise, and emotionally vast.',
    [
        ('What Is Flash Fiction?', '/what-is-flash-fiction.html'),
        ('Best Flash Fiction Collections', '/best-flash-fiction-collections.html'),
        ('Must Reads', '/reads.html'),
        ('George Saunders\u2019 Vigil \u2014 Review', '/george-saunders-vigil-review.html'),
    ],
    '2026-03-24'
)

# ══════════════════════════════════════════════════════════════════════════════
# 4. Night Watch — Kevin Young
# ══════════════════════════════════════════════════════════════════════════════
build(
    'kevin-young-night-watch-review.html',
    'Kevin Young\u2019s Night Watch \u2014 Review',
    'A review of Kevin Young\u2019s Night Watch \u2014 a big, restless, deeply musical collection moving through personal grief and American history, with the Millie-Christine sequence as its centrepiece.',
    'Kevin Young Night Watch review, Night Watch poetry 2025, Kevin Young poetry collection',
    'https://tumbleweedwords.com/paris-bookshop.jpg',
    'Poetry Review',
    'Kevin Young\u2019s <em>Night Watch</em>',
    'A big, restless, deeply musical collection that moves through personal grief and American history with the confidence of a writer working at the peak of his powers. The Millie-Christine sequence alone makes this essential.',
    """<p>Kevin Young\u2019s <em>Night Watch</em> is a big, restless, deeply musical collection that moves through personal grief and American history with the confidence of a writer working at the peak of his powers. Divided into four sections, the book covers extraordinary ground \u2014 from meditations on the moon and birds to a sequence about Young\u2019s Louisiana roots, to the remarkable story of Millie-Christine, enslaved conjoined twin singers who performed across nineteenth-century America, to a Dante-inspired descent into the underworld.</p>

<h2>What holds it together</h2>
<p>The range alone is impressive. But what holds <em>Night Watch</em> together is Young\u2019s ear. These are poems built on rhythm and repetition; on the way a phrase can gather weight through variation. The lines feel scored rather than written. You can hear blues and jazz underneath the syntax, and the grief \u2014 for his father, for a version of America, for the passage of time \u2014 comes through the music rather than despite it.</p>

<h2>The Millie-Christine sequence</h2>
<p>The Millie-Christine sequence is the collection\u2019s centrepiece and its most ambitious achievement. Young tells their story without spectacle, letting the twin voices speak in overlapping registers. It becomes a meditation on what it means to share a body, a life, a history with someone \u2014 and what happens when that bond is severed. In a collection concerned with American memory, this section asks who gets remembered, who gets forgotten, and whose voice survives.</p>

<h2>A culmination</h2>
<p>Young has been writing with distinction for over two decades, but <em>Night Watch</em> feels like a culmination. It is elegiac without being heavy, political without being didactic, and formally inventive without losing emotional directness. If you have not read him, start here. If you have, this may be his finest work \u2014 a collection that trusts the reader to sit in the dark and listen.</p>""",
    'Possibly Young\u2019s finest collection. Musically assured, historically serious, and emotionally direct.',
    [
        ('Prose Poetry vs Flash Fiction', '/prose-poetry-vs-flash-fiction.html'),
        ('What Is Dirty Realism?', '/what-is-dirty-realism.html'),
        ('Must Reads', '/reads.html'),
        ('George Saunders\u2019 Vigil \u2014 Review', '/george-saunders-vigil-review.html'),
    ],
    '2026-03-24'
)

# ══════════════════════════════════════════════════════════════════════════════
# 5. Poor — Caleb Azumah Nelson
# ══════════════════════════════════════════════════════════════════════════════
build(
    'caleb-azumah-nelson-poor-review.html',
    'Caleb Azumah Nelson\u2019s Poor \u2014 Review',
    'A review of Caleb Azumah Nelson\u2019s Forward Prize-winning poetry debut \u2014 poems and photographs charting young Black lives in South London, intimate and political in the same afternoon.',
    'Caleb Azumah Nelson Poor review, Poor poetry 2026, Caleb Azumah Nelson Forward Prize',
    'https://tumbleweedwords.com/paris-bookshop.jpg',
    'Poetry Review',
    'Caleb Azumah Nelson\u2019s <em>Poor</em>',
    'Nelson made his name with two novels written in rhythmic, second-person prose closer to poetry than fiction. Now he has crossed over entirely. Poor won the Forward Prize before most people had read it, and it deserves to.',
    """<p>Caleb Azumah Nelson made his name with the novels <em>Open Water</em> and <em>Small Worlds</em>, both written in a rhythmic, second-person prose that felt closer to poetry than fiction. Now he has crossed over entirely. <em>Poor</em> is a collection of poems and photographs that charts the lives of young Black men growing up in South London, and it won the Forward Prize before most people had even read it.</p>

<h2>Grounded in place</h2>
<p>The collection is grounded in place. Nelson writes about estates, playgrounds, barbershops, and bus routes with the specificity of someone who learned to see there. The photographs \u2014 stark, tender, shot with an eye for gesture and light \u2014 sit alongside the poems without illustrating them. They are parallel texts. Together they build a portrait of a world that is both intimate and political, where friendship and policing coexist in the same afternoon.</p>

<h2>Restraint and accumulation</h2>
<p>What strikes you first is the restraint. Nelson does not explain or argue. He places a scene in front of you \u2014 boys walking, a mother calling from a window, a football caught in the last light \u2014 and lets the weight accumulate. The poems are short, sometimes just a few lines, but they carry an emotional density that much longer work fails to achieve. There is a Vuong-like quality here: the belief that a single image, held still long enough, can contain an entire life.</p>

<h2>More than a novelist</h2>
<p>The Guardian named it a Book of the Year and called it a landmark debut for British poetry. That feels right. <em>Poor</em> does something rare \u2014 it makes the ordinary sacred without making it sentimental. Nelson writes about his community with love and precision, and the result is a collection that feels both urgent and timeless. This is the book that announces him as more than a novelist. He is simply a writer, and this is his best work.</p>""",
    'A landmark debut for British poetry. Intimate, political, and made sacred by precision rather than sentiment.',
    [
        ('Prose Poetry vs Flash Fiction', '/prose-poetry-vs-flash-fiction.html'),
        ('What Is Flash Fiction?', '/what-is-flash-fiction.html'),
        ('Must Reads', '/reads.html'),
        ('Richie Hofmann\u2019s The Bronze Arms \u2014 Review', '/richie-hofmann-bronze-arms-review.html'),
    ],
    '2026-03-24'
)

# ══════════════════════════════════════════════════════════════════════════════
# 6. Ruth — Kate Riley
# ══════════════════════════════════════════════════════════════════════════════
build(
    'kate-riley-ruth-review.html',
    'Kate Riley\u2019s Ruth \u2014 Review',
    'A review of Kate Riley\u2019s seventh novel \u2014 a book in which almost nothing happens and everything matters. Two old friends, ageing, failing. Prose stripped to essential weight.',
    'Kate Riley Ruth review, Ruth novel 2025, Kate Riley seventh novel',
    'https://tumbleweedwords.com/paris-bookshop.jpg',
    'Book Review',
    'Kate Riley\u2019s <em>Ruth</em>',
    'A novel in which almost nothing happens and everything matters. Two old friends move through their lives in London \u2014 writing, failing, ageing, trying to stay afloat. The prose is so precise, so clean of excess, that each sentence reads like a decision made after all other options were weighed and quietly discarded.',
    """<p>Kate Riley\u2019s <em>Ruth</em> is a novel in which almost nothing happens and everything matters. Two old friends, Laura and Edward, move through their lives in London \u2014 writing, failing, ageing, trying to stay afloat. The prose is so precise, so clean of excess, that each sentence reads like a decision made after all other options were weighed and quietly discarded.</p>

<h2>Accumulation as method</h2>
<p>This is Riley\u2019s seventh novel, but it arrives with the energy of a discovery. The book was the subject of a six-way auction, and its publisher described it as her finest work. That claim is not hyperbole. <em>Ruth</em> achieves something extraordinarily difficult: it makes the interior life of two moderately successful, moderately unhappy people feel urgent and essential.</p>
<p>Riley\u2019s method is accumulation. Small details \u2014 a meal prepared badly, a walk through a park that used to mean something, a phone call not returned \u2014 build into an emotional architecture that the reader inhabits rather than observes.</p>

<h2>The loneliness of being known</h2>
<p>The novel is about friendship, but it is also about the loneliness of being known by someone who no longer quite sees you. Laura and Edward care for each other, deeply, but they cannot save each other, and the novel never pretends otherwise.</p>

<h2>The prose itself</h2>
<p>The writing is crystalline. Riley has always been praised for her prose, but here the sentences have a new quality \u2014 a kind of earned simplicity, as though the language has been stripped back to its essential weight. There are digressions on life and art that feel neither digressive nor academic. They feel like thinking. The novel trusts you to think alongside it.</p>
<p>If you are the kind of reader who believes fiction should move at the speed of attention \u2014 that the quiet devastation of two people failing to say the right thing is worth five hundred pages of plot \u2014 then <em>Ruth</em> is the novel you have been waiting for. It is a small, perfect, devastating thing.</p>""",
    'Riley\u2019s finest work. Crystalline prose, earned simplicity, and the quiet devastation of two people who know each other too well.',
    [
        ('Best Books If You Like Carver', '/best-books-if-you-like-carver.html'),
        ('What Is Minimalist Fiction?', '/post-minimalist-fiction.html'),
        ('Must Reads', '/reads.html'),
        ('Ocean Vuong\u2019s The Emperor of Gladness \u2014 Review', '/ocean-vuong-emperor-of-gladness-review.html'),
    ],
    '2026-03-24'
)

# ── Sitemap ────────────────────────────────────────────────────────────────────
new_pages = [
    'ocean-vuong-emperor-of-gladness-review.html',
    'richie-hofmann-bronze-arms-review.html',
    'tara-menon-under-water-review.html',
    'kevin-young-night-watch-review.html',
    'caleb-azumah-nelson-poor-review.html',
    'kate-riley-ruth-review.html',
]
with open(f'{BASE}/sitemap.xml', 'r', encoding='utf-8') as f:
    sm = f.read()
for p in new_pages:
    url = f'https://tumbleweedwords.com/{p}'
    if url not in sm:
        entry = f'  <url>\n    <loc>{url}</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n'
        sm = sm.replace('</urlset>', entry + '</urlset>')
        print(f'  Sitemap: added {p}')
with open(f'{BASE}/sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sm)

print('\nDone.')
