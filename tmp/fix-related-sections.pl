#!/usr/bin/perl
use strict;
use warnings;

my $dir = 'C:/Users/tumbl/projects/tumbleewords';

# Per-page work links: 2 fiction/poetry items, varied by theme
# Each entry: [url, link text (HTML ok)]
my %work_links = (
    # Dirty realism / Carver / minimalism
    'what-is-dirty-realism.html' => [
        ['/street-legal.html',                                                       'Read — <em>Street Legal</em>, flash fiction from Berlin'],
        ['https://tumbleweedwords.substack.com/p/you-wanting-anything-from-the-shops','Read — <em>You wanting anything from the shops?</em>, a poem'],
    ],
    'influenced-by-raymond-carver.html' => [
        ['/street-legal.html',                                                       'Read — <em>Street Legal</em>, flash fiction from Berlin'],
        ['https://tumbleweedwords.substack.com/p/you-wanting-anything-from-the-shops','Read — <em>You wanting anything from the shops?</em>, a poem'],
    ],
    'why-minimalist-fiction-is-harder.html' => [
        ['/street-legal.html',                                                'Read — <em>Street Legal</em>, flash fiction from Berlin'],
        ['https://tumbleweedwords.substack.com/p/indescretion-poem',         'Read — <em>Mature Indiscretions</em>, a poem'],
    ],
    'hemingway-vs-carver-difference.html' => [
        ['/street-legal.html',                                                       'Read — <em>Street Legal</em>, flash fiction from Berlin'],
        ['https://tumbleweedwords.substack.com/p/you-wanting-anything-from-the-shops','Read — <em>You wanting anything from the shops?</em>, a poem'],
    ],
    'best-books-if-you-like-carver.html' => [
        ['/street-legal.html',         'Read — <em>Street Legal</em>, flash fiction from Berlin'],
        ['/an-expat-in-paris.html',    'Read — <em>An Expat in Paris</em>'],
    ],

    # Poetry / prose poetry
    'prose-poetry-vs-flash-fiction.html' => [
        ['https://tumbleweedwords.substack.com/p/three-nomadic-poems', 'Read — <em>Red Eye</em>, a nomadic poem'],
        ['https://tumbleweedwords.substack.com/p/indescretion-poem',   'Read — <em>Mature Indiscretions</em>, a poem from Scotland'],
    ],
    'is-poetry-dying-2026.html' => [
        ['https://tumbleweedwords.substack.com/p/three-nomadic-poems',               'Read — <em>Red Eye</em>, a nomadic poem'],
        ['https://tumbleweedwords.substack.com/p/you-wanting-anything-from-the-shops','Read — <em>You wanting anything from the shops?</em>, a poem'],
    ],
    'influenced-by-virginia-woolf.html' => [
        ['/an-expat-in-paris.html',                                          'Read — <em>An Expat in Paris</em>'],
        ['https://tumbleweedwords.substack.com/p/indescretion-poem',         'Read — <em>Mature Indiscretions</em>, a poem from Scotland'],
    ],
    'influenced-by-w-g-sebald.html' => [
        ['/an-expat-in-paris.html',                                          'Read — <em>An Expat in Paris</em>'],
        ['https://tumbleweedwords.substack.com/p/three-nomadic-poems',       'Read — <em>Red Eye</em>, a nomadic poem'],
    ],

    # Nomadic / travel / expat
    'nomadic-writing-what-is-it.html' => [
        ['https://tumbleweedwords.substack.com/p/three-nomadic-poems', 'Read — <em>Red Eye</em>, a nomadic poem'],
        ['/an-expat-in-paris.html',                                    'Read — <em>An Expat in Paris</em>'],
    ],
    'influenced-by-samuel-beckett.html' => [
        ['/an-expat-in-paris.html',    'Read — <em>An Expat in Paris</em>'],
        ['/street-legal.html',         'Read — <em>Street Legal</em>, flash fiction from Berlin'],
    ],
    'influenced-by-franz-kafka.html' => [
        ['/an-expat-in-paris.html',                                          'Read — <em>An Expat in Paris</em>'],
        ['https://tumbleweedwords.substack.com/p/three-nomadic-poems',       'Read — <em>Red Eye</em>, a nomadic poem'],
    ],

    # General craft / flash fiction technique
    'what-is-flash-fiction.html' => [
        ['/street-legal.html',      'Read — <em>Street Legal</em>, flash fiction from Berlin'],
        ['/an-expat-in-paris.html', 'Read — <em>An Expat in Paris</em>'],
    ],
    'how-long-should-flash-fiction-be.html' => [
        ['/street-legal.html',                                               'Read — <em>Street Legal</em>, flash fiction from Berlin'],
        ['https://tumbleweedwords.substack.com/p/three-nomadic-poems',       'Read — <em>Red Eye</em>, a nomadic poem'],
    ],
    'flash-fiction-vs-short-story.html' => [
        ['/street-legal.html',      'Read — <em>Street Legal</em>, flash fiction from Berlin'],
        ['/an-expat-in-paris.html', 'Read — <em>An Expat in Paris</em>'],
    ],
    'how-to-end-a-flash-fiction-story.html' => [
        ['/street-legal.html',                                       'Read — <em>Street Legal</em>, flash fiction from Berlin'],
        ['https://tumbleweedwords.substack.com/p/indescretion-poem', 'Read — <em>Mature Indiscretions</em>, a poem'],
    ],
    'what-is-sudden-fiction.html' => [
        ['/street-legal.html',      'Read — <em>Street Legal</em>, flash fiction from Berlin'],
        ['/an-expat-in-paris.html', 'Read — <em>An Expat in Paris</em>'],
    ],
    'show-dont-tell-what-it-actually-means.html' => [
        ['/street-legal.html',      'Read — <em>Street Legal</em>, flash fiction from Berlin'],
        ['/an-expat-in-paris.html', 'Read — <em>An Expat in Paris</em>'],
    ],

    # Influences / authors
    'influenced-by-amy-hempel.html' => [
        ['/street-legal.html',                                               'Read — <em>Street Legal</em>, flash fiction from Berlin'],
        ['https://tumbleweedwords.substack.com/p/three-nomadic-poems',       'Read — <em>Red Eye</em>, a nomadic poem'],
    ],
    'influenced-by-ernest-hemingway.html' => [
        ['/street-legal.html',                                       'Read — <em>Street Legal</em>, flash fiction from Berlin'],
        ['https://tumbleweedwords.substack.com/p/indescretion-poem', 'Read — <em>Mature Indiscretions</em>, a poem'],
    ],
    'influenced-by-anton-chekhov.html' => [
        ['/street-legal.html',      'Read — <em>Street Legal</em>, flash fiction from Berlin'],
        ['/an-expat-in-paris.html', 'Read — <em>An Expat in Paris</em>'],
    ],
    'influenced-by-grace-paley.html' => [
        ['https://tumbleweedwords.substack.com/p/you-wanting-anything-from-the-shops','Read — <em>You wanting anything from the shops?</em>, a poem'],
        ['/street-legal.html',                                                        'Read — <em>Street Legal</em>, flash fiction from Berlin'],
    ],
    'influenced-by-jorge-luis-borges.html' => [
        ['/street-legal.html',                                               'Read — <em>Street Legal</em>, flash fiction from Berlin'],
        ['https://tumbleweedwords.substack.com/p/three-nomadic-poems',       'Read — <em>Red Eye</em>, a nomadic poem'],
    ],

    # Books / resources / trends
    'best-flash-fiction-2025.html' => [
        ['/street-legal.html',      'Read — <em>Street Legal</em>, flash fiction from Berlin'],
        ['/an-expat-in-paris.html', 'Read — <em>An Expat in Paris</em>'],
    ],
    'best-flash-fiction-collections.html' => [
        ['/street-legal.html',                                               'Read — <em>Street Legal</em>, flash fiction from Berlin'],
        ['https://tumbleweedwords.substack.com/p/three-nomadic-poems',       'Read — <em>Red Eye</em>, a nomadic poem'],
    ],
    'george-saunders-vigil-review.html' => [
        ['/street-legal.html',      'Read — <em>Street Legal</em>, flash fiction from Berlin'],
        ['/an-expat-in-paris.html', 'Read — <em>An Expat in Paris</em>'],
    ],
    'what-george-saunders-teaches-writers.html' => [
        ['/street-legal.html',      'Read — <em>Street Legal</em>, flash fiction from Berlin'],
        ['/an-expat-in-paris.html', 'Read — <em>An Expat in Paris</em>'],
    ],
    'can-you-make-money-writing-flash-fiction.html' => [
        ['/street-legal.html',                                               'Read — <em>Street Legal</em>, flash fiction from Berlin'],
        ['https://tumbleweedwords.substack.com/p/three-nomadic-poems',       'Read — <em>Red Eye</em>, a nomadic poem'],
    ],
    'literary-fiction-2026-trends.html' => [
        ['/street-legal.html',                                       'Read — <em>Street Legal</em>, flash fiction from Berlin'],
        ['https://tumbleweedwords.substack.com/p/indescretion-poem', 'Read — <em>Mature Indiscretions</em>, a poem'],
    ],
    'pushcart-prize-what-is-it.html' => [
        ['/street-legal.html',                                       'Read — <em>Street Legal</em>, flash fiction from Berlin'],
        ['https://tumbleweedwords.substack.com/p/indescretion-poem', 'Read — <em>Mature Indiscretions</em> (Pushcart-nominated)'],
    ],
    'substack-vs-mailchimp-for-writers.html' => [
        ['/street-legal.html',                                               'Read — <em>Street Legal</em>, flash fiction from Berlin'],
        ['https://tumbleweedwords.substack.com/p/three-nomadic-poems',       'Read — <em>Red Eye</em>, a nomadic poem'],
    ],
    'what-makes-a-good-literary-newsletter.html' => [
        ['/street-legal.html',      'Read — <em>Street Legal</em>, flash fiction from Berlin'],
        ['/an-expat-in-paris.html', 'Read — <em>An Expat in Paris</em>'],
    ],
    'how-to-start-a-literary-newsletter.html' => [
        ['/street-legal.html',                                               'Read — <em>Street Legal</em>, flash fiction from Berlin'],
        ['https://tumbleweedwords.substack.com/p/three-nomadic-poems',       'Read — <em>Red Eye</em>, a nomadic poem'],
    ],
    'writing-prompts-for-flash-fiction.html' => [
        ['/street-legal.html',                                               'Read — <em>Street Legal</em>, flash fiction from Berlin'],
        ['https://tumbleweedwords.substack.com/p/three-nomadic-poems',       'Read — <em>Red Eye</em>, a nomadic poem'],
    ],
);

opendir(my $dh, $dir) or die "Can't open $dir: $!";
my @html = sort grep { /\.html$/ } readdir($dh);
closedir($dh);

my $updated = 0;

for my $file (@html) {
    next unless exists $work_links{$file};

    my $path = "$dir/$file";
    open(my $fh, '<:raw', $path) or next;
    my $content = do { local $/; <$fh> };
    close($fh);

    # Match the entire .related div (no nested divs inside it)
    next unless $content =~ m{<div class="related">(.*?)</div>}s;

    my $related_inner = $1;

    # Collect ALL <li> items (from <ul> and any stray ones after </ul>)
    my @all_lis = ($related_inner =~ m{(<li>.*?</li>)}gs);

    # Filter out street-legal (the broken injection from previous script)
    my @craft_lis = grep { !/street-legal/ } @all_lis;

    # Keep first 2 craft items
    my @keep = @craft_lis[0, 1];

    # Build work link <li> items
    my @work_lis;
    for my $w (@{$work_links{$file}}) {
        my ($href, $text) = @$w;
        my $target = ($href =~ /substack/) ? ' target="_blank" rel="noopener"' : '';
        push @work_lis, "<li><a href=\"$href\"$target>$text</a></li>";
    }

    # Extract the lbl span
    my $lbl = 'Keep reading';
    if ($related_inner =~ m{<span class="lbl">(.*?)</span>}s) {
        $lbl = $1;
    }

    # Build new related section
    my $new_ul = join("\n", @keep, @work_lis);
    my $new_related = "<div class=\"related\">\n    <span class=\"lbl\">$lbl</span>\n    <ul>$new_ul\n</ul>\n  </div>";

    my $modified = $content;
    $modified =~ s{<div class="related">.*?</div>}{$new_related}s;

    if ($modified ne $content) {
        open(my $out, '>:raw', $path) or next;
        print $out $modified;
        close($out);
        $updated++;
        print "OK  $file\n";
    }
}

print "\nDone. Fixed and updated $updated pages.\n";
