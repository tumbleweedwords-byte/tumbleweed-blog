#!/usr/bin/perl
use strict;
use warnings;

my $dir = 'C:/Users/tumbl/projects/tumbleewords';

my %skip = map { $_ => 1 } qw(
    REPLACE-photo-reel.html hero-banner.html newsletter-popup.html
    tagline-snippet.html subscribe.html search.html
);

my $craft_cta = q{<section style="background:var(--bg2,#EDEBE3);border-top:2px solid var(--p,#5533E8);padding:4rem 2rem;text-align:center"><div style="max-width:560px;margin:0 auto"><h2 style="font-family:var(--fd,'Fraunces',Georgia,serif);font-size:clamp(1.2rem,2.5vw,1.65rem);font-weight:700;color:var(--ink,#1a1820);letter-spacing:-.02em;margin-bottom:.7rem;line-height:1.2">One piece a week, written from everywhere<br><em style="color:var(--p,#5533E8);font-style:normal">Sent to your inbox</em></h2><p style="font-family:var(--fb,'Source Serif 4',Georgia,serif);font-size:.82rem;color:var(--mu,#6B6880);line-height:1.75;margin-bottom:1.4rem;font-weight:300">Internationally published literary fiction and poetry, delivered in bitesize portions to your inbox. Free, every week.</p><form action="https://tumbleweedwords.substack.com/api/v1/free" method="post" target="_blank" style="display:flex;gap:.5rem;max-width:420px;margin:0 auto"><input type="email" name="email" placeholder="Your email address" required autocomplete="email" style="flex:1;background:#fff;border:1.5px solid var(--br,#D4D0C4);color:var(--ink,#1a1820);font-family:var(--fb,'Source Serif 4',Georgia,serif);font-size:.78rem;padding:.7rem 1rem;outline:none;transition:border-color .2s"><button type="submit" style="background:var(--p,#5533E8);color:#fff;font-family:var(--fm,ui-monospace,monospace);font-size:.54rem;letter-spacing:.1em;text-transform:uppercase;padding:.7rem 1.2rem;border:none;cursor:pointer;white-space:nowrap;transition:background .15s">Subscribe free &rarr;</button></form><p style="font-family:var(--fm,ui-monospace,monospace);font-size:.46rem;letter-spacing:.1em;text-transform:uppercase;color:var(--fa,#9896a8);margin-top:.7rem">Free &middot; Weekly &middot; No spam &middot; Unsubscribe any time</p></div></section>};

opendir(my $dh, $dir) or die;
my @html = sort grep { /\.html$/ && !$skip{$_} } readdir($dh);
closedir($dh);

my $added = 0;

for my $file (@html) {
    my $path = "$dir/$file";
    open(my $fh, '<:raw', $path) or next;
    my $content = do { local $/; <$fh> };
    close($fh);

    # Only target: has </main>, no cta-sec, no existing inline subscribe CTA in content before bar was added
    # Use original content check: had no inline-sub and had no api/v1/free in CTA sections
    next unless $content =~ m{</main>};
    next if $content =~ /class="cta-sec"/;
    next if $content =~ /class="inline-sub"/;
    # Skip if craft CTA already injected
    next if $content =~ /One piece a week, written from everywhere/;

    my $modified = $content;
    my $eol = ($modified =~ /\r\n/) ? "\r\n" : "\n";
    $modified =~ s{(</main>[\r\n]+)(<footer\b)}{${1}${craft_cta}${eol}${2}};

    if ($modified ne $content) {
        open(my $out, '>:raw', $path) or next;
        print $out $modified;
        close($out);
        $added++;
        print "OK  $file\n";
    }
}

print "\nDone. Added craft CTA to $added pages.\n";
