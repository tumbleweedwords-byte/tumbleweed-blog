#!/usr/bin/perl
use strict;
use warnings;

my $dir = 'C:/Users/tumbl/projects/tumbleewords';

opendir(my $dh, $dir) or die "Cannot open $dir: $!";
my @html = sort grep { /\.html$/ } readdir($dh);
closedir($dh);

my $count = 0;

for my $file (@html) {
    my $path = "$dir/$file";
    open(my $fh, '<:raw', $path) or do { warn "Cannot read $file"; next; };
    my $content = do { local $/; <$fh> };
    close($fh);

    my $modified = $content;

    # 1. Whiten the search toggle button (all pages incl search.html)
    my $old_btn = '.nsearch-btn{background:none;border:none;';
    my $new_btn = '.nsearch-btn{background:#fff;border:1px solid #D4D0C4;';
    $modified =~ s/\Q$old_btn\E/$new_btn/g;

    # 2. Box the purple section labels (all pages)
    # Only update if the basic .sec-label override exists and doesn't already have the box
    my $old_label = '.sec-label{font-size:.75rem!important}';
    my $new_label = '.sec-label{font-size:.75rem!important;display:inline-block!important;border:1.5px solid #5533E8!important;padding:.26rem .9rem!important;padding-bottom:.26rem!important;margin-bottom:2.4rem!important}.sec-eye{border:1.5px solid #5533E8!important;padding:.26rem .85rem!important;display:inline-flex!important;gap:.6rem!important}';
    $modified =~ s/\Q$old_label\E/$new_label/g;

    # 3. Move paid-sec higher in index.html (from after scarcity to after what-sec)
    if ($file eq 'index.html') {
        if ($modified =~ /(<section class="paid-sec">.*?<\/section>)/s) {
            my $paid = $1;
            # Remove paid-sec (and the blank line before it)
            $modified =~ s/[\r\n]+<section class="paid-sec">.*?<\/section>//s;
            # Detect line ending style
            my $eol = ($modified =~ /\r\n/) ? "\r\n" : "\n";
            # Insert after what-sec section
            $modified =~ s{(<section class="what-sec">.*?<\/section>)}{$1$eol$eol$paid}s;
            print "  -> Moved paid-sec up in index.html\n";
        }
    }

    if ($modified ne $content) {
        open(my $out, '>:raw', $path) or do { warn "Cannot write $file"; next; };
        print $out $modified;
        close($out);
        $count++;
        print "OK  $file\n";
    }
}

print "\nDone. $count files updated.\n";
