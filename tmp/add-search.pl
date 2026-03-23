#!/usr/bin/perl
use strict;
use warnings;

my %skip = map { $_ => 1 } qw(
    REPLACE-photo-reel.html
    hero-banner.html
    newsletter-popup.html
    tagline-snippet.html
    search.html
);

my $dir = 'C:/Users/tumbl/projects/tumbleewords';

my $css = q{<style id="nsearch-css">.nsearch{position:relative;display:flex;align-items:center;flex-shrink:0;margin-right:.5rem}.nsearch-btn{background:none;border:none;cursor:pointer;color:#1a1820;padding:.38rem;display:flex;align-items:center;border-radius:3px;transition:color .15s}.nsearch-btn:hover,.nsearch-btn.active{color:#5533E8}.nsearch-wrap{display:none;position:absolute;right:0;top:calc(100% + 8px);background:#fff;border:1.5px solid #5533E8;border-radius:3px;overflow:hidden;width:230px;z-index:500;box-shadow:0 4px 16px rgba(85,51,232,.15)}.nsearch-wrap.open{display:flex}.nsearch-input{flex:1;border:none;padding:.5rem .85rem;font-family:"Source Serif 4",Georgia,serif;font-size:.8rem;color:#1a1820;outline:none;background:transparent;min-width:0}.nsearch-go{background:#5533E8;border:none;cursor:pointer;padding:.5rem .7rem;color:#fff;display:flex;align-items:center;transition:background .15s;flex-shrink:0}.nsearch-go:hover{background:#6644F5}@media(max-width:600px){.nsearch-wrap.open{width:180px;right:-1rem}}</style>};

my $widget = q{<div id="navSearch" class="nsearch"><button id="searchToggle" class="nsearch-btn" aria-label="Search" type="button"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg></button><div id="nsearchWrap" class="nsearch-wrap"><input type="search" id="nsearchInput" class="nsearch-input" placeholder="Search&#8230;" autocomplete="off"><button type="button" id="nsearchGo" class="nsearch-go"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg></button></div></div>};

my $js = q{<script>(function(){var t=document.getElementById('searchToggle');var w=document.getElementById('nsearchWrap');var i=document.getElementById('nsearchInput');var g=document.getElementById('nsearchGo');if(!t)return;function ds(){var q=i.value.trim();if(q)window.location.href='/search.html?q='+encodeURIComponent(q);}t.addEventListener('click',function(e){e.stopPropagation();w.classList.toggle('open');t.classList.toggle('active');if(w.classList.contains('open'))i.focus();});g.addEventListener('click',ds);i.addEventListener('keydown',function(e){if(e.key==='Enter')ds();});document.addEventListener('click',function(e){if(!e.target.closest('#navSearch')){w.classList.remove('open');t.classList.remove('active');}});document.addEventListener('keydown',function(e){if(e.key==='Escape'){w.classList.remove('open');t.classList.remove('active');}});})();</script>};

opendir(my $dh, $dir) or die "Cannot open $dir: $!";
my @files = sort grep { /\.html$/ && !$skip{$_} } readdir($dh);
closedir($dh);

my ($updated, $skipped, $no_match) = (0, 0, 0);

for my $file (@files) {
    my $path = "$dir/$file";
    open(my $fh, '<:raw', $path) or do { warn "Cannot read $file: $!"; next; };
    my $content = do { local $/; <$fh> };
    close($fh);

    if ($content =~ /id="navSearch"/) {
        $skipped++;
        next;
    }

    my $modified = $content;

    # 1. Inject CSS before </head>
    $modified =~ s{</head>}{${css}</head>};

    # 2. Inject search widget before the ncta link
    $modified =~ s{(<a [^>]*class="ncta")}{${widget}$1};

    # 3. Inject JS before </body>
    $modified =~ s{</body>}{${js}</body>};

    if ($modified ne $content) {
        open(my $out, '>:raw', $path) or do { warn "Cannot write $file: $!"; next; };
        print $out $modified;
        close($out);
        $updated++;
        print "OK  $file\n";
    } else {
        $no_match++;
        print "--- $file (no nav match)\n";
    }
}

print "\nDone. Updated: $updated  Already done: $skipped  No match: $no_match\n";
