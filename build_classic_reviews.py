import os, re

BASE = 'C:/Users/tumbl/projects/tumbleewords'

BOILERPLATE = open(os.path.join(BASE, 'ocean-vuong-emperor-of-gladness-review.html'), encoding='utf-8').read()

NAV = re.search(r'(<nav class="nav">.*?</nav>)', BOILERPLATE, re.DOTALL).group(1)
POPUP = re.search(r'(<style>#tw-popup.*?</script>\n)', BOILERPLATE, re.DOTALL).group(1)
SEARCH_JS = re.search(r'(<script>\(function\(\)\{var t=document\.getElementById\(\'searchToggle\'\).*?</script>)', BOILERPLATE, re.DOTALL).group(1)
SUB_BAR = re.search(r'(<style id="sub-bar-css">.*?</script>)', BOILERPLATE, re.DOTALL).group(1)
CONSENT = re.search(r'(<div id="tw-consent".*?</div>)', BOILERPLATE, re.DOTALL).group(1)
READING_TIME = re.search(r'(<script>\(function\(\)\{var b=document\.querySelector.*?</script>)', BOILERPLATE, re.DOTALL).group(1)

STYLES_1 = re.search(r'(<style>\n\*,\*::before.*?</style>)', BOILERPLATE, re.DOTALL).group(1)
STYLES_2 = re.search(r'(<style>\n\.nav\{position:sticky.*?</style>)', BOILERPLATE, re.DOTALL).group(1)

BOOK_COVER_CSS = (
    '.book-cover{float:right;margin:0 0 1.4rem 2rem;max-width:170px;width:100%;'
    'box-shadow:0 4px 20px rgba(26,24,32,.18);border-radius:3px;display:block}'
    '@media(max-width:600px){.book-cover{float:none;margin:0 auto 1.6rem;max-width:140px}}'
    '.review-badge{display:inline-block;font-family:ui-monospace,"SF Mono",monospace;'
    'font-size:.44rem;letter-spacing:.14em;text-transform:uppercase;color:#6B6880;'
    'border:1px solid #D4D0C4;padding:.18rem .55rem;border-radius:2px;margin-left:.6rem;'
    'vertical-align:middle}'
)

REVIEWS = [
    {
        'slug': 'hemingway-old-man-sea-review',
        'title': "Hemingway's <em>The Old Man and the Sea</em>",
        'title_plain': "Hemingway's The Old Man and the Sea",
        'badge': 'Classic &middot; Novel',
        'badge_plain': 'Classic · Novel',
        'img': 'old-man-and-the-sea.jpg',
        'img_alt': 'The Old Man and the Sea by Ernest Hemingway — book cover',
        'author': 'Ernest Hemingway',
        'year': '1952',
        'publisher': 'Scribner',
        'description': "The novel that won Hemingway the Nobel Prize. Santiago, an ageing Cuban fisherman, rows out alone and hooks the greatest marlin of his life. What follows is a study in dignity, endurance, and the grace of trying.",
        'standfirst': "The novel that won Hemingway the Nobel Prize. Santiago, an ageing Cuban fisherman, rows out alone and hooks the greatest marlin of his life. What follows is a study in dignity, endurance, and the grace of trying.",
        'keywords': 'Old Man and the Sea review, Hemingway review, Hemingway classic novel',
        'verdict': 'A perfect novel. 127 pages that contain everything Hemingway believed about how to live and how to lose.',
        'body': """<p>Hemingway wrote <em>The Old Man and the Sea</em> in eight weeks in Cuba in 1951. He knew immediately it was the best thing he had ever written. It is 127 pages. It contains everything.</p>

<h2>The setup</h2>
<p>Santiago is an old Cuban fisherman who has gone 84 days without a catch. The village boys have been pulled away by their parents. He rows out alone before dawn, further than anyone else, and hooks a great marlin he cannot see. What follows is three days at sea — the line taut between the old man and the fish, the fish pulling the skiff, Santiago holding on.</p>

<h2>The iceberg in action</h2>
<p>This is Hemingway's iceberg theory made flesh. Nothing is explained. The dignity is in what is not said: the pain in Santiago's hands, the boy he thinks of, the lions he dreams of on the beaches of Africa. Hemingway strips language down to action and sensation and somehow puts the whole of a human life inside it.</p>

<h2>What the book is actually about</h2>
<p>It is about failure and what a man does with it. Santiago catches the marlin and then loses it — stripped to the bone by sharks on the way home. He returns with nothing but the skeleton. But he has not been beaten. The book insists on the difference. There is a kind of winning that has nothing to do with what you bring back, and Hemingway knew it was the only kind worth writing about.</p>

<blockquote><p>&ldquo;A man can be destroyed but not defeated.&rdquo;</p></blockquote>

<p>The Nobel Committee said this book showed the power of his style &ldquo;as it is at its best&rdquo;. For once, the Committee was right.</p>""",
        'related': [
            ('/influenced-by-ernest-hemingway.html', 'How Hemingway Influenced the Short Story'),
            ('/hemingway-vs-carver-difference.html', 'Hemingway vs Carver: What Actually Separates Them'),
            ('/what-is-flash-fiction.html', 'What Is Flash Fiction?'),
            ('/reads.html', 'More Book Reviews'),
        ],
    },
    {
        'slug': 'doris-lessing-fifth-child-review',
        'title': "Doris Lessing's <em>The Fifth Child</em>",
        'title_plain': "Doris Lessing's The Fifth Child",
        'badge': 'Classic &middot; Novel',
        'badge_plain': 'Classic · Novel',
        'img': 'doris lessing.jpg',
        'img_alt': 'The Fifth Child by Doris Lessing — book cover',
        'author': 'Doris Lessing',
        'year': '1988',
        'publisher': 'Jonathan Cape',
        'description': "The Lovatt family have built a perfect life: big house, many children, warmth and order. Then Ben arrives. Lessing's horror story never announces itself as one — it just gets colder and colder.",
        'standfirst': "The Lovatt family have built a perfect life: big house, many children, warmth and order. Then Ben arrives. Lessing's horror story never announces itself as one — it just gets colder and colder.",
        'keywords': 'Doris Lessing Fifth Child review, Fifth Child novel, Doris Lessing classic',
        'verdict': 'Quietly devastating. One of the great British novels of the twentieth century, dressed up as something smaller than it is.',
        'body': """<p>Harriet and David Lovatt want to live differently from everyone around them. More children, more family, more love. They buy a large Victorian house in the English countryside and fill it with warmth, relatives, and purpose. For several years, it works. Then Harriet falls pregnant for the fifth time.</p>

<h2>The arrival of Ben</h2>
<p>Even in the womb, Ben is wrong. He kicks with something beyond ordinary strength. When he arrives, he is pale, heavy, expressionless — not quite like other children. He does not play. He watches. The other children are afraid of him. The family contracts around him, then disperses. The warmth that Harriet and David had built is dismantled, slowly, without drama, by one child who simply does not fit.</p>

<h2>What Lessing does that no one else could</h2>
<p>This is a horror story written entirely in the language of domestic realism. Nothing supernatural happens. Lessing never explains Ben — never says what he is, why he is, what should be done about him. She simply records what a family does when love runs out, and it is more frightening than any ghost story because it is entirely plausible. The real horror is not Ben. It is what the family does to survive him.</p>

<blockquote><p>&ldquo;She was trying to be fair, trying to maintain some balance. But what was fair when nothing was fair?&rdquo;</p></blockquote>

<p>Lessing won the Nobel Prize in 2007. <em>The Fifth Child</em> is 133 pages. It is one of the most precisely disturbing things in British fiction.</p>""",
        'related': [
            ('/best-books-if-you-like-carver.html', 'Best Books If You Like Carver'),
            ('/what-is-flash-fiction.html', 'What Is Flash Fiction?'),
            ('/reads.html', 'More Book Reviews'),
        ],
    },
    {
        'slug': 'bukowski-love-dog-hell-review',
        'title': "Bukowski's <em>Love is a Dog from Hell</em>",
        'title_plain': "Bukowski's Love is a Dog from Hell",
        'badge': 'Classic &middot; Poetry',
        'badge_plain': 'Classic · Poetry',
        'img': 'love-is-a-dog-from-hell.jpg',
        'img_alt': 'Love is a Dog from Hell by Charles Bukowski — book cover',
        'author': 'Charles Bukowski',
        'year': '1977',
        'publisher': 'Black Sparrow Press',
        'description': "150 poems about women, drink, the racetrack, and the life of the margins. Bukowski at his most confessional, most funny, most honest about failure and desire.",
        'standfirst': "150 poems about women, drink, the racetrack, and the life of the margins. Bukowski at his most confessional, most funny, most honest about failure and desire.",
        'keywords': 'Bukowski Love is a Dog from Hell review, Bukowski poetry, Charles Bukowski classic',
        'verdict': 'Essential Bukowski. Raw and funny and honest about failure in ways that feel less like poetry and more like someone telling the truth at closing time.',
        'body': """<p>Bukowski wrote these poems between 1974 and 1977, living in Los Angeles, going to the track, drinking, writing. There are 150 of them. They are about the same things all of Bukowski is about: women who leave, men who drink, rooms that are too small, and the strange grace of keeping going anyway.</p>

<h2>The confessional mode</h2>
<p>Bukowski's great subject is failure without self-pity. He lost jobs, relationships, years. He turned all of it into poems that read like overheard conversation — casual, direct, sometimes funny, occasionally shattering. The language is low, the sentiment is not. These poems are sentimental in the original sense: they feel things fully, without apology.</p>

<h2>Why it matters to serious readers</h2>
<p>Literary readers sometimes dismiss Bukowski as too rough, too popular, too barroom. The dismissal is wrong. What he does with line breaks, with the casual revelation, with the specific image that unlocks the whole poem — these are technical achievements. The apparent artlessness is the art. It takes years to write this badly on purpose.</p>

<blockquote><p>&ldquo;Some lose all mind and become soul, insane.<br>Some lose all soul and become mind, intellectual.<br>Some lose both and become accepted.&rdquo;</p></blockquote>

<p>Read one poem. Then read fifty more. The accumulation is where Bukowski lives.</p>""",
        'related': [
            ('/what-is-flash-fiction.html', 'What Is Flash Fiction?'),
            ('/best-flash-fiction-collections.html', 'Best Flash Fiction Collections'),
            ('/reads.html', 'More Book Reviews'),
        ],
    },
    {
        'slug': 'james-baldwin-another-country-review',
        'title': "James Baldwin's <em>Another Country</em>",
        'title_plain': "James Baldwin's Another Country",
        'badge': 'Classic &middot; Novel',
        'badge_plain': 'Classic · Novel',
        'img': 'james baldwin.jpeg',
        'img_alt': 'Another Country by James Baldwin — book cover',
        'author': 'James Baldwin',
        'year': '1962',
        'publisher': 'Dial Press',
        'description': "New York in the late 1950s. Race, love, sexuality, violence, and the connections between them. Baldwin's third novel is one of the great American books.",
        'standfirst': "New York in the late 1950s. Race, love, sexuality, violence, and the connections between them. Baldwin's third novel is one of the great American books.",
        'keywords': 'James Baldwin Another Country review, Another Country novel, Baldwin classic fiction',
        'verdict': 'Devastating and necessary. One of the great American novels — Baldwin writing at the pitch of full power about everything that mattered.',
        'body': """<p>The first thing that happens in <em>Another Country</em> is Rufus Scott. He is a Black jazz drummer from Harlem, beautiful and talented, and by page forty he is dead — jumped from the George Washington Bridge. The rest of the novel is what his death does to the people who loved him.</p>

<h2>The world Baldwin made</h2>
<p>Baldwin's New York is a city of impossible crossings: across race, across sexuality, across class. His characters — white and Black, straight and gay, artists and drifters — attempt to know each other fully and cannot, not because they are bad people but because the city, the country, the century will not allow it. The violence in the book is not dramatic. It is the quiet violence of a society that cannot bear honesty about desire.</p>

<h2>The language</h2>
<p>Baldwin's prose is the most musical in American fiction after Faulkner — and easier to live inside. His sentences move with the logic of feeling rather than argument. When he describes a jazz performance or the moment before a relationship breaks, the language lifts. It does not describe music; it becomes it.</p>

<blockquote><p>&ldquo;People can't, unhappily, invent their mooring posts, their lovers and their friends, anymore than they can invent their parents. Life gives these and also takes them away.&rdquo;</p></blockquote>

<p>Baldwin wrote this novel while living in Istanbul. It was controversial on publication in 1962. It has not aged a day.</p>""",
        'related': [
            ('/an-expat-in-paris.html', "An Expat in Paris — on Baldwin's Giovanni's Room"),
            ('/best-books-if-you-like-carver.html', 'Best Books If You Like Carver'),
            ('/reads.html', 'More Book Reviews'),
        ],
    },
    {
        'slug': 'baudelaire-flowers-evil-review',
        'title': "Baudelaire's <em>The Flowers of Evil</em>",
        'title_plain': "Baudelaire's The Flowers of Evil",
        'badge': 'Classic &middot; Poetry',
        'badge_plain': 'Classic · Poetry',
        'img': 'flowers of evil.jpg',
        'img_alt': 'The Flowers of Evil by Charles Baudelaire — book cover',
        'author': 'Charles Baudelaire',
        'year': '1857',
        'publisher': 'Poulet-Malassis',
        'description': "The collection that defined what poetry could be after Romanticism. Spleen, beauty, sin, the city, the flesh. Baudelaire invented modern poetry and was put on trial for it.",
        'standfirst': "The collection that defined what poetry could be after Romanticism. Spleen, beauty, sin, the city, the flesh. Baudelaire invented modern poetry and was put on trial for it.",
        'keywords': 'Baudelaire Flowers of Evil review, Les Fleurs du Mal, Baudelaire poetry classic',
        'verdict': 'The collection that launched modern poetry. Still shocking, still beautiful, still the standard everything written since is measured against.',
        'body': """<p>When <em>The Flowers of Evil</em> was published in Paris in 1857, a court convicted Baudelaire of offending public morality and ordered six poems removed. It is the best review a poetry collection has ever received.</p>

<h2>What Baudelaire did</h2>
<p>He took the subject matter of Romanticism — beauty, love, death, transcendence — and refused to redeem any of it. The beauty in these poems is rotting. The love is tied to boredom and disgust. The city is ugly and magnetic simultaneously. Baudelaire was the first major poet to look at the modern city and see it honestly: the crowds, the prostitutes, the gaslight, the ennui, the extraordinary flashes of grace inside all of it.</p>

<h2>The spleen</h2>
<p>The key word in the collection is <em>spleen</em> — Baudelaire's term for a specific modern melancholy, the feeling of being alive in a world that no longer provides adequate meaning. It is not depression. It is consciousness. The poems that explore it are the most modern things in nineteenth-century literature.</p>

<blockquote><p>&ldquo;I have felt the wind of the wing of madness.&rdquo;</p></blockquote>

<p>Rimbaud, Verlaine, Eliot, Ginsberg, Plath — they all begin here. There is no modern poetry without this book.</p>""",
        'related': [
            ('/is-poetry-dying-2026.html', 'Is Poetry Dying? What the Evidence Says'),
            ('/best-flash-fiction-collections.html', 'Best Flash Fiction Collections'),
            ('/reads.html', 'More Book Reviews'),
        ],
    },
    {
        'slug': 'camus-outsider-review',
        'title': "Camus&rsquo; <em>The Outsider</em>",
        'title_plain': "Camus' The Outsider",
        'badge': 'Classic &middot; Novel',
        'badge_plain': 'Classic · Novel',
        'img': 'camus.jpg',
        'img_alt': 'The Outsider by Albert Camus — book cover',
        'author': 'Albert Camus',
        'year': '1942',
        'publisher': 'Gallimard',
        'description': "Meursault kills a man on an Algerian beach and feels nothing about it. What follows is one of the strangest and most important novels ever written — the founding text of literary absurdism.",
        'standfirst': "Meursault kills a man on an Algerian beach and feels nothing about it. What follows is one of the strangest and most important novels ever written — the founding text of literary absurdism.",
        'keywords': 'Camus Outsider review, The Stranger Camus, Camus classic novel absurdism',
        'verdict': "One of the great short novels. The opening line alone is worth the price. Everything after it earns the shock of that beginning.",
        'body': """<p>&ldquo;Mother died today. Or maybe yesterday; I can&rsquo;t be sure.&rdquo;</p>

<p>No opening line in twentieth-century fiction does more work. Camus published <em>The Outsider</em> in 1942, the same year as <em>The Myth of Sisyphus</em>, his philosophical essay on the absurd. The novel is the essay made flesh — but it is better than the essay, because Meursault is more interesting than any argument.</p>

<h2>Meursault</h2>
<p>He is a French Algerian office clerk. His mother dies; he does not cry at her funeral. He goes to the beach, meets a woman, watches a fight, and shoots a man — an Arab, unnamed, reduced to the sun glinting off his knife. He does not know why he shot him. He does not understand why the court is so interested in the question. The second half of the novel is his trial, in which the prosecutor cares far more about Meursault&rsquo;s failure to mourn than about the murder itself.</p>

<h2>The absurd made readable</h2>
<p>Camus&rsquo; point is that society cannot tolerate a man who refuses to perform the correct emotions. Meursault is condemned not for killing but for failing to be appropriately sorry, appropriately human, appropriately legible. The novel is a critique of social conformity dressed as a murder story. It is 123 pages and it changes how you see every interaction you have for weeks afterwards.</p>

<blockquote><p>&ldquo;I looked up at the mass of signs and stars in the night sky and laid myself open for the first time to the gentle indifference of the world.&rdquo;</p></blockquote>

<p>Sartre said it was the best French novel of the Occupation years. It is hard to disagree.</p>""",
        'related': [
            ('/what-is-flash-fiction.html', 'What Is Flash Fiction?'),
            ('/best-books-if-you-like-carver.html', 'Best Books If You Like Carver'),
            ('/reads.html', 'More Book Reviews'),
        ],
    },
]

PAGE_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-8B7DYTLXQC"></script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title_plain} — Review | Tumbleweed Words</title>
<meta name="description" content="{description}">
<meta name="keywords" content="{keywords}">
<meta name="author" content="David Moran — Tumbleweed Words">
<link rel="canonical" href="https://tumbleweedwords.com/{slug}.html">
<meta property="og:type" content="article">
<meta property="og:title" content="{title_plain} — Review">
<meta property="og:description" content="{description}">
<meta property="og:url" content="https://tumbleweedwords.com/{slug}.html">
<meta property="og:site_name" content="Tumbleweed Words">
<meta property="og:image" content="https://tumbleweedwords.com/paris-bookshop.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:creator" content="@tumbleweedwords">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{title_plain} — Review","description":"{description}","datePublished":"2026-03-25","dateModified":"2026-03-25","author":{{"@type":"Person","name":"David Moran","url":"https://tumbleweedwords.com/about.html","sameAs":["https://tumbleweedwords.substack.com"]}},"publisher":{{"@type":"Organization","name":"Tumbleweed Words","url":"https://tumbleweedwords.com"}},"mainEntityOfPage":{{"@type":"WebPage","@id":"https://tumbleweedwords.com/{slug}.html"}},"keywords":"{keywords}","image":"https://tumbleweedwords.com/paris-bookshop.jpg","url":"https://tumbleweedwords.com/{slug}.html"}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,400&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;1,8..60,300&display=swap" rel="stylesheet">
{styles_1}
{styles_2_with_book_css}
</head>
<body>
<div class="wrap">
{nav}
<main>
  <nav class="breadcrumb" aria-label="breadcrumb"><a href="/">Tumbleweed Words</a><span class="bc-sep">&rsaquo;</span><a href="/reads.html">Must Reads</a></nav>
  <span class="tag">Book Review <span class="review-badge">{badge}</span></span>
  <h1>{title}</h1>
  <p class="byline">By David Moran &middot; <time datetime="2026-03-25">2026-03-25</time></p>
  <p class="standfirst">{standfirst}</p>
  <img src="{img}" alt="{img_alt}" class="book-cover" loading="lazy">
  <div class="body">
{body}
  <div class="verdict"><div class="verdict-l">Verdict</div><p>{verdict}</p></div>
  <div class="cta-box">
    <div class="lbl">Tumbleweed Words &middot; Newsletter</div>
    <p>Flash fiction and poetry in the tradition of what you just read. Written on the road. Over 1,200 readers. Free.</p>
    <a href="https://tumbleweedwords.substack.com" target="_blank" rel="noopener">Read and subscribe &rarr;</a>
  </div>
  <div class="related"><span class="lbl">Keep reading</span><ul>{related_links}</ul></div>
  </div>
</main>
<section style="background:var(--bg2,#EDEBE3);border-top:2px solid var(--p,#5533E8);padding:4rem 2rem;text-align:center"><div style="max-width:560px;margin:0 auto"><h2 style="font-family:var(--fd,'Fraunces',Georgia,serif);font-size:clamp(1.2rem,2.5vw,1.65rem);font-weight:700;color:var(--ink,#1a1820);letter-spacing:-.02em;margin-bottom:.7rem;line-height:1.2">One piece a week, written from everywhere<br><em style="color:var(--p,#5533E8);font-style:normal">Sent to your inbox</em></h2><p style="font-family:var(--fb,'Source Serif 4',Georgia,serif);font-size:.82rem;color:var(--mu,#6B6880);line-height:1.75;margin-bottom:1.4rem;font-weight:300">Internationally published literary fiction and poetry, delivered in bitesize portions to your inbox. Free, every week.</p><form action="https://tumbleweedwords.substack.com/api/v1/free" method="post" target="_blank" style="display:flex;gap:.5rem;max-width:420px;margin:0 auto"><input type="email" name="email" placeholder="Your email address" required autocomplete="email" style="flex:1;background:#fff;border:1.5px solid var(--br,#D4D0C4);color:var(--ink,#1a1820);font-family:var(--fb,'Source Serif 4',Georgia,serif);font-size:.78rem;padding:.7rem 1rem;outline:none;transition:border-color .2s"><button type="submit" style="background:var(--p,#5533E8);color:#fff;font-family:var(--fm,ui-monospace,monospace);font-size:.54rem;letter-spacing:.1em;text-transform:uppercase;padding:.7rem 1.2rem;border:none;cursor:pointer;white-space:nowrap;transition:background .15s">Subscribe free &rarr;</button></form><p style="font-family:var(--fm,ui-monospace,monospace);font-size:.46rem;letter-spacing:.1em;text-transform:uppercase;color:var(--fa,#9896a8);margin-top:.7rem">Free &middot; Weekly &middot; No spam &middot; Unsubscribe any time</p></div></section>
<footer class="ft">
  <span class="ft-c">&copy; 2026 David &middot; Tumbleweed Words</span>
  <nav class="ft-l">
    <a href="https://tumbleweedwords.substack.com" target="_blank" rel="noopener">Newsletter</a>
    <a href="about.html">About</a>
    <a href="index.html">Writing</a>
  </nav>
</footer>
</div>
{popup}
{search_js}
{sub_bar}
{consent}
<script>(function(){{var b=document.querySelector('.body');var bl=document.querySelector('.byline');if(!b||!bl)return;var words=b.innerText.trim().split(/\\s+/).length;var mins=Math.max(1,Math.round(words/200));var sp=document.createElement('span');sp.textContent=' \u00b7 '+mins+' min read';bl.appendChild(sp);}})();</script>
</body>
</html>"""

styles_2_with_book_css = STYLES_2.replace(
    '.byline{font-family:ui-monospace',
    BOOK_COVER_CSS + '.byline{font-family:ui-monospace',
    1
)

written = []
for r in REVIEWS:
    related_links = ''.join(
        f'<li><a href="{href}">{label}</a></li>'
        for href, label in r['related']
    )
    html = PAGE_TEMPLATE.format(
        slug=r['slug'],
        title=r['title'],
        title_plain=r['title_plain'],
        badge=r['badge'],
        description=r['description'],
        standfirst=r['standfirst'],
        keywords=r['keywords'],
        verdict=r['verdict'],
        body=r['body'],
        img=r['img'],
        img_alt=r['img_alt'],
        author=r['author'],
        year=r['year'],
        publisher=r['publisher'],
        related_links=related_links,
        styles_1=STYLES_1,
        styles_2_with_book_css=styles_2_with_book_css,
        nav=NAV,
        popup=POPUP,
        search_js=SEARCH_JS,
        sub_bar=SUB_BAR,
        consent=CONSENT,
    )
    out = os.path.join(BASE, r['slug'] + '.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  Written: {r["slug"]}.html')
    written.append(r['slug'] + '.html')

# --- Update sitemap.xml ---
sm_path = os.path.join(BASE, 'sitemap.xml')
with open(sm_path, encoding='utf-8') as f:
    sm = f.read()

for fname in written:
    url = f'https://tumbleweedwords.com/{fname}'
    if url not in sm:
        entry = f'\n  <url>\n    <loc>{url}</loc>\n    <lastmod>2026-03-25</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>'
        sm = sm.replace('</urlset>', entry + '\n</urlset>')
        print(f'  Sitemap: added {fname}')

with open(sm_path, 'w', encoding='utf-8') as f:
    f.write(sm)

print('\nDone.')
