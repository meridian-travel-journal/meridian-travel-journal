import os, json
from urllib.parse import quote
SITE = "https://your-domain.example"   # <- set your real domain (used for canonical + sitemap only)
SOURCE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(SOURCE)
os.makedirs(OUT + "/assets", exist_ok=True)

NAV = [("index.html","Home"),("destinations.html","Destinations"),("travel-tips.html","Tips"),("culture.html","Culture"),
       ("food.html","Food"),("inspiration.html","Inspire")]
PAGES = [("index.html","Home","Worldwide travel stories and guides"),
 ("destinations.html","Destinations","Browse and filter guides by region"),
 ("lofoten.html","Lofoten, Norway","Fjords, red cabins and midnight light"),
 ("cinque-terre.html","Cinque Terre, Italy","Five cliffside villages on the Ligurian coast"),
 ("florence.html","36 hours in Florence","A weekend itinerary through Tuscany's capital"),
 ("travel-tips.html","Travel tips","Packing, documents and planning checklists"),
 ("culture.html","Culture and heritage","Landmarks and how to visit them well"),
 ("food.html","Food and local experiences","Dishes worth travelling for"),
 ("inspiration.html","Inspiration","Take the quiz, find your next place"),
 ("about.html","About","Who we are"),("contact.html","Contact","Send us a note"),
 ("saved.html","Saved guides","Your bookmarks"),("credits.html","Photo credits","Image sources and licences")]

def commons(name, w=1600):
    return "https://commons.wikimedia.org/wiki/Special:FilePath/" + quote(name) + "?width=%d" % w

PHOTO_FILES = {
    "Cinque Terre": "Cinque Terre (Italy, October 2020) - 24 (50543603956).jpg",
    "Florence": "Firenze - Piazzale Michelangelo, Firenze, Italy - April 6, 2015 02.jpg",
    "Lofoten": "Reine at Reinefjorden, 2010 September.jpg",
    "Manarola": "Manarola NW Cinque Terre Sep23 A7C 07233.jpg",
    "Florence_Cathedral": "Cattedrale di Santa Maria del Fiore – Il Duomo di Firenze.jpg",
    "Maldives": "Kuramathi Beach (Lagoon) 001.jpg",
    "Bali": "Ubud (49818456887).jpg",
    "Iceland": "2008-05-24 35 Skógafoss.jpg",
    "Patagonia": "Torres del Paine y cuernos del Paine, montaje.jpg",
    "Santorini": "Oia sunset - panoramio (2).jpg",
    "Mole": "ChickRedMole.JPG",
    "Vernazza": "Vernazza and the sea, Cinque Terre, Italy.jpg",
    "Kyoto": "Kiyomizu-dera, Kyoto, November 2016 -02.jpg",
    "Marrakesh": "Marrakech, Morocco (5421595453) (5).jpg",
    "Cappadocia": "Cappadocia balloon trip, Ortahisar Castle (11893715185).jpg",
    "Angkor_Wat": "Angkor Wat.jpg",
    "Machu_Picchu": "Machu Picchu, 2023 (012).jpg",
    "Acropolis_of_Athens": "1029 Acropolis of Athens in Greece at night Photo by Giles Laurent.jpg",
    "Taj_Mahal": "Taj Mahal (Edited).jpeg",
    "Sushi": "Sushi platter.jpg",
    "Tagine": "Moroccan food-Chicken tagine with preserved lemons and olives-01.jpg",
    "Paella": "01 Paella Valenciana original.jpg",
    "Ramen": "Shoyu Ramen（Tokyo Ramen） - 01.jpg",
    "Gelato": "Delicious Gelato on display.jpg",
    "Ponte_Vecchio": "Ponte Vecchio from Ponte alle Grazie.jpg",
    "Riomaggiore": "Riomaggiore From Ferry Cinque Terre Italy Sep23 A7C 07414.jpg",
    "Lisbon_Alfama": "View across Alfama from the Miradouro de Santa Luzia 01.jpg",
}

def ph(wiki=None, file=None, alt="", label="", cls=""):
    """One photo slot. wiki = Wikipedia article whose lead photo is used; file = exact Commons file."""
    file = file or PHOTO_FILES.get(wiki)
    a = ' data-wiki="%s"' % wiki if wiki and not file else ""
    src = (' src="%s" srcset="%s 800w, %s 1600w" sizes="(max-width: 700px) 90vw, 75vw"' %
           (commons(file), commons(file, 800).replace("&","&amp;"), commons(file, 1600).replace("&","&amp;"))) if file else ""
    on = " on" if file else ""
    priority = "hero-image" in cls or "lead-photo" in cls or cls == "full"
    loading = 'loading="eager" fetchpriority="high"' if priority else 'loading="lazy"'
    return ('<figure class="ph %s%s" data-label="%s"%s><img alt="%s" %s decoding="async"%s></figure>'
            % (cls, on, label or alt, a, alt, loading, src))

def rail_controls():
    return '<div class="rail-controls"><button type="button" data-prev aria-label="Previous story">←</button><span data-count aria-live="polite"></span><span class="rail-line"><i data-progress></i></span><button type="button" data-next aria-label="Next story">→</button></div>'

def related_rail(entries):
    slides = "".join(card(h, w, t, tag, description) for h,w,t,tag,description in entries)
    return ('<section class="wrap related-stories"><p class="eyebrow">KEEP EXPLORING / THE JOURNAL</p>'
            '<h2 class="serif">More stories for the road.</h2><div class="story-carousel" data-carousel>'
            '<div class="story-rail" tabindex="0" aria-label="Related destination stories">%s</div>%s</div></section>'
            % (slides, rail_controls()))

def bm(href, title):
    return '<button class="bm" type="button" aria-label="Save %s" data-bm="%s|%s">♡</button>' % (title, href, title)

def card(href, wiki, title, tag, blurb, region="", cls=""):
    return ('<article class="card %s" data-region="%s" data-t="%s">%s<div class="cb"><span class="tag">%s</span>'
            '<h3><a href="%s">%s</a></h3><p>%s</p></div>%s</article>'
            % (cls, region, (title+" "+blurb).lower(), ph(wiki, alt=title+" — "+blurb, label=title, cls="lead-photo" if "priority" in cls else ""), tag, href, title, blurb, bm(href, title)))

def rate(i): return '<div class="rate" data-id="%s" aria-label="Rate this guide">%s<span class="rv"></span></div>' % (i, "".join('<button type="button" data-v="%d" aria-label="%d stars">★</button>'%(n,n) for n in range(1,6)))
def react(i): return '<div class="react" data-id="%s">%s</div>' % (i, "".join('<button type="button" data-e="%s">%s <b>0</b></button>'%(e,e) for e in "😍🔥🧭🙌"))
def share(): return '<div class="share"><button type="button" data-copy>Copy link</button><button type="button" data-native>Share</button></div>'
def crumbs(*items):
    out = '<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a>'
    for h,t in items: out += ' / ' + ('<a href="%s">%s</a>'%(h,t) if h else '<span aria-current="page">%s</span>'%t)
    return out + '</nav>'

def layout(slug, title, desc, body, cls="", ld=None):
    nav = "".join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h==slug else "", t) for h,t in NAV)
    ld = ld or {"@context":"https://schema.org","@type":"WebPage","name":title,"description":desc,"url":SITE+"/"+slug}
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | Meridian Travel Journal</title><meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}/{slug}"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:ital,wght@0,700;0,800;1,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css"><script type="application/ld+json">{json.dumps(ld)}</script></head>
<body class="{cls}"><div id="prog" aria-hidden="true"></div><a class="skip" href="#main">Skip to content</a>
<header class="top"><a class="logo masthead-logo" href="index.html" aria-label="Meridian Travel Journal home"><span class="brand-name serif">meridian<span>.</span></span><span class="brand-caption">THE TRAVEL JOURNAL</span></a><nav class="nav" id="nav" aria-label="Main">{nav}</nav>
<div class="tools"><button id="sb" type="button" aria-label="Search"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/></svg><span>Search</span></button><a href="saved.html" class="saved" aria-label="Saved guides"><span aria-hidden="true">♡</span> <b id="bc">0</b></a><button id="mb" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M3 8h18M3 16h18"/></svg><span>Menu</span></button></div></header>
<div id="so" class="so" hidden><div class="sbox"><input id="sq" type="search" placeholder="Search guides, places, tips" aria-label="Search"><button id="sx" type="button">Close</button><ul id="sr"></ul></div></div>
<nav class="quick-rail" aria-label="Quick links"><button type="button" id="quick-search" aria-controls="so">Search</button><a href="#nle">Subscribe</a><a href="saved.html">Saved</a><a href="contact.html">Contact</a></nav>
<main id="main">{body}</main>
<footer class="foot">
<div class="footer-intro"><span>THE MERIDIAN TRAVEL JOURNAL</span><span>AN INVITATION TO WANDER <span aria-hidden="true">✳</span></span></div>
<div class="fg">
<nav class="footer-column footer-nav" aria-label="Explore Meridian"><h2>Find your way</h2><a href="index.html">Home</a>{"".join('<a href="%s">%s</a>'%(h,t) for h,t in NAV[1:])}</nav>
<nav class="footer-column footer-nav" aria-label="Journal links"><h2>From the journal</h2><a href="lofoten.html">Lofoten</a><a href="cinque-terre.html">Cinque Terre</a><a href="florence.html">Florence</a><a href="saved.html">Saved guides</a><a href="about.html">About</a></nav>
<form class="nl footer-column" novalidate><h2>A letter from elsewhere</h2><p>Travel stories, thoughtful guides and a little inspiration for your next journey.</p><label for="nle">Your email address</label><input id="nle" type="email" placeholder="you@example.com" required><button type="submit">Subscribe <span aria-hidden="true">↗</span></button><p class="msg" role="status"></p></form>
<div class="footer-signoff"><div class="footer-seal" aria-hidden="true"><span>THE ART OF GOING ELSEWHERE</span><svg viewBox="0 0 100 100" fill="none"><circle cx="50" cy="50" r="36"/><circle cx="50" cy="50" r="29"/><path d="M50 10v80M10 50h80M50 24l7 19 19 7-19 7-7 19-7-19-19-7 19-7z"/><circle cx="50" cy="50" r="3"/></svg><span>MERIDIAN • TRAVEL JOURNAL</span></div><p class="footer-quote serif">For the curious,<br><em>wherever you go.</em></p><a class="footer-return" href="#" aria-label="Back to top">BACK TO TOP <span aria-hidden="true">↗</span></a></div>
</div>
<div class="footer-bottom"><p>© <span id="yr">2026</span> Meridian Travel Journal</p><p>MADE FOR THE LONG WAY AROUND <span aria-hidden="true">✳</span></p></div></footer>
<button id="top" type="button" aria-label="Back to top" hidden>↑</button><script src="assets/app.js" defer></script></body></html>'''
    open(os.path.join(OUT, slug), "w", encoding="utf-8").write(html)

# ---------------------------------------------------------------- HOME
body = f'''<section class="opening">
{ph(file="Reine at Reinefjorden, 2010 September.jpg", alt="Red fishing cabins and mountains at Reine in the Lofoten islands, Norway", label="Lofoten", cls="hero-image")}
<div class="opening-copy"><p class="opening-kicker">AN INDEPENDENT JOURNAL FOR CURIOUS TRAVELLERS</p>
<h1 class="serif">The art of<br><em>going elsewhere.</em></h1>
<p>For places that stay with you long after you leave.</p><a href="destinations.html" class="opening-link">EXPLORE THE JOURNAL <span>↗</span></a></div>
<div class="opening-bottom"><span>01 / LOFOTEN, NORWAY</span><a href="#home-latest">SCROLL TO EXPLORE ↓</a><a href="lofoten.html">THE STORY BEHIND THE VIEW ↗</a></div></section>
<div class="ticker" aria-label="Explore the journal"><span>PLACES WITH SOUL</span><b>✳</b><span>THE SCENIC ROUTE</span><b>✳</b><span>GOOD FOOD, GOOD STORIES</span><b>✳</b><span>TRAVEL A LITTLE DIFFERENTLY</span></div>
<section class="wrap" id="home-latest"><div class="section-intro"><div><p class="eyebrow">THE MERIDIAN EDIT / 01</p><h2 class="serif">A few places <em>we love.</em></h2><p>For the daydreamers, the list-makers, and everyone in between.</p></div><a class="text-link" href="destinations.html">VIEW ALL DESTINATIONS ↗</a></div>
<div class="home-filters" role="group" aria-label="Filter stories by travel mood"><span>FIND YOUR KIND OF PLACE</span><button type="button" data-mood="all" aria-pressed="true">All stories</button><button type="button" data-mood="coast" aria-pressed="false">Coastal days</button><button type="button" data-mood="city" aria-pressed="false">City wandering</button><button type="button" data-mood="nature" aria-pressed="false">Into nature</button></div>
<div class="story-carousel" data-carousel><div class="story-rail home-stories" tabindex="0" aria-label="Featured destination stories">{card("cinque-terre.html","Cinque Terre","Cinque Terre","Italy","Five colourful villages, coastal paths and a slower way to see the Italian Riviera.","coast","tall")}
{card("florence.html","Florence","36 hours in Florence","Italy","A weekend of Renaissance art, winding streets and very good food.","city")}
{card("lofoten.html","Lofoten","Lofoten","Norway","Fishing villages, mountain trails and the extraordinary light of the Arctic.","nature")}</div>{rail_controls()}</div></section>
<section class="editorial-band"><div class="editorial-image">{ph("Manarola", alt="Colourful houses above the sea in Manarola, Cinque Terre", label="Manarola")}</div><div class="editorial-copy"><p class="eyebrow">A NOTE FROM MERIDIAN / 02</p><h2 class="serif">Take the long way <em>home.</em></h2><p>Some of the best travel moments aren't on an itinerary. They're found over a long lunch, down a quiet street, or wherever curiosity takes you.</p><a class="text-link" href="inspiration.html">FIND YOUR NEXT PLACE ↗</a></div><span class="editorial-number">02</span></section>
<section class="wrap" id="home-pillars"><div class="section-intro"><div><p class="eyebrow">A WORLD OF WAYS TO WANDER / 03</p><h2 class="serif">The journey is <em>yours.</em></h2><p>A little inspiration for wherever you're headed next.</p></div></div><ul class="pillars">
<li><a href="destinations.html"><span>01 / EXPLORE</span><b class="serif">Destinations</b><p>Find a place that feels like you.</p><i>↗</i></a></li>
<li><a href="food.html"><span>02 / TASTE</span><b class="serif">Food & drink</b><p>Get to know a place one bite at a time.</p><i>↗</i></a></li>
<li><a href="culture.html"><span>03 / CONNECT</span><b class="serif">Culture</b><p>See more, and travel thoughtfully.</p><i>↗</i></a></li>
<li><a href="travel-tips.html"><span>04 / PREPARE</span><b class="serif">Travel tips</b><p>Thoughtful notes for the road ahead.</p><i>↗</i></a></li></ul></section>'''
layout("index.html","Worldwide travel inspiration and destination guides","An independent travel journal with destination guides, tips, culture and food from around the world.",body,"home",
 {"@context":"https://schema.org","@type":"WebSite","name":"Meridian Travel Journal","url":SITE})

# ---------------------------------------------------------------- DESTINATIONS
D = [("Maldives","Maldives","Islands","Overwater villas and glassy lagoons.","islands"),
 ("Kyoto","Kyoto, Japan","Asia","Moss gardens, temples and tea houses.","asia"),
 ("Marrakesh","Marrakesh, Morocco","Africa","Courtyard riads and a night-time square.","africa"),
 ("Patagonia","Patagonia","Americas","Granite spires and endless steppe.","americas"),
 ("Santorini","Santorini, Greece","Europe","White villages on a drowned volcano.","europe"),
 ("Bali","Bali, Indonesia","Asia","Rice terraces, temples and surf.","asia"),
 ("Cappadocia","Cappadocia, Türkiye","Asia","Fairy chimneys and sunrise balloons.","asia"),
 ("Iceland","Iceland","Europe","Waterfalls, lava fields and long dusk.","europe")]
destination_guides = {
 "Maldives": ("maldives.html", "A slower rhythm on the water", "Coral islands, clear lagoons and life shaped by the Indian Ocean make the Maldives a place to linger. Explore beyond the resort experience by learning about island communities and marine life.",
  "December to April is generally drier; the wetter months can bring showers and lower prices. Conditions vary between atolls.",
  "International flights arrive at Malé. Depending on your island, onward travel may involve a speedboat, domestic flight or seaplane; arrange transfers with your accommodation.",
  ["Swim or snorkel with a responsible local operator", "Visit an inhabited island and support local businesses", "Watch the changing colours of the lagoon"]),
 "Kyoto": ("kyoto.html", "Old traditions, lived in the present", "Kyoto rewards an unhurried approach: temple gardens, neighbourhood lanes, craft workshops and seasonal food reveal a city that is both historic and very much alive.",
  "Spring blossoms and autumn foliage are popular, busy seasons. Early mornings and quieter neighbourhoods can offer a gentler experience.",
  "Kyoto is well connected by train, including the shinkansen. Use trains, subways and buses to move around, and group nearby sights together.",
  ["Walk the wooded paths around Fushimi Inari", "Visit Kiyomizu-dera and explore the Higashiyama lanes", "Pause for tea and seasonal sweets"]),
 "Marrakesh": ("marrakesh.html", "A city of courtyards and colour", "Inside the medina, market lanes open onto shaded courtyards and gardens. Marrakesh is best discovered at a measured pace, with time for its food, craft and hospitality.",
  "Spring and autumn are often more comfortable for walking; summer afternoons can be very hot.",
  "Marrakesh has an international airport and rail connections to other Moroccan cities. In the medina, expect to explore many lanes on foot.",
  ["Explore the souks with time to wander", "Visit a garden or a historic courtyard", "Experience the evening food stalls around Jemaa el-Fnaa"]),
 "Patagonia": ("patagonia.html", "At the edge of the continent", "Patagonia stretches across southern Chile and Argentina, from windswept steppe to glacial lakes and mountain ranges. Choose a few bases rather than trying to see it all at once.",
  "The southern summer, roughly December to February, offers long days; weather can change quickly in any season.",
  "Distances are large. Plan flights, buses or a rental car around your chosen area, and check border requirements if travelling between Chile and Argentina.",
  ["Explore trails in Torres del Paine National Park", "Discover the mountain town of El Chaltén", "See glacial landscapes with a reputable local guide"]),
 "Santorini": ("santorini.html", "Life along the caldera", "Whitewashed villages trace the rim of Santorini's volcanic caldera. Beyond the famous views, look for archaeological sites, local vineyards and quieter corners of the island.",
  "Late spring and early autumn can be warm with fewer visitors than peak summer. Ferry schedules and opening hours change with the season.",
  "Reach the island by air or ferry. Buses connect major villages, while taxis and rentals can help with less-served places.",
  ["Walk part of the caldera path between Fira and Oia", "Explore the archaeological site at Akrotiri", "Try local wines made from grapes grown on volcanic soil"]),
 "Bali": ("bali.html", "An island beyond the beach", "Bali brings together coastal landscapes, rice fields, village life and living temple traditions. Spend time in more than one area and make space to travel respectfully.",
  "The drier season generally runs from April to October, though tropical showers are possible year-round.",
  "International flights arrive near Denpasar. Road journeys can take longer than expected, so allow extra time and use a reputable local driver when needed.",
  ["Explore the rice-field landscapes around Ubud", "Visit a temple respectfully in appropriate clothing", "Discover the coast with a locally run surf or snorkel guide"]),
 "Cappadocia": ("cappadocia.html", "A landscape shaped by time", "Cappadocia's valleys are known for their rock formations, cave dwellings and early churches. The best days leave room for both a viewpoint and a walk among the valleys.",
  "Spring and autumn often bring pleasant walking conditions. Balloon flights depend on weather and can be cancelled, so leave flexibility.",
  "The region is served by airports near Kayseri and Nevşehir. Göreme is a popular base; arrange transfers or transport for the wider region.",
  ["Walk among the rock formations of a nearby valley", "Explore the rock-cut churches at Göreme Open Air Museum", "Watch the sunrise over the valleys"]),
 "Iceland": ("iceland.html", "A land in motion", "Waterfalls, volcanic landscapes and geothermal pools make Iceland a journey through powerful natural forces. Let the weather shape your route and leave room for the unexpected.",
  "Summer brings long daylight hours; winter offers darker skies and a chance of northern lights, but road and weather conditions can be challenging.",
  "International flights commonly arrive at Keflavík. A car offers flexibility outside Reykjavík, but always check road and weather conditions before setting out.",
  ["Visit waterfalls along the south coast", "Explore geothermal landscapes and bathing pools", "Take a guided walk or boat trip suited to the season"])
}
PAGES.extend((destination_guides[w][0], t, "Travel guide to "+t) for w,t,_,_,_ in D)
chips = "".join('<button type="button" data-f="%s">%s</button>'%(k,v) for k,v in [("all","All"),("europe","Europe"),("asia","Asia"),("africa","Africa"),("americas","Americas"),("islands","Islands")])
grid = "".join(card(destination_guides[w][0], w, t, tag, b, r, "priority" if i==0 else "") for i,(w,t,tag,b,r) in enumerate(D))
body = f'''<section class="destination-intro"><p class="eyebrow">THE MERIDIAN ATLAS / PLACES TO KNOW</p><h1 class="serif">A world of <em>elsewhere.</em></h1><p>Follow your curiosity. Find a place worth lingering in.</p></section>
<section class="destination-stage">
<div class="filters" id="dest-filters"><div class="chips" role="group" aria-label="Region">{chips}</div><label class="sr" for="dq">Filter</label><input id="dq" type="search" placeholder="Filter by name or mood"></div>
<div class="story-carousel" data-carousel><div class="story-rail" id="dest-grid" tabindex="0" aria-label="Destination stories">{grid}</div>{rail_controls()}</div><p id="dest-empty" class="empty" hidden>Nothing matches. Clear the filter or try another word.</p></section>
<section class="guide-index wrap"><p class="eyebrow">THE STORIES BEHIND THE PLACES</p><h2 class="serif">Go a little deeper.</h2><ul class="guides"><li><a href="lofoten.html"><b class="serif">01 / Lofoten</b><span>Norway · An Arctic escape ↗</span></a></li><li><a href="cinque-terre.html"><b class="serif">02 / Cinque Terre</b><span>Italy · Five villages, one coastline ↗</span></a></li><li><a href="florence.html"><b class="serif">03 / Florence</b><span>Italy · A weekend in the city ↗</span></a></li></ul></section>'''
layout("destinations.html","Destinations","Filter worldwide travel guides by region and mood.",body,"dest")

# ---------------------------------------------------------------- DESTINATION GUIDES
for i, (wiki, title, region, blurb, region_filter) in enumerate(D):
    slug, heading, introduction, when, getting_there, highlights = destination_guides[wiki]
    next_wiki, next_title, next_region, next_blurb, _ = D[(i + 1) % len(D)]
    highlight_items = "".join("<li>%s</li>" % item for item in highlights)
    body = f'''<section class="atlas-opening">{ph(wiki, alt=title, label=title, cls="lead-photo")}<div class="atlas-opening-copy"><p class="eyebrow">THE MERIDIAN ATLAS / {region}</p><h1 class="serif">{title}</h1><p>{blurb}</p></div></section>
<section class="atlas-guide wrap"><div class="atlas-intro"><p class="eyebrow">A PLACE TO KNOW / {region}</p><h2 class="serif">{heading}.</h2><p>{introduction}</p><div class="atlas-actions">{bm(slug,title)}{share()}</div></div>
<div class="atlas-notes"><div><span>01 / THE SEASON</span><h2 class="serif">When to go</h2><p>{when}</p></div><div><span>02 / THE JOURNEY</span><h2 class="serif">Getting there</h2><p>{getting_there}</p></div></div></section>
<section class="atlas-highlights"><div><p class="eyebrow">A LITTLE INSPIRATION</p><h2 class="serif">While you're <em>there.</em></h2></div><ol>{highlight_items}</ol></section>
<section class="wrap atlas-review"><h2 class="serif">Rate this guide</h2>{rate(wiki.lower())}{react(wiki.lower())}</section>
<section class="next-story"><p class="eyebrow">KEEP WANDERING / NEXT DESTINATION</p><a href="{destination_guides[next_wiki][0]}" class="serif">Discover {next_title} <span>↗</span></a><p>{next_blurb}</p></section>
{related_rail([(destination_guides[next_wiki][0],next_wiki,next_title,next_region,next_blurb),("florence.html","Florence","36 hours in Florence","Italy","Art, markets and a city made for walking.")])}'''
    layout(slug, title + " travel guide", "Discover " + title + ": when to go, how to get there and what to explore.", body, "atlas-guide-page")

# ---------------------------------------------------------------- LOFOTEN (split sticky)
body = f'''<section class="lofoten-opening">{ph(file="Reine Lofoten 2009.JPG", alt="The fishing village of Reine on the Lofoten islands", label="Reine", cls="full")}<div><p>THE NORTHERN JOURNAL / NORWAY</p><h1 class="serif">Lofoten<span>, Norway</span></h1><p>Where the mountains meet the sea.</p></div></section><section class="split"><aside class="side"><h2 class="serif">A guide to<br>the islands.</h2>
<p class="by"><b>Meridian Editors</b><br>Arctic Norway</p><nav class="toc" aria-label="On this page"><a href="#lf-when">When to go</a><a href="#lf-reach">Getting there</a><a href="#lf-stay">Where to stay</a><a href="#lf-see">What to see</a><a href="#lf-rate">Rate this guide</a></nav>{bm("lofoten.html","Lofoten, Norway")}{share()}</aside>
<article class="art"><p class="lede">Before the crowds find the next fjord, Lofoten still feels like the edge of something.</p>
<h2 id="lf-when">When to go</h2><p>June to August brings the midnight sun. September to March gives northern lights and quiet roads.</p>
{ph(file="Lofoten, Norway (Unsplash).jpg", alt="Aurora borealis over Flakstad in Lofoten", label="Aurora", cls="wide")}
<h2 id="lf-reach">Getting there</h2><p>Fly to Leknes or Svolvær, or take the ferry from Bodø. A car makes the islands easy.</p>
<h2 id="lf-stay">Where to stay</h2><p>Book a converted fishermen's cabin (rorbu) on the water. Reserve early for summer.</p>
{ph(file="0688 Norway Lofoten bridge between Sakrisoya and Andoya.jpg", alt="Road bridge between Sakrisøya and Andøya in Lofoten", label="Bridge", cls="wide")}
<h2 id="lf-see">What to see</h2><ul class="tick"><li>Reinebringen viewpoint at sunrise</li><li>Henningsvær harbour</li><li>Haukland and Uttakleiv beaches</li><li>The Å fishing museum</li></ul>
<h2 id="lf-rate">Rate this guide</h2>{rate("lofoten")}{react("lofoten")}</article></section>
<section class="next-story"><p class="eyebrow">KEEP WANDERING / NEXT STORY</p><a href="cinque-terre.html" class="serif">From Arctic light to the Italian coast <span>↗</span></a><p>Discover the villages of Cinque Terre.</p></section>
{related_rail([("cinque-terre.html","Cinque Terre","Cinque Terre","Italy","Five villages and one unforgettable coastline."),("florence.html","Florence","36 hours in Florence","Italy","Art, markets and a city made for walking.")])}'''
layout("lofoten.html","Lofoten, Norway travel guide","When to go, how to get there and what to see in the Lofoten islands.",body,"split-p")

# ---------------------------------------------------------------- CINQUE TERRE (magazine spread)
body = f'''<section class="spread">{ph("Manarola", alt="Colourful houses of Manarola above the sea, Cinque Terre", label="Manarola", cls="full")}
<div class="sp-t"><h1 class="serif caps">Cinque<br>Terre</h1><p class="sub serif">Five villages, one coastline</p>
<div class="cols dropcap"><p>Five fishing villages cling to the Ligurian cliffs, linked by trails, trains and boats. Walk between them, swim off the rocks, and eat focaccia in every one.</p>
<p>Base yourself in one village and use the train for the rest. Go in spring or autumn for softer light and fewer people.</p></div>
<div class="row">{bm("cinque-terre.html","Cinque Terre, Italy")}{share()}</div></div></section>
<section class="wrap" id="ct-towns"><div class="sh"><h2>The five villages</h2></div><div class="acc" id="ct-acc">
<details open><summary class="serif">Monterosso al Mare</summary><p>The only proper beach, and the easiest base for families.</p></details>
<details><summary class="serif">Vernazza</summary><p>A tiny harbour and a castle tower. Arrive early or stay late.</p></details>
<details><summary class="serif">Corniglia</summary><p>The quiet one, up 382 steps. Rewarding and rarely crowded.</p></details>
<details><summary class="serif">Manarola</summary><p>The postcard view, best at sunset from the rocks.</p></details>
<details><summary class="serif">Riomaggiore</summary><p>Steep lanes, small marinas and the start of the Via dell'Amore.</p></details></div></section>
<section class="wrap pair" id="ct-more"><div>{ph("Vernazza", alt="Vernazza harbour in Cinque Terre", label="Vernazza")}<p class="cap">Vernazza harbour</p></div><div>{ph("Riomaggiore", alt="Riomaggiore houses on the cliff", label="Riomaggiore")}<p class="cap">Riomaggiore from the water</p></div></section>
<section class="wrap" id="ct-rate"><h2 class="serif">Rate this guide</h2>{rate("cinque")}{react("cinque")}</section><section class="next-story"><p class="eyebrow">CONTINUE THROUGH ITALY</p><a href="florence.html" class="serif">A weekend in Florence <span>↗</span></a><p>Art, markets and a city made for walking.</p></section>
{related_rail([("florence.html","Florence","36 hours in Florence","Italy","A weekend of art, markets and winding streets."),("lofoten.html","Lofoten","Lofoten","Norway","Fishing villages and extraordinary Arctic light.")])}'''
layout("cinque-terre.html","Cinque Terre travel guide","The five villages of Cinque Terre: where to base yourself and when to go.",body,"spread-p")

# ---------------------------------------------------------------- FLORENCE (full bleed + timeline)
tl = [("Friday","6:00 pm","Climb to Piazzale Michelangelo for the skyline at dusk."),("Friday","8:30 pm","Dinner of bistecca and Chianti in Oltrarno."),
("Saturday","8:00 am","Walk the Duomo and climb the dome before the queues."),("Saturday","1:00 pm","Lunch at Mercato Centrale: pasta, lampredotto, gelato."),
("Saturday","4:00 pm","Cross Ponte Vecchio and wander the Pitti side."),("Sunday","9:00 am","Uffizi, booked ahead. Keep it to two hours."),("Sunday","1:00 pm","Slow aperitivo before the train home.")]
items = "".join('<li class="tli"><button type="button" aria-expanded="false"><b>%s</b><i>%s</i><span>%s</span></button></li>'%(d,t,x) for d,t,x in tl)
body = f'''<section class="bleed">{ph("Florence_Cathedral", alt="Florence Cathedral dome above the terracotta rooftops", label="Florence", cls="full")}
<div class="bl-t"><p class="serif ital">Tuscan food amid alluring architecture</p><h1 class="serif"><span>36 hours in</span> Florence</h1></div></section>
<section class="wrap narrow" id="fl-plan">{crumbs(("destinations.html","Destinations"),(None,"Florence"))}<p class="lede">Compact, walkable and rich. This route fits a weekend. Tap a stop to mark it done.</p>
<ol class="tline" id="fl-tl">{items}</ol><div class="prog"><span id="fl-bar"></span></div><p class="cap" id="fl-count">0 of 7 stops done</p></section>
<section class="wrap pair" id="fl-pics"><div>{ph("Ponte_Vecchio", alt="Ponte Vecchio over the Arno in Florence", label="Ponte Vecchio")}<p class="cap">Ponte Vecchio at golden hour</p></div>
<div class="center">{bm("florence.html","36 hours in Florence")}{share()}{rate("florence")}{react("florence")}</div></section><section class="next-story"><p class="eyebrow">A TASTE OF THE JOURNEY</p><a href="food.html" class="serif">Travel by appetite <span>↗</span></a><p>Discover dishes and local flavours from around the world.</p></section>
{related_rail([("cinque-terre.html","Cinque Terre","Cinque Terre","Italy","Five colourful villages on the Italian Riviera."),("lofoten.html","Lofoten","Lofoten","Norway","Fishing villages, mountain trails and Arctic light.")])}'''
layout("florence.html","36 hours in Florence","A weekend itinerary for Florence with times, food and the views worth the climb.",body,"bleed-p")

# ---------------------------------------------------------------- TIPS (tabs + checklist)
tips = {"Packing":["Roll clothes and pack one layer too many.","Carry a day bag with a refillable bottle.","Leave room for what you will buy."],
 "Documents":["Check passport validity and entry rules early.","Keep digital and paper copies of bookings.","Carry insurance details offline."],
 "Money":["Notify your bank and carry a backup card.","Withdraw local cash at an ATM, not an airport kiosk.","Tip as locals do, not as home habits dictate."],
 "Safety":["Share your itinerary with someone at home.","Keep valuables in more than one place.","Use licensed taxis or ride apps at night."]}
chapters = "".join('<details %s><summary><span>0%d</span><b class="serif">%s</b><i>+</i></summary><ul class="tick">%s</ul></details>'%("open" if i==0 else "",i+1,k,"".join("<li>%s</li>"%x for x in v)) for i,(k,v) in enumerate(tips.items()))
pack = ["Passport and visa or ETA","Phone charger and adapter","Reusable water bottle","Light rain jacket","Comfortable walking shoes","Travel insurance details","Small first-aid kit","Offline maps downloaded"]
cl = "".join('<li><label><input type="checkbox" data-ck="%d"> %s</label></li>'%(i,x) for i,x in enumerate(pack))
body = f'''<section class="tips-opening"><div><p class="eyebrow">THE CONSIDERED TRAVELLER / FIELD NOTES</p><h1 class="serif">A little more<br><em>prepared.</em></h1><p>Practical notes for a lighter, more thoughtful journey.</p></div>{ph("Ponte_Vecchio", alt="Ponte Vecchio crossing the Arno in Florence", label="Florence", cls="lead-photo")}</section>
<section class="wrap tips-index"><div id="tp-tabs"><p class="eyebrow">OPEN A CHAPTER / 01—04</p><div class="tip-chapters">{chapters}</div></div>
<aside class="box" id="tp-pack"><p class="eyebrow">YOUR TRAVEL COMPANION</p><h2 class="serif">Packing checklist</h2><ul class="cl">{cl}</ul><div class="prog"><span id="pk-bar"></span></div><p class="cap" id="pk-count"></p><button type="button" id="pk-reset" class="ghost">Reset list</button></aside></section>'''
layout("travel-tips.html","Travel tips","Packing, documents, money and safety tips with a checklist that saves as you tick.",body,"tips")

# ---------------------------------------------------------------- CULTURE (alternating rows)
C = [("Angkor_Wat","Angkor Wat, Cambodia","Go at dawn, dress to cover shoulders and knees, and hire a local guide."),
("Machu_Picchu","Machu Picchu, Peru","Book timed entry, stay on marked paths, and acclimatise in Cusco first."),
("Acropolis_of_Athens","The Acropolis, Greece","Visit late afternoon for softer light, and wear shoes with grip."),
("Taj_Mahal","Taj Mahal, India","Sunrise is best. Bring little, since bag rules are strict.")]
rows = "".join('<article class="culture-chapter" id="culture-%d">%s<div class="culture-caption"><span>CHAPTER 0%d / CULTURE & HERITAGE</span><h2 class="serif">%s</h2><p>%s</p>%s</div></article>'%(i+1,ph(w,alt=t,label=t),i+1,t,x,bm("culture.html",t)) for i,(w,t,x) in enumerate(C))
chapter_links = "".join('<a href="#culture-%d"><span>0%d</span> %s ↗</a>'%(i+1,i+1,t) for i,(_,t,_) in enumerate(C))
body = f'''<section class="culture-opening"><p class="eyebrow">THE CULTURE JOURNAL / 01—04</p><h1 class="serif">Places with<br><em>stories to tell.</em></h1><p>Great places last because visitors treat them well.</p><nav aria-label="Cultural chapters">{chapter_links}</nav></section>
<section class="culture-stories">{rows}</section><section class="wrap culture-end"><div class="box" id="cu-etiq"><h2 class="serif">Respect checklist</h2><ul class="tick"><li>Learn three words of the local language.</li><li>Ask before photographing people.</li><li>Cover up at religious sites.</li><li>Buy from local makers.</li></ul></div><a href="travel-tips.html" class="serif">Travel thoughtfully ↗</a></section>'''
layout("culture.html","Culture and heritage","Four landmark sites and how to visit them respectfully.",body,"culture")

# ---------------------------------------------------------------- FOOD (dark masonry + lightbox)
F = [("Mole","Mole poblano, Mexico","Chocolate, chilli and nuts, slow-cooked for hours."),("Sushi","Sushi, Japan","Rice, fish and restraint, ideally at a counter."),
("Tagine","Tagine, Morocco","Conical clay pots of spiced lamb or chicken."),("Paella","Paella, Spain","Saffron rice cooked over open flame in Valencia."),
("Ramen","Ramen, Japan","A late-night bowl with a story in every region."),("Gelato","Gelato, Italy","Dense, slow-churned and best eaten walking.")]
food_links = {"Mole":("",""),"Sushi":("kyoto.html","Explore Kyoto"),"Tagine":("marrakesh.html","Explore Marrakesh"),"Paella":("",""),"Ramen":("kyoto.html","Explore Kyoto"),"Gelato":("florence.html","Explore Florence")}
m = "".join('<figure class="mi" data-food="%s" data-cap="%s — %s" data-link="%s" data-link-title="%s" role="button" aria-label="Learn about %s">%s<figcaption><b>%s</b><span>%s</span></figcaption></figure>'%("sweet" if w=="Gelato" else "savoury",t,x,food_links[w][0],food_links[w][1],t,ph(w,alt=t+": "+x,label=t),t,x) for w,t,x in F)
body = f'''<section class="food-opening"><div><p class="eyebrow">THE FOOD JOURNAL / A TASTE OF PLACE</p><h1 class="serif">The world<br><em>at the table.</em></h1><p>Six dishes, six invitations to experience somewhere new.</p></div>{ph("Paella",alt="A pan of Valencian paella",label="Paella",cls="lead-photo")}</section>
<section class="food-gallery" id="fd-grid"><div class="food-heading"><div><p class="eyebrow">AN APPETITE FOR DISCOVERY</p><h2 class="serif">A taste of elsewhere.</h2></div><div class="food-filters" role="group" aria-label="Food category"><button data-food-filter="all" aria-pressed="true">All dishes</button><button data-food-filter="savoury" aria-pressed="false">Savoury</button><button data-food-filter="sweet" aria-pressed="false">Sweet</button></div></div>
<div class="story-carousel food-carousel" data-carousel><div class="story-rail food-rail" tabindex="0" aria-label="Food stories">{m}</div>{rail_controls()}</div><p class="food-hint">SELECT A DISH TO EXPLORE ITS STORY ↗</p></section>
<section class="next-story"><p class="eyebrow">GO BEYOND THE TABLE</p><a href="culture.html" class="serif">The stories behind the places <span>↗</span></a><p>Explore culture and heritage with care.</p></section>
<div class="lb" id="lb" hidden role="dialog" aria-modal="true" aria-label="Dish"><button type="button" id="lbx">Close</button><div id="lbi"></div><p id="lbc"></p><a id="lb-link" href="destinations.html"></a></div>'''
layout("food.html","Food and local experiences","Six dishes worth planning a trip around, with what to know before you go.",body,"food")

# ---------------------------------------------------------------- INSPIRATION
body = f'''<section class="inspire-opening"><div class="inspire-image one">{ph("Iceland",alt="Skógafoss waterfall in Iceland",label="Iceland")}</div><div class="inspire-copy"><p class="eyebrow">A LITTLE INSPIRATION / 01</p><h1 class="serif">Where will<br><em>curiosity</em><br>take you?</h1><p>Every great journey begins with a little wondering.</p><a href="#qz" class="text-link">FIND YOUR NEXT PLACE ↓</a></div><div class="inspire-image two">{ph("Florence",alt="Florence and the Arno from Piazzale Michelangelo",label="Florence")}</div></section>
<section class="inspire-work wrap"><div><p class="eyebrow">THREE QUESTIONS / ONE IDEA</p><h2 class="serif">Find your kind of elsewhere.</h2><div class="box" id="qz"></div></div><aside><div class="box" id="pollbox"><h2 class="serif">Poll: your ideal trip length?</h2><div id="poll"></div></div><div class="inspire-links"><p class="eyebrow">STORIES TO DREAM ABOUT</p><a href="lofoten.html">01 / Arctic light <span>↗</span></a><a href="cinque-terre.html">02 / The Italian coast <span>↗</span></a><a href="florence.html">03 / City of art <span>↗</span></a></div></aside></section>'''
layout("inspiration.html","Inspiration quiz","Answer three questions and get a destination idea.",body,"inspire")

# ---------------------------------------------------------------- ABOUT / CONTACT / SAVED / CREDITS / 404
layout("about.html","About","Meridian is an independent worldwide travel journal.",f'''{crumbs((None,"About"))}
<section class="about-opening"><div class="about-introduction"><p class="eyebrow">HELLO, FELLOW TRAVELLER <span aria-hidden="true">✳</span></p><h1 class="serif">A little more<br><em>about Meridian.</em></h1><p class="about-lede">We write short, useful guides to places we would go back to.</p><p>Meridian is an independent travel journal for curious minds and considered journeys. We share what we learn, so you can plan with confidence.</p><a class="about-link" href="destinations.html">COME EXPLORE WITH US <span aria-hidden="true">↗</span></a></div>
<div class="about-photo"><div class="about-photo-frame">{ph("Lisbon_Alfama",alt="View over Lisbon's Alfama neighbourhood toward the Tagus River",label="Lisbon",cls="lead-photo")}<p>POSTCARD FROM LISBON <span>PORTUGAL / 01</span></p></div><div class="about-photo-stamp" aria-hidden="true">FOR THE<br><span>curious</span><br>TRAVELLER ✳</div></div></section>
<section class="about-discover wrap"><div class="about-section-heading"><p class="eyebrow">A WORLD OF STORIES / 01</p><h2 class="serif">A little something<br><em>for every journey.</em></h2><p>From the first spark of an idea to the details that bring it to life.</p></div><nav class="about-index" aria-label="Explore the journal"><a href="destinations.html"><span>01</span><b class="serif">Destination guides</b><i>Places worth getting to know</i><strong aria-hidden="true">↗</strong></a><a href="travel-tips.html"><span>02</span><b class="serif">Travel tips</b><i>Thoughtful notes for the road</i><strong aria-hidden="true">↗</strong></a><a href="culture.html"><span>03</span><b class="serif">Culture &amp; heritage</b><i>Stories that connect us to a place</i><strong aria-hidden="true">↗</strong></a><a href="food.html"><span>04</span><b class="serif">Food &amp; local experiences</b><i>A taste of somewhere new</i><strong aria-hidden="true">↗</strong></a><a href="inspiration.html"><span>05</span><b class="serif">Inspiration</b><i>Find your next spark of an idea</i><strong aria-hidden="true">↗</strong></a></nav></section>
<section class="about-notes"><div class="about-notes-heading"><p class="eyebrow">OUR APPROACH / 02</p><h2 class="serif">A more thoughtful<br><em>way to wander.</em></h2><span aria-hidden="true">✳</span></div><div class="about-values"><article><span>01</span><div><h3 class="serif">Stay curious</h3><p>Look beyond the familiar and leave room for discovery.</p></div></article><article><span>02</span><div><h3 class="serif">Travel with care</h3><p>Respect local communities, cultures and the places you visit.</p></div></article><article><span>03</span><div><h3 class="serif">Make it your own</h3><p>Use our guides as a starting point for a journey that feels like yours.</p></div></article></div></section>
<section class="about-invitation"><p class="eyebrow">WHERE TO NEXT?</p><h2 class="serif">The world is waiting.<br><em>Let's wander.</em></h2><div><a href="destinations.html">EXPLORE DESTINATIONS ↗</a><a href="contact.html">SAY HELLO ↗</a><a href="credits.html">IMAGE SOURCES &amp; LICENCES ↗</a></div></section>''',"about")
layout("contact.html","Contact","Send the Meridian team a note.",f'''{crumbs((None,"Contact"))}<section class="wrap narrow"><h1 class="serif big">Contact</h1>
<form class="box ct" id="ctf" novalidate><label>Name<input id="cn" required></label><label>Email<input id="ce" type="email" required></label><label>Message<textarea id="cm" rows="5" required></textarea></label>
<button class="btn">Send message</button><p class="msg" role="status"></p></form></section>''',"contact")
layout("saved.html","Saved guides","Your bookmarked guides.",f'''{crumbs((None,"Saved"))}<section class="wrap narrow"><h1 class="serif big">Saved guides</h1><ul class="guides" id="sv"></ul><p class="empty" id="sv-e" hidden>Nothing saved yet. Tap ♡ on any guide to keep it here.</p></section>''',"saved")
credit = [("Reine at Reinefjorden, 2010 September.jpg","Home hero and Lofoten card","Wikimedia Commons file; CC BY-SA 3.0"),("Reine Lofoten 2009.JPG","Lofoten","Petr Šmerkl (Sveter); CC BY-SA 3.0"),
("Lofoten, Norway (Unsplash).jpg","Lofoten aurora","followhansi; CC0"),("0688 Norway Lofoten bridge between Sakrisoya and Andoya.jpg","Lofoten bridge","Wikimedia Commons featured picture; check file page licence")]
cr = "".join("<li><b>%s</b> — %s. <i>%s</i></li>"%(a,b,c) for a,b,c in credit)
photo_links = "".join('<li><a href="https://commons.wikimedia.org/wiki/File:%s">%s</a> — %s</li>' % (quote(filename), filename, name.replace("_", " ")) for name,filename in PHOTO_FILES.items() if name != "Lisbon_Alfama")
photo_links += '<li><a href="https://commons.wikimedia.org/wiki/File:%s">View across Alfama from the Miradouro de Santa Luzia 01</a> — Simon Burchell, <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>; cropped for the About page.</li>' % quote(PHOTO_FILES["Lisbon_Alfama"])
layout("credits.html","Photo credits","Image sources and licences.",f'''{crumbs((None,"Photo credits"))}<section class="wrap narrow"><h1 class="serif big">Photo credits</h1>
<p>Photographs come from Wikimedia Commons. The file links below lead to the author and licence information; please check the individual licence before reuse. Other photographs are the lead images of the named Wikipedia articles, where their Commons file pages provide attribution and licence details.</p><ul class="tick">{cr}
{photo_links}</ul></section>''',"credits")
layout("404.html","Page not found","This page does not exist.",'<section class="wrap narrow"><h1 class="serif big">Lost the trail</h1><p class="lede">That page is not here. Try the <a href="destinations.html">destinations</a> or go <a href="index.html">home</a>.</p></section>',"nf")

# ---------------------------------------------------------------- sitemap / robots / assets
open(OUT+"/sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join("<url><loc>%s/%s</loc></url>"%(SITE,p[0]) for p in PAGES)+"</urlset>")
open(OUT+"/robots.txt","w").write("User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n"%SITE)
js = open(os.path.join(SOURCE,"app.js"), encoding="utf-8").read().replace("/*PAGES*/", json.dumps([{"h":h,"t":t,"d":d} for h,t,d in PAGES]))
open(OUT+"/assets/app.js","w",encoding="utf-8").write(js); open(OUT+"/assets/style.css","w",encoding="utf-8").write(open(os.path.join(SOURCE,"style.css"),encoding="utf-8").read())
print("ok")
