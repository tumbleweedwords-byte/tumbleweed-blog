import re, glob

CITY_RELATED = {
    'flash-fiction-berlin.html': [
        ('City', 'flash-fiction-prague.html', 'Prague'),
        ('City', 'flash-fiction-vienna.html', 'Vienna'),
        ('Theme', 'flash-fiction-about-solitude.html', 'Flash fiction about solitude'),
        ('Theme', 'flash-fiction-about-strangers.html', 'Flash fiction about strangers'),
    ],
    'flash-fiction-lisbon.html': [
        ('City', 'flash-fiction-porto.html', 'Porto'),
        ('City', 'flash-fiction-barcelona.html', 'Barcelona'),
        ('Theme', 'flash-fiction-about-memory.html', 'Flash fiction about memory'),
        ('Theme', 'flash-fiction-about-departure.html', 'Flash fiction about departure'),
    ],
    'flash-fiction-edinburgh.html': [
        ('City', 'flash-fiction-berlin.html', 'Berlin'),
        ('City', 'flash-fiction-reykjavik.html', 'Reykjavik'),
        ('Theme', 'flash-fiction-about-fog.html', 'Flash fiction about fog'),
        ('Theme', 'flash-fiction-about-solitude.html', 'Flash fiction about solitude'),
    ],
    'flash-fiction-buenos-aires.html': [
        ('City', 'flash-fiction-havana.html', 'Havana'),
        ('City', 'flash-fiction-belgrade.html', 'Belgrade'),
        ('Theme', 'flash-fiction-about-exile.html', 'Flash fiction about exile'),
        ('Theme', 'flash-fiction-about-return.html', 'Flash fiction about return'),
    ],
    'flash-fiction-istanbul.html': [
        ('City', 'flash-fiction-tangier.html', 'Tangier'),
        ('City', 'flash-fiction-tbilisi.html', 'Tbilisi'),
        ('Theme', 'flash-fiction-about-strangers.html', 'Flash fiction about strangers'),
        ('Theme', 'flash-fiction-about-borders.html', 'Flash fiction about borders'),
    ],
    'flash-fiction-prague.html': [
        ('City', 'flash-fiction-berlin.html', 'Berlin'),
        ('City', 'flash-fiction-warsaw.html', 'Warsaw'),
        ('Theme', 'flash-fiction-about-memory.html', 'Flash fiction about memory'),
        ('Theme', 'flash-fiction-about-insomnia.html', 'Flash fiction about insomnia'),
    ],
    'flash-fiction-vienna.html': [
        ('City', 'flash-fiction-prague.html', 'Prague'),
        ('City', 'flash-fiction-berlin.html', 'Berlin'),
        ('Theme', 'flash-fiction-about-last-things.html', 'Flash fiction about last things'),
        ('Theme', 'flash-fiction-about-letters.html', 'Flash fiction about letters'),
    ],
    'flash-fiction-warsaw.html': [
        ('City', 'flash-fiction-prague.html', 'Prague'),
        ('City', 'flash-fiction-belgrade.html', 'Belgrade'),
        ('Theme', 'flash-fiction-about-departure.html', 'Flash fiction about departure'),
        ('Theme', 'flash-fiction-about-grief.html', 'Flash fiction about grief'),
    ],
    'flash-fiction-belgrade.html': [
        ('City', 'flash-fiction-sarajevo.html', 'Sarajevo'),
        ('City', 'flash-fiction-buenos-aires.html', 'Buenos Aires'),
        ('Theme', 'flash-fiction-about-exile.html', 'Flash fiction about exile'),
        ('Theme', 'flash-fiction-about-return.html', 'Flash fiction about return'),
    ],
    'flash-fiction-sarajevo.html': [
        ('City', 'flash-fiction-belgrade.html', 'Belgrade'),
        ('City', 'flash-fiction-warsaw.html', 'Warsaw'),
        ('Theme', 'flash-fiction-about-grief.html', 'Flash fiction about grief'),
        ('Theme', 'flash-fiction-about-last-things.html', 'Flash fiction about last things'),
    ],
    'flash-fiction-barcelona.html': [
        ('City', 'flash-fiction-lisbon.html', 'Lisbon'),
        ('City', 'flash-fiction-marseille.html', 'Marseille'),
        ('Theme', 'flash-fiction-about-strangers.html', 'Flash fiction about strangers'),
        ('Theme', 'flash-fiction-about-hotels.html', 'Flash fiction about hotels'),
    ],
    'flash-fiction-porto.html': [
        ('City', 'flash-fiction-lisbon.html', 'Lisbon'),
        ('City', 'flash-fiction-edinburgh.html', 'Edinburgh'),
        ('Theme', 'flash-fiction-about-solitude.html', 'Flash fiction about solitude'),
        ('Theme', 'flash-fiction-about-memory.html', 'Flash fiction about memory'),
    ],
    'flash-fiction-marseille.html': [
        ('City', 'flash-fiction-barcelona.html', 'Barcelona'),
        ('City', 'flash-fiction-tangier.html', 'Tangier'),
        ('Theme', 'flash-fiction-about-exile.html', 'Flash fiction about exile'),
        ('Theme', 'flash-fiction-about-strangers.html', 'Flash fiction about strangers'),
    ],
    'flash-fiction-naples.html': [
        ('City', 'flash-fiction-barcelona.html', 'Barcelona'),
        ('City', 'flash-fiction-marseille.html', 'Marseille'),
        ('Theme', 'flash-fiction-about-grief.html', 'Flash fiction about grief'),
        ('Theme', 'flash-fiction-about-memory.html', 'Flash fiction about memory'),
    ],
    'flash-fiction-havana.html': [
        ('City', 'flash-fiction-buenos-aires.html', 'Buenos Aires'),
        ('City', 'flash-fiction-oaxaca.html', 'Oaxaca'),
        ('Theme', 'flash-fiction-about-exile.html', 'Flash fiction about exile'),
        ('Theme', 'flash-fiction-about-memory.html', 'Flash fiction about memory'),
    ],
    'flash-fiction-tbilisi.html': [
        ('City', 'flash-fiction-istanbul.html', 'Istanbul'),
        ('City', 'flash-fiction-tangier.html', 'Tangier'),
        ('Theme', 'flash-fiction-about-borders.html', 'Flash fiction about borders'),
        ('Theme', 'flash-fiction-about-strangers.html', 'Flash fiction about strangers'),
    ],
    'flash-fiction-thessaloniki.html': [
        ('City', 'flash-fiction-istanbul.html', 'Istanbul'),
        ('City', 'flash-fiction-naples.html', 'Naples'),
        ('Theme', 'flash-fiction-about-solitude.html', 'Flash fiction about solitude'),
        ('Theme', 'flash-fiction-about-exile.html', 'Flash fiction about exile'),
    ],
    'flash-fiction-tangier.html': [
        ('City', 'flash-fiction-istanbul.html', 'Istanbul'),
        ('City', 'flash-fiction-marseille.html', 'Marseille'),
        ('Theme', 'flash-fiction-about-borders.html', 'Flash fiction about borders'),
        ('Theme', 'flash-fiction-about-language-barriers.html', 'Flash fiction about language barriers'),
    ],
    'flash-fiction-reykjavik.html': [
        ('City', 'flash-fiction-edinburgh.html', 'Edinburgh'),
        ('City', 'flash-fiction-porto.html', 'Porto'),
        ('Theme', 'flash-fiction-about-solitude.html', 'Flash fiction about solitude'),
        ('Theme', 'flash-fiction-about-insomnia.html', 'Flash fiction about insomnia'),
    ],
    'flash-fiction-oaxaca.html': [
        ('City', 'flash-fiction-havana.html', 'Havana'),
        ('City', 'flash-fiction-buenos-aires.html', 'Buenos Aires'),
        ('Theme', 'flash-fiction-about-memory.html', 'Flash fiction about memory'),
        ('Theme', 'flash-fiction-about-last-things.html', 'Flash fiction about last things'),
    ],
}

THEME_RELATED = {
    'flash-fiction-about-memory.html': [
        ('Theme', 'flash-fiction-about-grief.html', 'Flash fiction about grief'),
        ('Theme', 'flash-fiction-about-letters.html', 'Flash fiction about letters'),
        ('City', 'flash-fiction-lisbon.html', 'Lisbon'),
        ('City', 'flash-fiction-prague.html', 'Prague'),
    ],
    'flash-fiction-about-grief.html': [
        ('Theme', 'flash-fiction-about-memory.html', 'Flash fiction about memory'),
        ('Theme', 'flash-fiction-about-last-things.html', 'Flash fiction about last things'),
        ('City', 'flash-fiction-sarajevo.html', 'Sarajevo'),
        ('City', 'flash-fiction-warsaw.html', 'Warsaw'),
    ],
    'flash-fiction-about-solitude.html': [
        ('Theme', 'flash-fiction-about-insomnia.html', 'Flash fiction about insomnia'),
        ('Theme', 'flash-fiction-about-hotels.html', 'Flash fiction about hotels'),
        ('City', 'flash-fiction-edinburgh.html', 'Edinburgh'),
        ('City', 'flash-fiction-reykjavik.html', 'Reykjavik'),
    ],
    'flash-fiction-about-exile.html': [
        ('Theme', 'flash-fiction-about-departure.html', 'Flash fiction about departure'),
        ('Theme', 'flash-fiction-about-borders.html', 'Flash fiction about borders'),
        ('City', 'flash-fiction-buenos-aires.html', 'Buenos Aires'),
        ('City', 'flash-fiction-havana.html', 'Havana'),
    ],
    'flash-fiction-about-departure.html': [
        ('Theme', 'flash-fiction-about-return.html', 'Flash fiction about return'),
        ('Theme', 'flash-fiction-about-trains.html', 'Flash fiction about trains'),
        ('City', 'flash-fiction-warsaw.html', 'Warsaw'),
        ('City', 'flash-fiction-barcelona.html', 'Barcelona'),
    ],
    'flash-fiction-about-return.html': [
        ('Theme', 'flash-fiction-about-departure.html', 'Flash fiction about departure'),
        ('Theme', 'flash-fiction-about-memory.html', 'Flash fiction about memory'),
        ('City', 'flash-fiction-buenos-aires.html', 'Buenos Aires'),
        ('City', 'flash-fiction-belgrade.html', 'Belgrade'),
    ],
    'flash-fiction-about-borders.html': [
        ('Theme', 'flash-fiction-about-exile.html', 'Flash fiction about exile'),
        ('Theme', 'flash-fiction-about-language-barriers.html', 'Flash fiction about language barriers'),
        ('City', 'flash-fiction-istanbul.html', 'Istanbul'),
        ('City', 'flash-fiction-tangier.html', 'Tangier'),
    ],
    'flash-fiction-about-strangers.html': [
        ('Theme', 'flash-fiction-about-trains.html', 'Flash fiction about trains'),
        ('Theme', 'flash-fiction-about-hotels.html', 'Flash fiction about hotels'),
        ('City', 'flash-fiction-barcelona.html', 'Barcelona'),
        ('City', 'flash-fiction-istanbul.html', 'Istanbul'),
    ],
    'flash-fiction-about-trains.html': [
        ('Theme', 'flash-fiction-about-departure.html', 'Flash fiction about departure'),
        ('Theme', 'flash-fiction-about-strangers.html', 'Flash fiction about strangers'),
        ('City', 'flash-fiction-berlin.html', 'Berlin'),
        ('City', 'flash-fiction-vienna.html', 'Vienna'),
    ],
    'flash-fiction-about-hotels.html': [
        ('Theme', 'flash-fiction-about-solitude.html', 'Flash fiction about solitude'),
        ('Theme', 'flash-fiction-about-strangers.html', 'Flash fiction about strangers'),
        ('City', 'flash-fiction-barcelona.html', 'Barcelona'),
        ('City', 'flash-fiction-lisbon.html', 'Lisbon'),
    ],
    'flash-fiction-about-fog.html': [
        ('Theme', 'flash-fiction-about-solitude.html', 'Flash fiction about solitude'),
        ('Theme', 'flash-fiction-about-insomnia.html', 'Flash fiction about insomnia'),
        ('City', 'flash-fiction-edinburgh.html', 'Edinburgh'),
        ('City', 'flash-fiction-reykjavik.html', 'Reykjavik'),
    ],
    'flash-fiction-about-insomnia.html': [
        ('Theme', 'flash-fiction-about-solitude.html', 'Flash fiction about solitude'),
        ('Theme', 'flash-fiction-about-fog.html', 'Flash fiction about fog'),
        ('City', 'flash-fiction-berlin.html', 'Berlin'),
        ('City', 'flash-fiction-prague.html', 'Prague'),
    ],
    'flash-fiction-about-letters.html': [
        ('Theme', 'flash-fiction-about-memory.html', 'Flash fiction about memory'),
        ('Theme', 'flash-fiction-about-last-things.html', 'Flash fiction about last things'),
        ('City', 'flash-fiction-lisbon.html', 'Lisbon'),
        ('City', 'flash-fiction-vienna.html', 'Vienna'),
    ],
    'flash-fiction-about-language-barriers.html': [
        ('Theme', 'flash-fiction-about-exile.html', 'Flash fiction about exile'),
        ('Theme', 'flash-fiction-about-strangers.html', 'Flash fiction about strangers'),
        ('City', 'flash-fiction-istanbul.html', 'Istanbul'),
        ('City', 'flash-fiction-tbilisi.html', 'Tbilisi'),
    ],
    'flash-fiction-about-last-things.html': [
        ('Theme', 'flash-fiction-about-grief.html', 'Flash fiction about grief'),
        ('Theme', 'flash-fiction-about-memory.html', 'Flash fiction about memory'),
        ('City', 'flash-fiction-vienna.html', 'Vienna'),
        ('City', 'flash-fiction-sarajevo.html', 'Sarajevo'),
    ],
}

ALL_RELATED = dict(list(CITY_RELATED.items()) + list(THEME_RELATED.items()))

def build_related_html(links):
    cards = ''
    for tag, slug, title in links:
        cards += '<a href="https://tumbleweedwords.com/{}" class="rel-card"><span class="rel-tag">{}</span><div class="rel-title">{}</div></a>'.format(slug, tag, title)
    return '<div class="related">{}</div>'.format(cards)

updated = 0
for filename, links in ALL_RELATED.items():
    try:
        content = open(filename, encoding='utf-8').read()
    except FileNotFoundError:
        print('MISSING: ' + filename)
        continue

    new_related = build_related_html(links)
    new_content = re.sub(r'<div class="related">.*?</div>', new_related, content, count=1, flags=re.DOTALL)

    if new_content != content:
        open(filename, 'w', encoding='utf-8').write(new_content)
        updated += 1
    else:
        print('NO MATCH: ' + filename)

print('Updated {} files'.format(updated))
