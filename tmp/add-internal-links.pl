#!/usr/bin/perl
use strict;
use warnings;

my $dir = 'C:/Users/tumbl/projects/tumbleewords';

# -------------------------------------------------------
# PART 1: Add fiction link to craft/book/resource pages
# -------------------------------------------------------

# City and theme landing pages — skip (they ARE fiction collections)
my %skip_craft = map { $_ => 1 } qw(
    flash-fiction-barcelona.html flash-fiction-belgrade.html
    flash-fiction-berlin.html flash-fiction-buenos-aires.html
    flash-fiction-edinburgh.html flash-fiction-havana.html
    flash-fiction-istanbul.html flash-fiction-lisbon.html
    flash-fiction-marseille.html flash-fiction-naples.html
    flash-fiction-oaxaca.html flash-fiction-porto.html
    flash-fiction-prague.html flash-fiction-reykjavik.html
    flash-fiction-sarajevo.html flash-fiction-tangier.html
    flash-fiction-tbilisi.html flash-fiction-thessaloniki.html
    flash-fiction-vienna.html flash-fiction-warsaw.html
    flash-fiction-about-borders.html flash-fiction-about-departure.html
    flash-fiction-about-exile.html flash-fiction-about-fog.html
    flash-fiction-about-grief.html flash-fiction-about-hotels.html
    flash-fiction-about-insomnia.html flash-fiction-about-language-barriers.html
    flash-fiction-about-last-things.html flash-fiction-about-letters.html
    flash-fiction-about-memory.html flash-fiction-about-return.html
    flash-fiction-about-solitude.html flash-fiction-about-strangers.html
    flash-fiction-about-trains.html
    index.html about.html subscribe.html search.html
    all-writing.html craft-theory.html reads.html discover.html
    street-legal.html an-expat-in-paris.html honest-pursuit.html
    post-flash-fiction.html post-minimalist-fiction.html
    post-writing-nomadic.html post-literary-magazines.html
);

my $fiction_li = '<li><a href="/street-legal.html">Read the fiction &mdash; <em>Street Legal</em>, a story from Berlin</a></li>';

# -------------------------------------------------------
# PART 2: Craft links per fiction/essay page
# -------------------------------------------------------

my %fiction_craft_links = (
    'street-legal.html' => [
        ['/what-is-dirty-realism.html',         'What is dirty realism?'],
        ['/influenced-by-raymond-carver.html',  'Writing influenced by Raymond Carver'],
        ['/what-is-the-iceberg-theory.html',    'What is the iceberg theory?'],
    ],
    'an-expat-in-paris.html' => [
        ['/influenced-by-virginia-woolf.html',          'Writing influenced by Virginia Woolf'],
        ['/show-dont-tell-what-it-actually-means.html', 'Show don\'t tell — what it actually means'],
        ['/what-is-flash-fiction.html',                 'What is flash fiction?'],
    ],
    'honest-pursuit.html' => [
        ['/nomadic-writing-what-is-it.html',               'What is nomadic writing?'],
        ['/what-is-flash-fiction.html',                    'What is flash fiction?'],
        ['/can-you-make-money-writing-flash-fiction.html', 'Can you make money writing flash fiction?'],
    ],
    'post-flash-fiction.html' => [
        ['/what-is-flash-fiction.html',            'What is flash fiction?'],
        ['/how-to-end-a-flash-fiction-story.html', 'How to end a flash fiction story'],
        ['/flash-fiction-vs-short-story.html',     'Flash fiction vs the short story'],
    ],
    'post-minimalist-fiction.html' => [
        ['/why-minimalist-fiction-is-harder.html', 'Why minimalist fiction is harder than it looks'],
        ['/what-is-dirty-realism.html',            'What is dirty realism?'],
        ['/influenced-by-raymond-carver.html',     'Writing influenced by Raymond Carver'],
    ],
    'post-writing-nomadic.html' => [
        ['/nomadic-writing-what-is-it.html',   'What is nomadic writing?'],
        ['/what-is-flash-fiction.html',        'What is flash fiction?'],
        ['/flash-fiction-vs-short-story.html', 'Flash fiction vs the short story'],
    ],
    'post-literary-magazines.html' => [
        ['/literary-magazine-finder.html',                 'Literary magazine finder'],
        ['/can-you-make-money-writing-flash-fiction.html', 'Can you make money writing flash fiction?'],
        ['/what-is-flash-fiction.html',                    'What is flash fiction?'],
    ],
);

my $related_css = '<style id="related-css">.related{background:var(--bg2,#EDEBE3);border:1px solid var(--br,#D4D0C4);padding:1.5rem 1.8rem;margin:2.5rem 0;border-radius:6px}.related .lbl{font-family:var(--fm,ui-monospace,monospace);font-size:.56rem;letter-spacing:.16em;text-transform:uppercase;color:var(--p,#5533E8);margin-bottom:.9rem;display:block}.related ul{list-style:none;margin:0;padding:0}.related li{border-bottom:1px solid var(--br,#D4D0C4);padding:.5rem 0;display:flex;gap:.5rem;align-items:baseline}.related li:last-child{border-bottom:none;padding-bottom:0}.related li::before{content:"\2192";color:var(--p,#5533E8);font-size:.8rem;flex-shrink:0}.related a{color:var(--txt2,#6B6880);font-size:.9rem;text-decoration:none}.related a:hover{color:var(--p,#5533E8)}</style>';

# -------------------------------------------------------
# Process all HTML files
# -------------------------------------------------------

opendir(my $dh, $dir) or die "Can't open $dir: $!";
my @html = sort grep { /\.html$/ } readdir($dh);
closedir($dh);

my ($craft_updated, $fiction_updated) = (0, 0);

for my $file (@html) {
    my $path = "$dir/$file";
    open(my $fh, '<:raw', $path) or next;
    my $content = do { local $/; <$fh> };
    close($fh);

    my $modified = $content;

    # --- PART 1: Craft/resource/book pages → add fiction link ---
    if (!$skip_craft{$file} && $content =~ /class="related"/ && $content !~ /street-legal\.html/) {
        # Append fiction link before the closing </ul> inside .related
        $modified =~ s{(<div class="related">.*?</ul>)(\s*</div>)}{$1\n$fiction_li$2}s;
    }

    # --- PART 2: Fiction story pages → add craft related section ---
    if (exists $fiction_craft_links{$file} && $content !~ /id="related-css"/) {
        my $links = $fiction_craft_links{$file};
        my $lis = join("\n", map { "<li><a href=\"$_->[0]\">$_->[1]</a></li>" } @$links);
        my $block = "$related_css\n<div class=\"related\">\n  <span class=\"lbl\">On the craft</span>\n  <ul>\n$lis\n  </ul>\n</div>\n";

        # Try cta-sec first, then cband
        if ($modified =~ /<section class="cta-sec"/) {
            $modified =~ s{(<section class="cta-sec")}{$block$1};
        } elsif ($modified =~ /<section class="cband"/) {
            $modified =~ s{(<section class="cband")}{$block$1};
        }
    }

    if ($modified ne $content) {
        open(my $out, '>:raw', $path) or next;
        print $out $modified;
        close($out);

        if (exists $fiction_craft_links{$file}) {
            $fiction_updated++;
            print "FICTION  $file\n";
        } else {
            $craft_updated++;
            print "CRAFT    $file\n";
        }
    }
}

print "\nDone. Craft pages with fiction link: $craft_updated  Fiction pages with craft links: $fiction_updated\n";
