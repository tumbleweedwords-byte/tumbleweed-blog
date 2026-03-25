use strict;
use warnings;

my $banner = <<'BANNER';
<div id="tw-consent" style="position:fixed;bottom:0;left:0;right:0;z-index:9999;background:#F6F4EE;border-top:2px solid #5533E8;padding:1rem 2rem;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap;font-family:'Source Serif 4',Georgia,serif;font-size:.82rem;color:#1a1820;box-shadow:0 -4px 24px rgba(85,51,232,.08);display:none"></div>
<script>
(function(){
  var b=document.getElementById('tw-consent');
  if(!b)return;
  var consent=document.cookie.split(';').find(function(s){return s.trim().startsWith('tw_consent=');});
  if(!consent){
    b.innerHTML='<p style="margin:0;max-width:600px;line-height:1.6">We use cookies to understand how readers find us. <a href="/about.html" style="color:#5533E8">Learn more</a>.</p><div style="display:flex;gap:.7rem;flex-shrink:0"><button onclick="twConsent(\'decline\')" style="font-family:ui-monospace,\'SF Mono\',monospace;font-size:.52rem;letter-spacing:.1em;text-transform:uppercase;padding:.5rem 1.1rem;border:1.5px solid #D4D0C4;background:transparent;color:#6B6880;cursor:pointer;border-radius:3px">Decline</button><button onclick="twConsent(\'accept\')" style="font-family:ui-monospace,\'SF Mono\',monospace;font-size:.52rem;letter-spacing:.1em;text-transform:uppercase;padding:.5rem 1.1rem;border:1.5px solid #5533E8;background:#5533E8;color:#fff;cursor:pointer;border-radius:3px">Accept</button></div>';
    b.style.display='flex';
  }
})();
function twConsent(choice){
  var d=new Date();d.setFullYear(d.getFullYear()+1);
  document.cookie='tw_consent='+choice+';path=/;expires='+d.toUTCString()+';SameSite=Lax';
  document.getElementById('tw-consent').style.display='none';
  if(choice==='accept'&&typeof gtag==='function'){gtag('config','G-8B7DYTLXQC');}
}
</script>
</body>
BANNER

my $new_ga = "<!-- Google tag (gtag.js) -->\n<script async src=\"https://www.googletagmanager.com/gtag/js?id=G-8B7DYTLXQC\"></script>\n<script>\n  window.dataLayer = window.dataLayer || [];\n  function gtag(){dataLayer.push(arguments);}\n  gtag('js', new Date());\n  if(document.cookie.split(';').some(function(c){return c.trim().startsWith('tw_consent=accept');})){gtag('config','G-8B7DYTLXQC');}\n</script>\n";

my $old_ga = "<!-- Google tag (gtag.js) -->\n<script async src=\"https://www.googletagmanager.com/gtag/js?id=G-8B7DYTLXQC\"></script>\n<script>\n  window.dataLayer = window.dataLayer || [];\n  function gtag(){dataLayer.push(arguments);}\n  gtag('js', new Date());\n  gtag('config', 'G-8B7DYTLXQC');\n</script>\n";

my @files = glob("*.html");
my ($consent_count, $ga_count) = (0, 0);

for my $file (@files) {
    open(my $fh, '<:utf8', $file) or die "Cannot read $file: $!";
    my $content = do { local $/; <$fh> };
    close($fh);

    my $original = $content;

    # Update GA to be consent-conditional
    if ($content =~ /\Q$old_ga\E/) {
        $content =~ s/\Q$old_ga\E/$new_ga/;
        $ga_count++;
    }

    # Add banner before </body> if not already present
    if ($content !~ /tw-consent/ && $content =~ /<\/body>/) {
        $content =~ s/<\/body>/$banner/;
        $consent_count++;
    }

    if ($content ne $original) {
        open(my $out, '>:utf8', $file) or die "Cannot write $file: $!";
        print $out $content;
        close($out);
    }
}

print "GA updated on $ga_count files.\n";
print "Banner added to $consent_count files.\n";
