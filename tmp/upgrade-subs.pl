#!/usr/bin/perl
use strict;
use warnings;

my $dir = 'C:/Users/tumbl/projects/tumbleewords';

# Pages to skip entirely
my %skip = map { $_ => 1 } qw(
    REPLACE-photo-reel.html
    hero-banner.html
    newsletter-popup.html
    tagline-snippet.html
    subscribe.html
    search.html
);

# The direct-form CTA section injected at end of craft articles
my $craft_cta = q{<section style="background:var(--bg2,#EDEBE3);border-top:2px solid var(--p,#5533E8);padding:4rem 2rem;text-align:center"><div style="max-width:560px;margin:0 auto"><h2 style="font-family:var(--fd,'Fraunces',Georgia,serif);font-size:clamp(1.2rem,2.5vw,1.65rem);font-weight:700;color:var(--ink,#1a1820);letter-spacing:-.02em;margin-bottom:.7rem;line-height:1.2">One piece a week, written from everywhere<br><em style="color:var(--p,#5533E8);font-style:normal">Sent to your inbox</em></h2><p style="font-family:var(--fb,'Source Serif 4',Georgia,serif);font-size:.82rem;color:var(--mu,#6B6880);line-height:1.75;margin-bottom:1.4rem;font-weight:300">Internationally published literary fiction and poetry, delivered in bitesize portions to your inbox. Free, every week.</p><form action="https://tumbleweedwords.substack.com/api/v1/free" method="post" target="_blank" style="display:flex;gap:.5rem;max-width:420px;margin:0 auto"><input type="email" name="email" placeholder="Your email address" required autocomplete="email" style="flex:1;background:#fff;border:1.5px solid var(--br,#D4D0C4);color:var(--ink,#1a1820);font-family:var(--fb,'Source Serif 4',Georgia,serif);font-size:.78rem;padding:.7rem 1rem;outline:none;transition:border-color .2s"><button type="submit" style="background:var(--p,#5533E8);color:#fff;font-family:var(--fm,ui-monospace,monospace);font-size:.54rem;letter-spacing:.1em;text-transform:uppercase;padding:.7rem 1.2rem;border:none;cursor:pointer;white-space:nowrap;transition:background .15s">Subscribe free &rarr;</button></form><p style="font-family:var(--fm,ui-monospace,monospace);font-size:.46rem;letter-spacing:.1em;text-transform:uppercase;color:var(--fa,#9896a8);margin-top:.7rem">Free &middot; Weekly &middot; No spam &middot; Unsubscribe any time</p></div></section>};

# Floating bar CSS+HTML+JS — injected before </body>
my $sub_bar = q{<style id="sub-bar-css">.sub-bar{position:fixed;bottom:0;left:0;right:0;z-index:990;background:var(--bg,#F6F4EE);border-top:2px solid var(--p,#5533E8);padding:.85rem 2rem;box-shadow:0 -4px 20px rgba(85,51,232,.12);transform:translateY(110%);transition:transform .4s ease}.sub-bar.visible{transform:translateY(0)}.sub-bar-inner{max-width:860px;margin:0 auto;display:flex;align-items:center;gap:1.2rem;flex-wrap:nowrap}.sub-bar-text{font-family:var(--fb,"Source Serif 4",Georgia,serif);font-size:.82rem;color:var(--ink,#1a1820);font-style:italic;flex-shrink:0;white-space:nowrap}.sub-bar-form{display:flex;gap:.4rem;flex:1;min-width:0}.sub-bar-input{flex:1;border:1.5px solid var(--br,#D4D0C4);background:#fff;padding:.48rem .9rem;font-family:var(--fb,"Source Serif 4",Georgia,serif);font-size:.78rem;color:var(--ink,#1a1820);outline:none;min-width:0;transition:border-color .2s}.sub-bar-input:focus{border-color:var(--p,#5533E8)}.sub-bar-btn{background:var(--p,#5533E8);color:#fff;border:none;cursor:pointer;padding:.48rem 1.1rem;font-family:var(--fm,ui-monospace,"SF Mono",monospace);font-size:.5rem;letter-spacing:.1em;text-transform:uppercase;white-space:nowrap;transition:background .15s;flex-shrink:0}.sub-bar-btn:hover{background:var(--p2,#6644F5)}.sub-bar-close{background:none;border:none;cursor:pointer;color:var(--fa,#9896a8);font-size:1.3rem;padding:.2rem .4rem;line-height:1;flex-shrink:0;transition:color .15s;margin-left:auto}.sub-bar-close:hover{color:var(--ink,#1a1820)}@media(max-width:600px){.sub-bar-text{display:none}}</style><div id="subBar" class="sub-bar" role="complementary" aria-label="Subscribe to newsletter"><div class="sub-bar-inner"><span class="sub-bar-text">One piece a week. Free.</span><form class="sub-bar-form" action="https://tumbleweedwords.substack.com/api/v1/free" method="post" target="_blank"><input type="email" name="email" placeholder="Your email address" required autocomplete="email" class="sub-bar-input"><button type="submit" class="sub-bar-btn">Subscribe free &rarr;</button></form><button class="sub-bar-close" id="subBarClose" aria-label="Close subscribe bar" type="button">&times;</button></div></div><script>(function(){var KEY='tw_bar_v1',DAYS=30;try{var stored=localStorage.getItem(KEY);if(stored&&Date.now()-parseInt(stored)<DAYS*86400000)return;}catch(e){return;}var bar=document.getElementById('subBar');var closeBtn=document.getElementById('subBarClose');if(!bar||!closeBtn)return;function dismiss(){bar.classList.remove('visible');try{localStorage.setItem(KEY,Date.now().toString());}catch(e){}}closeBtn.addEventListener('click',dismiss);bar.querySelector('form').addEventListener('submit',function(){setTimeout(dismiss,500);});var shown=false;window.addEventListener('scroll',function(){if(!shown&&window.scrollY>500){shown=true;bar.classList.add('visible');}},{passive:true});})();</script>};

opendir(my $dh, $dir) or die;
my @html = sort grep { /\.html$/ && !$skip{$_} } readdir($dh);
closedir($dh);

my ($conv_sub, $added_bar, $added_cta) = (0, 0, 0);

for my $file (@html) {
    my $path = "$dir/$file";
    open(my $fh, '<:raw', $path) or next;
    my $content = do { local $/; <$fh> };
    close($fh);

    my $modified = $content;

    # 1. Convert <div class="inline-sub"> to direct Substack form
    if ($modified =~ /class="inline-sub"/) {
        $modified =~ s{<div class="inline-sub">.*?</div>}{<form class="inline-sub" action="https://tumbleweedwords.substack.com/api/v1/free" method="post" target="_blank"><input class="inline-sub__input" type="email" name="email" placeholder="Your email address" required autocomplete="email"><button class="inline-sub__btn" type="submit">Subscribe free &rarr;</button></form>}gs;
    }

    # 2. Update popup JS: replace old window.open submit with direct form submit
    my $old_popup_js = q{submit.addEventListener('click',function(){var v=email.value.trim(),u='https://tumbleweedwords.substack.com/subscribe';window.open(v?u+'?email='+encodeURIComponent(v):u,'_blank');hide()});};
    my $new_popup_js = q{submit.addEventListener('click',function(){var v=email.value.trim();if(!v){email.focus();return;}var f=document.createElement('form');f.action='https://tumbleweedwords.substack.com/api/v1/free';f.method='post';f.target='_blank';var inp=document.createElement('input');inp.type='hidden';inp.name='email';inp.value=v;f.appendChild(inp);document.body.appendChild(f);f.submit();document.body.removeChild(f);hide();});};
    if ($modified =~ /\Q$old_popup_js\E/) {
        $modified =~ s/\Q$old_popup_js\E/$new_popup_js/;
    }

    # 3. Add floating subscribe bar before </body> (if not already there)
    if ($modified !~ /id="subBar"/ && $modified =~ m{</body>}) {
        $modified =~ s{</body>}{${sub_bar}</body>};
        $added_bar++;
    }

    # 4. Add end-of-article CTA on craft/article pages:
    #    - Has </main> (article layout)
    #    - Does NOT already have inline-sub or craft_cta
    if ($modified =~ m{</main>} && $modified !~ /api\/v1\/free/ && $modified !~ /class="cta-sec"/) {
        my $eol = ($modified =~ /\r\n/) ? "\r\n" : "\n";
        $modified =~ s{(</main>[\r\n]+)(<footer class="ft">)}{${1}${craft_cta}${eol}${2}};
        $added_cta++;
    }

    if ($modified ne $content) {
        open(my $out, '>:raw', $path) or next;
        print $out $modified;
        close($out);
        print "OK  $file\n";
        $conv_sub++ if $content =~ /class="inline-sub"/;
    }
}

print "\nDone. Floating bar: +$added_bar pages  Craft CTA: +$added_cta pages  Inline-sub converted on: $conv_sub pages\n";
