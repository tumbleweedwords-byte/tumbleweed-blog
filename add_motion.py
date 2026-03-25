"""
Add hover lifts and scroll fade-in to index.html and all-writing.html.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

SHADOW = '0 8px 24px rgba(85,51,232,.1)'

FADE_JS = (
    '<script>(function(){'
    'if(!("IntersectionObserver" in window))return;'
    'var css=".fade-in{opacity:0;transform:translateY(18px);transition:opacity .55s ease,transform .55s ease}'
    '.fade-in.visible{opacity:1;transform:none}";'
    'var st=document.createElement("style");st.textContent=css;document.head.appendChild(st);'
    'var sel=".sec,.bestof-sec,.pieces-sec,.writer-sec,.proof-bar,.pub-bar,.excerpt-sec,.scarcity,.final-sec,.photos-sec";'
    'var io=new IntersectionObserver(function(entries){'
    'entries.forEach(function(e){if(e.isIntersecting){e.target.classList.add("visible");io.unobserve(e.target);}});'
    '},{threshold:0.07,rootMargin:"0px 0px -40px 0px"});'
    'document.querySelectorAll(sel).forEach(function(el){el.classList.add("fade-in");io.observe(el);});'
    '})();</script>'
)

# ─── INDEX.HTML ───────────────────────────────────────────────────────────────
with open('C:/Users/tumbl/projects/tumbleewords/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. bestof-card: extend transition + lift on hover
c = c.replace(
    'transition:background .15s,border-color .2s;display:flex;flex-direction:column;gap:.4rem;text-decoration:none}'
    '.bestof-card:hover{background:var(--bg);border-color:var(--p)}',
    'transition:background .15s,border-color .2s,transform .2s,box-shadow .2s;display:flex;flex-direction:column;gap:.4rem;text-decoration:none}'
    f'.bestof-card:hover{{background:var(--bg);border-color:var(--p);transform:translateY(-3px);box-shadow:{SHADOW}}}'
)

# 2. piece-card: extend transition + lift on hover
c = c.replace(
    'transition:border-color .2s}.piece-card:hover{border-color:var(--p)}',
    f'transition:border-color .2s,transform .2s,box-shadow .2s}}'
    f'.piece-card:hover{{border-color:var(--p);transform:translateY(-3px);box-shadow:{SHADOW}}}'
)

# 3. Scroll fade-in JS before </body>
if '</body>' in c and FADE_JS not in c:
    c = c.replace('</body>', FADE_JS + '\n</body>')
    print('index.html: fade-in JS added.')

with open('C:/Users/tumbl/projects/tumbleewords/index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('index.html done.')

# ─── ALL-WRITING.HTML ─────────────────────────────────────────────────────────
with open('C:/Users/tumbl/projects/tumbleewords/all-writing.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. card-img: extend transition + lift + keep img filter
c = c.replace(
    '.card-img{border:1px solid var(--br);background:var(--bg);transition:background .15s;overflow:hidden;display:flex;flex-direction:column}'
    '.card-img:hover{background:var(--bg2)}',
    '.card-img{border:1px solid var(--br);background:var(--bg);transition:background .15s,transform .2s,box-shadow .2s;overflow:hidden;display:flex;flex-direction:column}'
    f'.card-img:hover{{background:var(--bg2);transform:translateY(-3px);box-shadow:{SHADOW}}}'
)

# 2. tool-card: extend transition + lift on hover
c = c.replace(
    'transition:background .15s}.tool-card:hover{background:var(--pl)}',
    f'transition:background .15s,transform .2s,box-shadow .2s}}'
    f'.tool-card:hover{{background:var(--pl);transform:translateY(-3px);box-shadow:{SHADOW}}}'
)

# 3. bestof-card on all-writing: extend transition + lift
c = c.replace(
    '.bestof-card{border:1px solid var(--br);background:var(--bg);padding:1.2rem;transition:background .15s;display:flex;flex-direction:column;gap:.4rem}'
    '.bestof-card:hover{background:var(--bg2)}',
    '.bestof-card{border:1px solid var(--br);background:var(--bg);padding:1.2rem;transition:background .15s,border-color .2s,transform .2s,box-shadow .2s;display:flex;flex-direction:column;gap:.4rem}'
    f'.bestof-card:hover{{background:var(--bg2);border-color:var(--p);transform:translateY(-3px);box-shadow:{SHADOW}}}'
)

# 4. bestof-hero: extend transition + lift
c = c.replace(
    'transition:border-color .2s;margin-bottom:1rem}.bestof-hero:hover{border-color:var(--p)}',
    f'transition:border-color .2s,transform .2s,box-shadow .2s;margin-bottom:1rem}}'
    f'.bestof-hero:hover{{border-color:var(--p);transform:translateY(-3px);box-shadow:{SHADOW}}}'
)

# 5. Scroll fade-in JS before </body>
if '</body>' in c and FADE_JS not in c:
    c = c.replace('</body>', FADE_JS + '\n</body>')
    print('all-writing.html: fade-in JS added.')

with open('C:/Users/tumbl/projects/tumbleewords/all-writing.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('all-writing.html done.')
