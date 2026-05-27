# Claude Code Prompt: Publish "A Man With No Purpose Is a Dangerous Man"

## Before you run this prompt

1. Drop these two files into the root of the `tumbleweedwords.com` repo:
   - `latest_new_short_story_by_me.docx` (the story)
   - `1775816181405_IMG_20251010_213855253.jpg` (the hero image)
2. Open Claude Code in the repo directory.
3. Paste everything below the line into Claude Code as one prompt.

---

# Task

Publish a new short story on tumbleweedwords.com. It must mirror the existing fiction pages exactly (same template, same fonts, same layout, same metadata pattern, same internal linking style). Do not introduce new design elements. UK English throughout. No em dashes anywhere in any code, copy, or metadata.

## Step 1: Read the source files

- Read `latest_new_short_story_by_me.docx` in the repo root. This is the story body. The working title at the top of the doc is the story title: **A Man With No Purpose Is a Dangerous Man**. Strip the working title from the body before publishing (it becomes the page H1, not in-body text). Preserve the asterisk section breaks (`*`) as styled dividers, matching how existing fiction pages render scene breaks.
- The hero image is `1775816181405_IMG_20251010_213855253.jpg`. It is a night shot of an Edinburgh tenement street: moonlit cloud, lone streetlight starburst, parked cars, wheelie bins, "The House of Smalls" sign on the right. Use it as the story's feature image.

## Step 2: Audit the existing fiction template

Before writing any code, list the existing fiction pages on the site (under `/fiction/` or wherever the fiction section lives). Open one as a template. Note exactly:

- File path and naming convention
- HTML structure, CSS classes, fonts
- How the hero image is sized, positioned, and given alt text
- How H1, byline, date, and body paragraphs are styled
- How scene breaks (`*`) are rendered
- How schema markup is structured (CreativeWork / ShortStory / Article)
- How internal links back to other stories, the fiction index, and the homepage are placed
- How the "Buy me a coffee" line and any Bookshop.org affiliate block appear at the foot
- How the page is added to the fiction index page
- How it gets entered into `sitemap.xml`

Mirror all of this. Do not improvise structure.

## Step 3: Optimise and place the hero image

- Resize and compress `1775816181405_IMG_20251010_213855253.jpg` to a sensible web hero size (max 1600px wide, under 300KB, JPEG quality ~80).
- Rename it to `a-man-with-no-purpose-hero.jpg`.
- Save it to wherever existing fiction images live (e.g. `/images/fiction/` or matching path).
- Alt text: `A moonlit Edinburgh tenement street at night, lone streetlight flaring against cloud, parked cars and wheelie bins along the pavement.`
- Do not delete the original upload until the build is verified.

## Step 4: Create the story page

- File path: match existing fiction pages exactly. Suggested slug: `a-man-with-no-purpose-is-a-dangerous-man`.
- Final URL: `https://tumbleweedwords.com/fiction/a-man-with-no-purpose-is-a-dangerous-man/` (or whatever pattern matches existing stories).
- H1: `A Man With No Purpose Is a Dangerous Man`
- Byline: `By David Moran`
- Date: today's date in the same format used by other fiction pages.
- Body: full story from the docx, with `*` rendered as scene breaks. Preserve paragraph breaks. UK English (the source is already UK English, leave it as is).
- Hero image directly under the H1 / byline block, matching existing fiction layout.
- Footer block: same internal links the other fiction pages use (back to Fiction index, to a related story if obvious, to the Substack signup, to Buy Me a Coffee).

## Step 5: SEO metadata

Insert into the page head, matching the pattern used on existing fiction pages:

- **Title tag:** `A Man With No Purpose Is a Dangerous Man | Short Fiction by David Moran | Tumbleweed Words`
- **Meta description:** `A short story by David Moran. Gabriel visits his best friend Johnny on a rough estate in a forgotten university town. Friendship, weed, violence, and the slow hum of a place running out of money.` (Keep under 160 characters; trim if needed.)
- **Canonical URL:** the final story URL.
- **Open Graph tags:** og:title, og:description, og:image (point to the hero), og:type = article, og:url.
- **Twitter card:** summary_large_image with same fields.
- **Schema markup:** JSON-LD `ShortStory` (or `Article` if that is what existing fiction pages use). Include: headline, author (David Moran with sameAs link to Substack), datePublished, image, publisher, mainEntityOfPage, description, inLanguage `en-GB`.

## Step 6: Add to fiction index

Add a card / list entry on the Fiction index page for the new story. Mirror the existing card pattern: thumbnail (use the hero image, smaller), title, one-sentence teaser, link.

Teaser: `Gabriel cycles uphill to Johnny's flat in a town the money has left. Then one afternoon Johnny goes out for weed and does not come back the same.`

Place the new card at the top of the index (newest first) unless the existing pattern is different.

## Step 7: Homepage carousel

Find the homepage carousel component. Add a new slide for this story:

- Image: the hero image (or carousel-sized version if existing slides use a specific crop).
- Headline: `A Man With No Purpose Is a Dangerous Man`
- Subline: `New short fiction. Gabriel, Johnny, and a town running on fumes.`
- CTA link: the new story URL.

Match exactly how other carousel slides are coded. Place this slide first so it appears as the featured item.

## Step 8: Sitemap and internal linking

- Add the new URL to `sitemap.xml` with today's `lastmod`.
- Update `lastmod` on `sitemap.xml` itself, the homepage entry, and the fiction index entry.
- Find 2–3 existing pages on the site (other fiction pieces, craft essays, or the about page) where it would be natural to link to this new story. Add contextual internal links from those pages back to the new story. Do not force it. If nothing fits, skip.

## Step 9: Verify before pushing

- Run any existing build / lint checks the repo uses.
- Check the story page renders locally if a local preview is available.
- Confirm: page exists, hero loads, schema validates (mentally check the JSON-LD structure), fiction index shows the new card, homepage carousel shows the new slide, sitemap contains the new URL.
- No em dashes anywhere. No American spellings. No new fonts or colours introduced.

## Step 10: Commit and push

- Stage all changes.
- Commit message: `Add new short story: A Man With No Purpose Is a Dangerous Man`
- Push to main. GitHub Pages will rebuild automatically.

## Step 11: Report back

Once pushed, output:

- Final live URL of the story
- File paths created or modified
- Any pages where internal links were added
- Anything skipped or that needs my attention
