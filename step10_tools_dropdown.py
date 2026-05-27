"""
Step 10: Restructure Tools nav link into a dropdown.

Desktop nav: Replace <a href="/essays-and-culture.html#tools" class="nlink hide-m">Tools</a>
             with a dropdown button + menu.

Mobile nav: Replace <a href="/essays-and-culture.html#tools">Tools</a>
            with a collapsible group containing 4 tool links.

Footer: Remove <a href="/podcasts.html">Podcasts</a> from footer nav.

Also update final-links section where Tools link appears.
"""
import os, re, glob

SITE_DIR = r"C:\Users\tumbl\projects\tumbleewords"

# ---- Desktop dropdown HTML ----
DROPDOWN_CSS = """<style id="tools-dropdown-css">
.ndrop{position:relative;display:inline-flex;align-items:center}
.ndrop-btn{background:none;border:none;cursor:pointer;font-family:'Courier New',Courier,monospace;font-size:18px;font-weight:700;color:#000;transition:color .15s;white-space:nowrap;letter-spacing:0.5px;padding:0;display:flex;align-items:center;gap:2px;line-height:1}
.ndrop-btn:hover,.ndrop.open .ndrop-btn{color:#5533E8}
.ndrop-btn svg{transition:transform .2s}
.ndrop.open .ndrop-btn svg{transform:rotate(180deg)}
.ndrop-menu{display:none;position:absolute;top:calc(100% + 10px);left:50%;transform:translateX(-50%);background:#fff;border:1.5px solid #5533E8;min-width:210px;z-index:300;box-shadow:0 4px 20px rgba(85,51,232,.15)}
.ndrop.open .ndrop-menu{display:block}
.ndrop-menu a{display:block;padding:.7rem 1.1rem;font-family:'Courier New',Courier,monospace;font-size:14px;font-weight:700;color:#1a1820;text-decoration:none;transition:background .15s,color .15s;white-space:nowrap;border-bottom:1px solid #D4D0C4}
.ndrop-menu a:last-child{border-bottom:none}
.ndrop-menu a:hover{background:#EEEDFE;color:#5533E8}
.mm-tools-group{border-bottom:1px solid #D4D0C4}
.mm-tools-toggle{background:none;border:none;width:100%;text-align:left;font-family:'Courier New',Courier,monospace;font-size:16px;font-weight:500;color:#1a1820;padding:0 2rem;min-height:52px;display:flex;align-items:center;justify-content:space-between;cursor:pointer;letter-spacing:0.5px;transition:color .15s}
.mm-tools-toggle:hover{color:#5533E8}
.mm-tools-toggle .mm-tools-arrow{font-size:10px;transition:transform .2s}
.mm-tools-toggle[aria-expanded="true"] .mm-tools-arrow{transform:rotate(90deg)}
.mm-tools-sub{display:none;background:#F6F4EE}
.mm-tools-sub.open{display:block}
.mm-tools-sub a{font-family:'Courier New',Courier,monospace;font-size:14px;font-weight:500;color:#1a1820;text-decoration:none;padding:0 2.5rem;min-height:44px;display:flex;align-items:center;border-bottom:1px solid #D4D0C4;transition:color .15s}
.mm-tools-sub a:last-child{border-bottom:none}
.mm-tools-sub a:hover{color:#5533E8}
</style>"""

DROPDOWN_HTML = '<div class="ndrop hide-m" id="toolsDrop"><button class="ndrop-btn" aria-haspopup="true" aria-expanded="false" id="toolsBtn">Tools<svg width="10" height="10" viewBox="0 0 10 10" fill="none" style="margin-left:2px"><path d="M2 3.5L5 6.5L8 3.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></button><div class="ndrop-menu" id="toolsMenu" role="menu"><a href="/spot-the-typo.html" role="menuitem">Spot the Typo</a><a href="/literary-style-quiz.html" role="menuitem">Who Do You Write Like</a><a href="/flash-fiction-prompts.html" role="menuitem">Prompts Generator</a><a href="/podcasts.html" role="menuitem">Best Literary Podcasts</a></div></div>'

DROPDOWN_JS = """<script id="tools-dropdown-js">(function(){var d=document.getElementById('toolsDrop'),b=document.getElementById('toolsBtn');if(!d||!b)return;b.addEventListener('click',function(e){e.stopPropagation();var open=d.classList.toggle('open');b.setAttribute('aria-expanded',open);});document.addEventListener('click',function(e){if(!e.target.closest('#toolsDrop')){d.classList.remove('open');b.setAttribute('aria-expanded','false');}});d.addEventListener('keydown',function(e){if(e.key==='Escape'){d.classList.remove('open');b.setAttribute('aria-expanded','false');}});}());</script>"""

MOBILE_TOOLS_HTML = '<div class="mm-tools-group"><button class="mm-tools-toggle" aria-expanded="false" id="mmToolsBtn">Tools<span class="mm-tools-arrow">&#9658;</span></button><div class="mm-tools-sub" id="mmToolsSub"><a href="/spot-the-typo.html">Spot the Typo</a><a href="/literary-style-quiz.html">Who Do You Write Like</a><a href="/flash-fiction-prompts.html">Prompts Generator</a><a href="/podcasts.html">Best Literary Podcasts</a></div></div>'

MOBILE_TOOLS_JS = """<script id="mm-tools-js">(function(){var b=document.getElementById('mmToolsBtn'),s=document.getElementById('mmToolsSub');if(!b||!s)return;b.addEventListener('click',function(){var open=s.classList.toggle('open');b.setAttribute('aria-expanded',open);});}());</script>"""

# Desktop nav Tools link - two variants exist
DESKTOP_TOOLS_PATTERNS = [
    '<a href="/essays-and-culture.html#tools" class="nlink hide-m">Tools</a>',
    '<a href="essays-and-culture.html#tools" class="nlink hide-m">Tools</a>',
]

# Mobile nav Tools link
MOBILE_TOOLS_PATTERNS = [
    '<a href="/essays-and-culture.html#tools">Tools</a>',
    '<a href="essays-and-culture.html#tools">Tools</a>',
]

# Footer Podcasts link to remove
FOOTER_PODCASTS = '<a href="/podcasts.html">Podcasts</a>'

# Final-links Tools link (appears at bottom of some pages)
FINAL_TOOLS_PATTERNS = [
    '<a href="/essays-and-culture.html#tools">Tools</a>',
    '<a href="essays-and-culture.html#tools">Tools</a>',
]

html_files = glob.glob(os.path.join(SITE_DIR, "*.html"))
pages_updated = 0
desktop_updated = 0
mobile_updated = 0
footer_updated = 0

for fpath in html_files:
    fname = os.path.basename(fpath)
    if fname in ("hero-banner.html", "newsletter-popup.html", "REPLACE-photo-reel.html",
                 "tagline-snippet.html", "discover.html"):
        continue

    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    changed = False

    # 1. Add CSS to head (only if not already present)
    if 'id="tools-dropdown-css"' not in content:
        # Insert before </head>
        content = content.replace("</head>", DROPDOWN_CSS + "\n</head>", 1)
        changed = True

    # 2. Replace desktop nav Tools link with dropdown
    for pattern in DESKTOP_TOOLS_PATTERNS:
        if pattern in content:
            content = content.replace(pattern, DROPDOWN_HTML, 1)
            desktop_updated += 1
            changed = True
            break

    # 3. Replace mobile nav Tools link with collapsible group
    for pattern in MOBILE_TOOLS_PATTERNS:
        if pattern in content:
            content = content.replace(pattern, MOBILE_TOOLS_HTML, 1)
            mobile_updated += 1
            changed = True
            break

    # 4. Remove Podcasts from footer nav (only the footer nav link, not body links)
    # The footer nav link is specifically: <a href="/podcasts.html">Podcasts</a>
    # But we need to be careful not to remove body links to podcasts.html
    # The footer nav pattern: it appears right after Fiction & Poetry in the ft-l nav
    # Pattern: the footer contains: >Fiction &amp; Poetry</a><a href="/podcasts.html">Podcasts</a>
    footer_pattern = '<a href="/podcasts.html">Podcasts</a>'
    # Only remove if it's in the footer context (after <footer class="ft">)
    footer_split = content.split('<footer class="ft">')
    if len(footer_split) > 1:
        footer_part = footer_split[1]
        if footer_pattern in footer_part:
            footer_part = footer_part.replace(footer_pattern, "", 1)
            content = footer_split[0] + '<footer class="ft">' + footer_part
            footer_updated += 1
            changed = True

    # 5. Update final-links section (bottom of pages with final-links div)
    # These also use /essays-and-culture.html#tools
    for pattern in FINAL_TOOLS_PATTERNS:
        if pattern in content:
            # Replace with a direct link to essays-and-culture.html#tools in final-links
            # (not a dropdown since it's a simpler nav at page bottom)
            content = content.replace(
                pattern,
                '<a href="/essays-and-culture.html#tools">Tools</a>',
                1  # only first occurrence (should be same as pattern for /essays variant)
            )
            # Actually for final-links, we can just leave it as a plain link to the tools section
            # since it's not the nav. Let's keep /essays-and-culture.html#tools but without the #tools
            # Wait - the task says the Tools link goes to /essays-and-culture.html#tools in nav
            # but the final-links should link to the tools section still. Let's leave it as is.
            break

    # 6. Add JS for dropdown and mobile (only if not already present)
    if 'id="tools-dropdown-js"' not in content and 'id="toolsDrop"' in content:
        # Insert JS before </body>
        content = content.replace("</body>", DROPDOWN_JS + "\n" + MOBILE_TOOLS_JS + "\n</body>", 1)
        changed = True

    if changed and content != original:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        pages_updated += 1

print(f"Pages updated: {pages_updated}")
print(f"Desktop nav dropdown added: {desktop_updated}")
print(f"Mobile nav collapsible added: {mobile_updated}")
print(f"Footer Podcasts link removed: {footer_updated}")
