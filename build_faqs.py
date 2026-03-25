"""
Build 5 FAQ pages for tumbleweedwords.com
Extracts boilerplate from what-is-flash-fiction.html template.
"""
import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

BASE = 'C:/Users/tumbl/projects/tumbleewords'

# ── Extract boilerplate from template ─────────────────────────────────────────
with open(f'{BASE}/what-is-flash-fiction.html', 'r', encoding='utf-8') as f:
    TPL = f.read()

# GA block
GA = re.search(r'(<!-- Google tag.*?</script>)', TPL, re.DOTALL).group(1)
# Fonts link
FONTS = re.search(r'(<link rel="preconnect".*?display=swap" rel="stylesheet">)', TPL).group(1)
# First style block (base CSS)
STYLE1 = re.search(r'(<style>\s*\*,\*::before.*?</style>)', TPL, re.DOTALL).group(1)
# Second style block (nav overrides)
STYLE2 = re.search(r'(</style>\s*<style>\s*\.nav\{position:sticky.*?</style>)', TPL, re.DOTALL).group(1)
STYLE2 = STYLE2.strip().lstrip('</style>').strip()
if not STYLE2.startswith('<style>'):
    STYLE2 = '<style>' + STYLE2
# nsearch CSS style block
NSEARCH_CSS = re.search(r'(<style id="nsearch-css">.*?</style>)', TPL).group(1)
# Nav HTML
NAV_HTML = re.search(r'(<nav class="nav">.*?</nav>)', TPL).group(1)
# Subscribe section
SUB_SECTION = re.search(r'(<section style="background:var\(--bg2.*?</section>)', TPL, re.DOTALL).group(1)
# Footer
FOOTER = re.search(r'(<footer class="ft">.*?</footer>)', TPL, re.DOTALL).group(1)
# Popup style + HTML
POPUP = re.search(r'(<style>#tw-popup-overlay.*?</script>)', TPL, re.DOTALL).group(1)
# Search script
SEARCH_JS = re.search(r'(<script>\(function\(\)\{var t=document\.getElementById\(\'searchToggle.*?</script>)', TPL).group(1)
# Sub-bar
SUBBAR = re.search(r'(<style id="sub-bar-css">.*?</div>\s*$)', TPL, re.DOTALL)
SUBBAR_HTML = SUBBAR.group(1) if SUBBAR else ''
# Consent div
CONSENT = re.search(r'(<div id="tw-consent".*?display:none.*?></div>)', TPL).group(1)

# ── CSS for details/summary FAQ accordion ────────────────────────────────────
FAQ_CSS = """
.faq-list{margin:2rem 0}
details{border-bottom:1px solid var(--br);padding:1rem 0}
details:first-of-type{border-top:1px solid var(--br)}
summary{font-family:var(--fd);font-size:1.05rem;font-weight:600;color:var(--txt);cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:baseline;gap:1rem;padding:.2rem 0}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";font-family:var(--fm);font-size:.9rem;color:var(--p);flex-shrink:0;transition:transform .2s}
details[open] summary::after{content:"\\2212"}
.faq-answer{padding:1rem 0 .5rem;color:var(--txt2);font-size:.92rem;line-height:1.82}
.faq-answer p{margin-bottom:.9rem}
.faq-answer a{color:var(--p);border-bottom:1px solid var(--pl2)}.faq-answer a:hover{border-color:var(--p)}
.faq-read{font-family:var(--fm);font-size:.56rem;letter-spacing:.12em;text-transform:uppercase;color:var(--p);display:inline-block;margin-top:.4rem;border-bottom:none!important}
.faq-hub-grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:2rem 0}
@media(max-width:600px){.faq-hub-grid{grid-template-columns:1fr}}
.faq-hub-card{border:1px solid var(--br);background:var(--bg2);padding:1.4rem 1.6rem;text-decoration:none;display:block;transition:border-color .2s,transform .2s,box-shadow .2s}
.faq-hub-card:hover{border-color:var(--p);transform:translateY(-2px);box-shadow:0 6px 20px rgba(85,51,232,.1)}
.faq-hub-card .lbl{font-family:var(--fm);font-size:.52rem;letter-spacing:.16em;text-transform:uppercase;color:var(--p);margin-bottom:.5rem;display:block}
.faq-hub-card h3{font-family:var(--fd);font-size:1rem;font-weight:600;color:var(--txt);margin-bottom:.4rem}
.faq-hub-card p{font-size:.82rem;color:var(--mu);line-height:1.6;margin:0}"""

def breadcrumb_html(items):
    # items = list of (label, url) — last item has no url
    parts = []
    for i, (label, url) in enumerate(items):
        if url:
            parts.append(f'<a href="{url}">{label}</a>')
        else:
            parts.append(f'<span>{label}</span>')
    sep = '<span class="bc-sep">&rsaquo;</span>'
    return f'<nav class="breadcrumb" aria-label="breadcrumb">{sep.join(parts)}</nav>'

def breadcrumb_schema(items):
    entities = []
    for i, (label, url) in enumerate(items):
        entities.append({"@type":"ListItem","position":i+1,"name":label,"item":url})
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":entities}

def faq_schema(faqs):
    # faqs = list of (question_str, answer_plain_str)
    entities = []
    for q, a in faqs:
        entities.append({"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}})
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":entities}

def article_schema(title, desc, url, image, pub_date):
    return {
        "@context":"https://schema.org","@type":"Article",
        "headline":title,"description":desc,
        "author":{"@type":"Person","name":"David Moran","url":"https://tumbleweedwords.com/about.html","sameAs":["https://tumbleweedwords.substack.com"]},
        "publisher":{"@type":"Organization","name":"Tumbleweed Words","url":"https://tumbleweedwords.com"},
        "datePublished":pub_date,"dateModified":"2026-03-24",
        "image":image,"url":url,
        "mainEntityOfPage":{"@type":"WebPage","@id":url}
    }

def details_block(faqs_html):
    # faqs_html = list of (question_str, answer_html, read_more_html)
    out = ['<div class="faq-list">']
    for q, a_html, rm_html in faqs_html:
        out.append(f'''<details>
<summary>{q}</summary>
<div class="faq-answer">
<p>{a_html}</p>
{f'<a class="faq-read" href="{rm_html[0]}">{rm_html[1]} &rarr;</a>' if rm_html else ''}
</div>
</details>''')
    out.append('</div>')
    return '\n'.join(out)

def related_block(links):
    items = ''.join(f'<li><a href="{url}">{label}</a></li>' for label, url in links)
    return f'<div class="related"><span class="lbl">Keep reading</span><ul>{items}</ul></div>'

def build_page(fname, title, desc, keywords, og_image, canonical,
               bc_items, tag, h1, standfirst, main_content,
               schemas, related):

    schema_tags = ''.join(
        f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>\n'
        for s in schemas
    )

    bc_html = breadcrumb_html(bc_items)

    rel_html = related_block(related)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
{GA}

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<meta name="author" content="David Moran — Tumbleweed Words">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="Tumbleweed Words">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:creator" content="@tumbleweedwords">
{schema_tags}{FONTS}
{STYLE1}
{STYLE2}
<style>{FAQ_CSS}</style>
<style>.breadcrumb{{font-family:ui-monospace,"SF Mono",monospace;font-size:.48rem;letter-spacing:.08em;text-transform:uppercase;color:#9896a8;padding:.55rem 2.5rem;background:#F6F4EE;border-bottom:1px solid #D4D0C4;display:flex;align-items:center}}.breadcrumb a{{color:#6B6880;text-decoration:none}}.breadcrumb a:hover{{color:#5533E8}}.bc-sep{{margin:0 .4rem;color:#D4D0C4}}</style>
{NSEARCH_CSS}
</head>
<body>
<div class="wrap">
{NAV_HTML}
<main>
{bc_html}
  <span class="tag">{tag}</span>
  <h1>{h1}</h1>
  <p class="standfirst">{standfirst}</p>
  <div class="body">
{main_content}
  <div class="cta-box">
    <div class="lbl">Tumbleweed Words &middot; Substack Newsletter</div>
    <p>Gritty, minimalist fiction and poetry — written on trains, in borrowed rooms, in cities I am passing through. Over 1,200 readers. Free to subscribe.</p>
    <a href="https://tumbleweedwords.substack.com" target="_blank" rel="noopener">Read and subscribe &rarr;</a>
  </div>
{rel_html}
  </div>
</main>
{SUB_SECTION}
{FOOTER}
</div>
{POPUP}
{SEARCH_JS}
{SUBBAR_HTML}
{CONSENT}
</body>
</html>"""
    with open(f'{BASE}/{fname}', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  Written: {fname}')


# ══════════════════════════════════════════════════════════════════════════════
# 1. FAQ HUB
# ══════════════════════════════════════════════════════════════════════════════
hub_content = """<div class="faq-hub-grid">
<a class="faq-hub-card" href="/faq-flash-fiction.html">
  <span class="lbl">Flash Fiction</span>
  <h3>Flash Fiction FAQ</h3>
  <p>What is flash fiction? How long? Where to publish? How to write it?</p>
</a>
<a class="faq-hub-card" href="/faq-literary-craft.html">
  <span class="lbl">Literary Craft</span>
  <h3>Literary Craft FAQ</h3>
  <p>Iceberg theory, show don&rsquo;t tell, minimalism, prose poems, endings.</p>
</a>
<a class="faq-hub-card" href="/faq-writing-life.html">
  <span class="lbl">Writing Life</span>
  <h3>Writing Life FAQ</h3>
  <p>Dirty realism, the Pushcart Prize, literary magazines, submitting work.</p>
</a>
<a class="faq-hub-card" href="/faq-reading.html">
  <span class="lbl">Reading</span>
  <h3>Reading FAQ</h3>
  <p>Best flash fiction writers, best literary magazines, what to read next.</p>
</a>
</div>"""

hub_schemas = [
    article_schema(
        'FAQ — Your Literary Questions Answered',
        'Answers to the most common questions about flash fiction, literary craft, the writing life, and reading.',
        'https://tumbleweedwords.com/faq.html',
        'https://tumbleweedwords.com/hero-1.jpg',
        '2026-03-24'
    ),
    breadcrumb_schema([
        ('Tumbleweed Words','https://tumbleweedwords.com'),
        ('FAQ','https://tumbleweedwords.com/faq.html'),
    ])
]

build_page(
    'faq.html',
    'FAQ — Your Literary Questions Answered | Tumbleweed Words',
    'Answers to the most common questions about flash fiction, literary craft, the writing life, and reading.',
    'flash fiction faq, literary craft questions, writing life faq, what is flash fiction',
    'https://tumbleweedwords.com/hero-1.jpg',
    'https://tumbleweedwords.com/faq.html',
    [('Tumbleweed Words','/'),('FAQ',None)],
    'Reference',
    'Frequently Asked Questions',
    'Answers to the most common questions about flash fiction, literary craft, the writing life, and reading. Each answer links to a full essay.',
    hub_content,
    hub_schemas,
    [
        ('Flash Fiction FAQ','/faq-flash-fiction.html'),
        ('Literary Craft FAQ','/faq-literary-craft.html'),
        ('Writing Life FAQ','/faq-writing-life.html'),
        ('Reading FAQ','/faq-reading.html'),
        ('All Writing — Fiction & Poetry','/all-writing.html'),
    ]
)

# ══════════════════════════════════════════════════════════════════════════════
# 2. FLASH FICTION FAQ
# ══════════════════════════════════════════════════════════════════════════════
ff_faqs_html = [
    ("What is flash fiction?",
     "Flash fiction is a complete short story told in under 1,000 words. Unlike a vignette or a scene, it must contain a beginning, a middle, and an end \u2014 fully realised within an impossibly compressed space. The form has many names depending on length: sudden fiction (under 2,000 words), micro fiction (under 300 words), hint fiction (under 25 words). What unites them is completeness. A flash fiction piece is not a fragment. It is a story that implies more than it says, trusts the reader to fill the spaces, and earns its ending. The form has roots in Chekhov and Hemingway, though neither called it by that name. Today it is one of the most published forms in literary journals worldwide.",
     ('/what-is-flash-fiction.html','What Is Flash Fiction? A Complete Guide')),
    ("How long is flash fiction?",
     "Flash fiction is generally defined as any story under 1,000 words, though definitions vary widely. Sudden fiction typically runs between 750 and 2,000 words. Micro fiction is usually under 300 words. Nano fiction pushes below 100 words. The useful working definition for most literary journals is: flash fiction fits on a single page or screen. The most important constraint is not the word count but the requirement for completeness \u2014 a flash piece must feel whole, not truncated. A 900-word story that trails off is not flash fiction. A 400-word story with a fully realised arc is.",
     ('/how-long-should-flash-fiction-be.html','How Long Should Flash Fiction Be?')),
    ("What\u2019s the difference between flash fiction and a short story?",
     "The short story can develop. It has room for backstory, secondary characters, and the slow accumulation of detail that builds a world. Flash fiction has none of that room. The short story explains. Flash fiction implies. Where a short story might take three paragraphs to establish character, a flash piece must do it in a sentence \u2014 often in the reader\u2019s imagination rather than on the page. Flash fiction is closer to the lyric poem in its relationship between what is written and what is meant: it works in implication, compression, and the charged single detail that carries the weight of an entire history.",
     ('/flash-fiction-vs-short-story.html','Flash Fiction vs Short Story')),
    ("Where can I publish flash fiction?",
     "The major literary journals publishing flash fiction include SmokeLong Quarterly, Flash Fiction Online, The Sun Magazine, Wigleaf, and Fractured Lit. Many top literary journals \u2014 The Missouri Review, Ploughshares, Tin House \u2014 also accept flash as part of their regular submissions. Response times vary enormously: from one week to over a year. For a Pushcart Prize nomination, aim for established journals with strong editorial standards. Use the literary magazine finder to filter by form, pay rate, and response time so you can match your piece to the right journal.",
     ('/literary-magazine-finder.html','Find Your Literary Magazine')),
    ("How do I write flash fiction?",
     "The single most important technique in flash fiction is compression without truncation. Every word must do more than one job. Every sentence must carry character, image, and momentum simultaneously. Begin as late as possible in the story \u2014 the moment just before something changes. End as early as possible \u2014 the moment just after. The gap between the last line and the rest of the story is where the reader lives. Trust that gap. Avoid explanation. Use concrete, specific detail rather than abstraction: one well-chosen detail does more work than three general ones. The best flash fiction leaves the reader understanding something they were never told.",
     ('/how-to-write-flash-fiction.html','How to Write Flash Fiction')),
    ("What are the best flash fiction examples?",
     "The canonical examples include Amy Hempel\u2019s \u201cIn the Cemetery Where Al Jolson Is Buried,\u201d Lydia Davis\u2019s compressed fictions, and Grace Paley\u2019s \u201cWants.\u201d For contemporary flash, read SmokeLong Quarterly\u2019s archive. For flash crossing into prose poetry, read Claudia Rankine. For flash that operates through pure implication and restraint, read the short prose of Yasunari Kawabata. Among living writers, Colin Barrett, Diane Cook, and Tessa Hadley consistently produce work that demonstrates what the form can do at its best. Read widely in the form before writing it.",
     ('/best-flash-fiction-stories.html','Best Flash Fiction Stories')),
]

ff_faqs_plain = [(q, re.sub(r'<[^>]+>', '', a)) for q, a, _ in ff_faqs_html]

ff_schemas = [
    faq_schema(ff_faqs_plain),
    article_schema(
        'Flash Fiction FAQ \u2014 Questions Answered',
        'Answers to the most common questions about flash fiction \u2014 what it is, how long, where to publish, and how to write it.',
        'https://tumbleweedwords.com/faq-flash-fiction.html',
        'https://tumbleweedwords.com/hero-1.jpg','2026-03-24'),
    breadcrumb_schema([
        ('Tumbleweed Words','https://tumbleweedwords.com'),
        ('FAQ','https://tumbleweedwords.com/faq.html'),
        ('Flash Fiction','https://tumbleweedwords.com/faq-flash-fiction.html'),
    ])
]

build_page(
    'faq-flash-fiction.html',
    'Flash Fiction FAQ \u2014 Questions Answered | Tumbleweed Words',
    'Answers to the most common questions about flash fiction \u2014 what it is, how long it is, how it differs from a short story, where to publish, and how to write it.',
    'what is flash fiction, flash fiction length, flash fiction vs short story, where to publish flash fiction, how to write flash fiction',
    'https://tumbleweedwords.com/hero-1.jpg',
    'https://tumbleweedwords.com/faq-flash-fiction.html',
    [('Tumbleweed Words','/'),('FAQ','/faq.html'),('Flash Fiction',None)],
    'Flash Fiction',
    'Flash Fiction \u2014 Frequently Asked Questions',
    'The most common questions about flash fiction, from definition to publication. Each answer links to a full essay.',
    details_block(ff_faqs_html),
    ff_schemas,
    [
        ('What Is Flash Fiction? A Complete Guide','/what-is-flash-fiction.html'),
        ('Flash Fiction vs Short Story','/flash-fiction-vs-short-story.html'),
        ('How to Write Flash Fiction','/how-to-write-flash-fiction.html'),
        ('Literary Magazine Finder','/literary-magazine-finder.html'),
        ('Read \u2014 train in vain | flash fiction from Berlin','/street-legal.html'),
    ]
)

# ══════════════════════════════════════════════════════════════════════════════
# 3. LITERARY CRAFT FAQ
# ══════════════════════════════════════════════════════════════════════════════
lc_faqs_html = [
    ("What is the iceberg theory?",
     "The iceberg theory is Ernest Hemingway\u2019s principle that the deeper meaning of a story should never appear on the surface. \u201cThe dignity of movement of an iceberg,\u201d he wrote, \u201cis due to only one-eighth of it being above water.\u201d The writer knows the full history, psychology, and context of every character and event \u2014 but conveys only a fraction of it directly. The reader senses the weight of the submerged seven-eighths through implication, through what is left out, through the precision of surface detail. It is one of the foundational principles of minimalist fiction, and the reason Hemingway\u2019s shortest scenes carry such pressure even when almost nothing appears to happen.",
     ('/what-is-the-iceberg-theory.html','What Is the Iceberg Theory?')),
    ("What does \u201cshow don\u2019t tell\u201d mean?",
     "Show don\u2019t tell is the craft principle that experience should be rendered rather than reported. Instead of writing \u201cshe was sad,\u201d you write the specific, observable behaviour: \u201cshe folded and refolded the letter until the paper wore through at the creases.\u201d The reader arrives at emotion through detail rather than being handed the conclusion. But it is not an absolute rule. Summary, telling, and direct emotional statement all have legitimate places in fiction. The instruction is better understood as: don\u2019t default to abstraction when a concrete detail would do more work. The mistake is not telling \u2014 it\u2019s telling when showing would be truer, more precise, and more alive.",
     ('/show-dont-tell-what-it-actually-means.html','Show Don\u2019t Tell \u2014 What It Actually Means')),
    ("What is minimalist fiction?",
     "Minimalist fiction strips language, plot, and character to essential elements \u2014 removing anything that can be cut without destroying meaning. The movement is associated with Raymond Carver, Amy Hempel, Mary Robison, and Ann Beattie, writing in America in the 1970s and 1980s. Its hallmarks are plain prose, working-class settings, economic anxiety, flat affect, and endings that refuse resolution. The style demands more from the reader: meaning is constructed in the gap between what is said and what is clearly felt but never named. Gordon Lish, as Carver\u2019s editor, pushed this aesthetic to an extreme \u2014 some argue too far, suppressing the warmth that Carver\u2019s own drafts contained.",
     ('/post-minimalist-fiction.html','Minimalist Fiction \u2014 The Techniques That Work')),
    ("How do you end a short story?",
     "The ending of a short story is not a conclusion \u2014 it is a detonation. The best endings reframe everything that came before: the reader rereads the opening line differently. The worst endings explain what has just happened, robbing the reader of the discovery. A strong ending arrives at the last possible responsible moment: as early as the story can afford to stop. It should be inevitable in retrospect but surprising on first reading. In flash fiction specifically, the last line often does double duty \u2014 it closes the story and opens a larger implication simultaneously. Never end with a character realising something. End with them doing something.",
     ('/how-to-end-a-flash-fiction-story.html','How to End a Flash Fiction Story')),
    ("What is a prose poem?",
     "A prose poem is a piece of writing that occupies the intersection between prose and poetry \u2014 written in full sentences without line breaks, but using the compression, sonic intensity, and imagistic logic of poetry rather than narrative. Claudia Rankine, Russell Edson, and Carolyn Forch\u00e9 work extensively in the form. The prose poem resists story in a way that flash fiction does not \u2014 where flash requires narrative arc, a prose poem may be purely lyric, associative, or fragmented. The question of whether a piece is prose or poetry is not a failure of categorisation but often the point of the work itself: the form thrives in the uncertainty.",
     ('/prose-poetry-vs-flash-fiction.html','Prose Poetry vs Flash Fiction')),
]

lc_faqs_plain = [(q, re.sub(r'<[^>]+>', '', a)) for q, a, _ in lc_faqs_html]

lc_schemas = [
    faq_schema(lc_faqs_plain),
    article_schema(
        'Literary Craft FAQ \u2014 Iceberg Theory, Show Don\u2019t Tell & More',
        'Answers to common questions about literary craft \u2014 the iceberg theory, show don\u2019t tell, minimalist fiction, prose poems, and how to end a story.',
        'https://tumbleweedwords.com/faq-literary-craft.html',
        'https://tumbleweedwords.com/hemingway.jpg','2026-03-24'),
    breadcrumb_schema([
        ('Tumbleweed Words','https://tumbleweedwords.com'),
        ('FAQ','https://tumbleweedwords.com/faq.html'),
        ('Literary Craft','https://tumbleweedwords.com/faq-literary-craft.html'),
    ])
]

build_page(
    'faq-literary-craft.html',
    'Literary Craft FAQ \u2014 Iceberg Theory, Show Don\u2019t Tell & More | Tumbleweed Words',
    'Answers to common questions about literary craft \u2014 the iceberg theory, show don\u2019t tell, minimalist fiction, prose poems, and how to end a story.',
    'iceberg theory, show dont tell, minimalist fiction, prose poem, how to end a short story',
    'https://tumbleweedwords.com/hemingway.jpg',
    'https://tumbleweedwords.com/faq-literary-craft.html',
    [('Tumbleweed Words','/'),('FAQ','/faq.html'),('Literary Craft',None)],
    'Literary Craft',
    'Literary Craft \u2014 Frequently Asked Questions',
    'Common questions about the techniques and principles that underpin serious literary fiction and poetry.',
    details_block(lc_faqs_html),
    lc_schemas,
    [
        ('What Is the Iceberg Theory?','/what-is-the-iceberg-theory.html'),
        ('Minimalist Fiction \u2014 The Techniques That Work','/post-minimalist-fiction.html'),
        ('Show Don\u2019t Tell \u2014 What It Actually Means','/show-dont-tell-what-it-actually-means.html'),
        ('Influenced by Raymond Carver','/influenced-by-raymond-carver.html'),
        ('Read \u2014 an expat in paris','/an-expat-in-paris.html'),
    ]
)

# ══════════════════════════════════════════════════════════════════════════════
# 4. WRITING LIFE FAQ
# ══════════════════════════════════════════════════════════════════════════════
wl_faqs_html = [
    ("What is dirty realism?",
     "Dirty realism is a term coined by editor Bill Buford in the 1983 Granta issue \u201cDirty Realism\u201d to describe a generation of American writers \u2014 Raymond Carver, Tobias Wolff, Richard Ford, Bobbie Ann Mason, Frederick Barthelme \u2014 writing short, compressed fiction about ordinary people in economic difficulty. The prose is plain, the subjects unglamorous: supermarkets, trailer parks, failed marriages, low-wage jobs. The emotional register is one of restraint: large feelings expressed through small, precise actions. It is distinct from naturalism or social realism in its compression and its refusal of explanation. The dirty realist story does not argue. It depicts, and trusts the depiction to carry the weight.",
     ('/what-is-dirty-realism.html','What Is Dirty Realism?')),
    ("What is sudden fiction?",
     "Sudden fiction is a term for very short short stories, typically between 750 and 2,000 words. The term was popularised by the 1986 anthology Sudden Fiction: American Short-Short Stories, edited by Robert Shapard and James Thomas, which collected work by Carver, Oates, Paley, and others. It sits between flash fiction and the conventional short story in length, and shares flash fiction\u2019s demand for compression and implication. Many writers use sudden fiction and flash fiction interchangeably; others use sudden fiction specifically for pieces that have slightly more room to develop character and situation before the turn or the closing image.",
     ('/what-is-sudden-fiction.html','What Is Sudden Fiction?')),
    ("What is nomadic writing?",
     "Nomadic writing is writing produced in movement \u2014 on trains, in rented rooms, in cities the writer is passing through rather than settled in. The condition creates a particular kind of attention: heightened observation of the unfamiliar, a relationship with place that is always partly departure, an emotional register shaped by impermanence. Writers associated with nomadic sensibilities include Bruce Chatwin, W.G. Sebald, Rebecca Solnit, and Ryszard Kapu\u015bci\u0144ski. Tumbleweed Words publishes literary fiction and poetry written on the road \u2014 pieces where the condition of movement is not the subject but the atmosphere the prose is soaked in.",
     ('/nomadic-writing-what-is-it.html','Nomadic Writing \u2014 What Is It?')),
    ("Where should I submit short fiction?",
     "Start with journals that match your aesthetic rather than prestige alone. For compressed, minimalist work: SmokeLong Quarterly, Wigleaf, Fractured Lit, Flash Fiction Online. For longer short fiction: Tin House, One Story, The Missouri Review. For international journals: The Stinging Fly (Ireland), Granta, and Litro. Always read at least three issues before submitting \u2014 you are looking for editors who respond to work like yours. Simultaneous submissions are accepted by most magazines but require immediate withdrawal if accepted elsewhere. Use the literary magazine finder to filter by genre, pay rate, and response time.",
     ('/literary-magazine-finder.html','Literary Magazine Finder')),
    ("How do literary magazines work?",
     "Literary magazines operate on a submissions model. Writers send unpublished work during open submission windows \u2014 typically through Submittable or by email. Editors often read blind. Acceptance rates at top journals run between 0.5% and 3%. Most magazines do not pay, or pay a token amount; a handful \u2014 The Sun, One Story, Tin House \u2014 pay professional rates. Simultaneous submissions are accepted by most magazines but require immediate withdrawal if accepted elsewhere. Response times range from weeks to over a year. Rejection is the majority experience for every working writer at every stage of their career. The work is to keep sending.",
     ('/post-literary-magazines.html','How Literary Magazines Work')),
    ("What is a Pushcart Prize?",
     "The Pushcart Prize is one of the most prestigious literary awards in American publishing. Founded by Bill Henderson in 1976, it honours the best short fiction, poetry, and essays published in small presses and literary magazines each year. Editors of literary journals nominate work they have published \u2014 each journal can nominate a limited number of pieces. Guest editors then select the final anthology from thousands of nominations. A Pushcart nomination alone, even without selection for the anthology, carries significant weight in the literary world and in academic creative writing contexts. The anthology is published annually and serves as a map of the best of independent American literary publishing.",
     ('/pushcart-prize-what-is-it.html','What Is the Pushcart Prize?')),
]

wl_faqs_plain = [(q, re.sub(r'<[^>]+>', '', a)) for q, a, _ in wl_faqs_html]

wl_schemas = [
    faq_schema(wl_faqs_plain),
    article_schema(
        'Writing Life FAQ \u2014 Dirty Realism, Submissions & Literary Prizes',
        'Answers to common questions about the writing life \u2014 dirty realism, sudden fiction, submitting to literary magazines, and what the Pushcart Prize is.',
        'https://tumbleweedwords.com/faq-writing-life.html',
        'https://tumbleweedwords.com/hero-1.jpg','2026-03-24'),
    breadcrumb_schema([
        ('Tumbleweed Words','https://tumbleweedwords.com'),
        ('FAQ','https://tumbleweedwords.com/faq.html'),
        ('Writing Life','https://tumbleweedwords.com/faq-writing-life.html'),
    ])
]

build_page(
    'faq-writing-life.html',
    'Writing Life FAQ \u2014 Dirty Realism, Submissions & Literary Prizes | Tumbleweed Words',
    'Answers to common questions about the writing life \u2014 dirty realism, sudden fiction, submitting to literary magazines, and what the Pushcart Prize is.',
    'dirty realism, sudden fiction, what is the pushcart prize, how to submit to literary magazines, nomadic writing',
    'https://tumbleweedwords.com/hero-1.jpg',
    'https://tumbleweedwords.com/faq-writing-life.html',
    [('Tumbleweed Words','/'),('FAQ','/faq.html'),('Writing Life',None)],
    'Writing Life',
    'Writing Life \u2014 Frequently Asked Questions',
    'Common questions about terms, movements, and practicalities for writers working in literary fiction and poetry.',
    details_block(wl_faqs_html),
    wl_schemas,
    [
        ('What Is Dirty Realism?','/what-is-dirty-realism.html'),
        ('Literary Magazine Finder','/literary-magazine-finder.html'),
        ('What Is the Pushcart Prize?','/pushcart-prize-what-is-it.html'),
        ('Influenced by Raymond Carver','/influenced-by-raymond-carver.html'),
        ('Read \u2014 an honest pursuit | literary manifesto','/honest-pursuit.html'),
    ]
)

# ══════════════════════════════════════════════════════════════════════════════
# 5. READING FAQ
# ══════════════════════════════════════════════════════════════════════════════
rd_faqs_html = [
    ("Who are the best flash fiction writers?",
     "The writers most associated with flash fiction and the compressed short story form are Raymond Carver (foundational), Amy Hempel (the most technically precise \u2014 start with Reasons to Live), Lydia Davis (the most formally inventive), Grace Paley (the most emotionally generous), and Tessa Hadley (one of the most consistently excellent contemporary practitioners). For prose poetry crossing into flash, read Claudia Rankine. For international flash, Yasunari Kawabata\u2019s Palm-of-the-Hand Stories and Borges\u2019s Fictions represent the form at its most compressed and strange. Among living writers, read Diane Cook, Colin Barrett, and Yuko Tsushima.",
     ('/best-flash-fiction-stories.html','Best Flash Fiction Stories')),
    ("What are the best literary magazines?",
     "The magazines that consistently publish the best short fiction and poetry: The Sun (pays well, deeply literary), Tin House (reliably excellent), One Story (single-story format, high selectivity), The Missouri Review, The Kenyon Review, and Ploughshares. For flash specifically: SmokeLong Quarterly, Wigleaf, Fractured Lit. For poetry: Poetry Magazine, The Paris Review, and The Rumpus. For international literary fiction: Granta, The Dublin Review, and The Stinging Fly. The New Yorker remains the most widely read literary venue for fiction. For essays and criticism: n+1, The Point, and the Los Angeles Review of Books.",
     ('/reads.html','Must Reads')),
    ("What should I read if I like Raymond Carver?",
     "If you respond to Carver\u2019s compression, restraint, and domestic subject matter, read: Amy Hempel (all four collections, start with Reasons to Live), Tobias Wolff (The Night in Question), Mary Robison (Why Did I Ever), Richard Ford (Rock Springs), and Bobbie Ann Mason (Shiloh). For the European equivalent of Carver\u2019s minimalism, read Peter Handke\u2019s short prose. For something darker and stranger, read Denis Johnson (Jesus\u2019 Son) and Barry Hannah (Airships). Gordon Lish edited both Carver and Hempel \u2014 reading the two together reveals how much of the minimalist aesthetic was editorial construction as much as individual voice.",
     ('/best-books-if-you-like-carver.html','Best Books If You Like Carver')),
    ("What are the best poetry newsletters?",
     "The best poetry newsletters for readers of serious literary work include the Poetry Foundation\u2019s daily poem, the Academy of American Poets\u2019 poem-a-day, and The Paris Review\u2019s poetry dispatches. For newsletter-first poetry publishing, Substack has become a serious venue \u2014 look for poets publishing original work directly to subscribers rather than aggregating links. Tumbleweed Words publishes original flash fiction and poetry directly to subscribers every week \u2014 work written on the road, in the tradition of the compressed lyric. The best newsletters are distinguished by a strong editorial voice and a commitment to original work over curation alone.",
     ('https://tumbleweedwords.substack.com','Subscribe to Tumbleweed Words')),
]

rd_faqs_plain = [(q, re.sub(r'<[^>]+>', '', a)) for q, a, _ in rd_faqs_html]

rd_schemas = [
    faq_schema(rd_faqs_plain),
    article_schema(
        'Reading FAQ \u2014 Best Flash Fiction Writers & Literary Magazines',
        'Answers to common reading questions \u2014 the best flash fiction writers, best literary magazines, what to read if you like Raymond Carver, and the best poetry newsletters.',
        'https://tumbleweedwords.com/faq-reading.html',
        'https://tumbleweedwords.com/paris-bookshop.jpg','2026-03-24'),
    breadcrumb_schema([
        ('Tumbleweed Words','https://tumbleweedwords.com'),
        ('FAQ','https://tumbleweedwords.com/faq.html'),
        ('Reading','https://tumbleweedwords.com/faq-reading.html'),
    ])
]

build_page(
    'faq-reading.html',
    'Reading FAQ \u2014 Best Flash Fiction Writers & Literary Magazines | Tumbleweed Words',
    'Answers to common reading questions \u2014 the best flash fiction writers, best literary magazines, what to read if you like Raymond Carver, and the best poetry newsletters.',
    'best flash fiction writers, best literary magazines, what to read if you like raymond carver, best poetry newsletters',
    'https://tumbleweedwords.com/paris-bookshop.jpg',
    'https://tumbleweedwords.com/faq-reading.html',
    [('Tumbleweed Words','/'),('FAQ','/faq.html'),('Reading',None)],
    'Reading',
    'Reading \u2014 Frequently Asked Questions',
    'Common questions about who to read, where to find the best literary work, and what to reach for next.',
    details_block(rd_faqs_html),
    rd_schemas,
    [
        ('Best Books If You Like Carver','/best-books-if-you-like-carver.html'),
        ('Must Reads','/reads.html'),
        ('Best Flash Fiction Collections','/best-flash-fiction-collections.html'),
        ('Influenced by Amy Hempel','/influenced-by-amy-hempel.html'),
        ('Read \u2014 an expat in paris','/an-expat-in-paris.html'),
    ]
)

# ── Update sitemap ─────────────────────────────────────────────────────────
with open(f'{BASE}/sitemap.xml', 'r', encoding='utf-8') as f:
    sm = f.read()

new_pages = ['faq.html','faq-flash-fiction.html','faq-literary-craft.html','faq-writing-life.html','faq-reading.html']
for p in new_pages:
    url = f'https://tumbleweedwords.com/{p}'
    if url not in sm:
        entry = f'  <url>\n    <loc>{url}</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n'
        sm = sm.replace('</urlset>', entry + '</urlset>')
        print(f'  Sitemap: added {p}')

with open(f'{BASE}/sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sm)

print('\nDone.')
