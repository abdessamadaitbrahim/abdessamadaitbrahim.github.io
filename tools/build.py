"""Static site generator for the portfolio.

Run from the repository root:  python tools/build.py
Reads tools/content.json and writes every HTML page, 404.html, sitemap.xml,
robots.txt. Icons come from tools/make_icons.py. All internal links are relative so the site works
on GitHub Pages; only 404.html uses root-absolute links (it is served at any path).
"""
import json
from datetime import date
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = json.loads((ROOT / "tools" / "content.json").read_text(encoding="utf-8"))
SITE, PROJECTS, HACKS = D["site"], D["projects"], D["hackathons"]
URL = SITE["url"]
TODAY = date.today().isoformat()
NAME = SITE["name"]
CV_EXISTS = (ROOT / SITE["cv"]).exists()

CATS = [("all", "All"), ("nlp", "NLP"), ("vision", "Computer Vision"), ("dl", "Deep Learning"),
        ("ml", "Machine Learning"), ("bigdata", "Big Data"), ("embedded", "Embedded & IoT"),
        ("bi", "Data & BI"), ("foundations", "Foundations")]
CAT_LABEL = dict(CATS)
INITIAL = 8  # cards shown on projects.html before "Show all"

# key, label, file, one-line description (used by the home index and the footer)
PAGES = [
 ("index", "Home", "index.html", "Introduction and highlights."),
 ("about", "About", "about.html", "Profile, interests, skills and languages."),
 ("projects", "Projects", "projects.html", f"{len(PROJECTS)} projects in AI, NLP, vision, Big Data and BI, each with a case study."),
 ("education", "Education", "education.html", "Engineering degree in Big Data and AI at ENSA Tétouan."),
 ("experience", "Experience", "experience.html", "AI engineering internships and teaching."),
 ("hackathons", "Hackathons", "hackathons.html", "Water4Future, Game4Health and MECA WORLD CUP, 2026."),
 ("volunteering", "Volunteering", "volunteering.html", "Erasmus+ youth exchange and cultural engagement."),
 ("honors", "Honors", "honors.html", "Semi-finalist, finalist and prize, 2026."),
 ("cv", "CV", "cv.html", "Download the résumé as a PDF."),
 ("contact", "Contact", "contact.html", "Email, LinkedIn and GitHub."),
]
PAGE = {k: (lbl, f, d) for k, lbl, f, d in PAGES}
MAIN_NAV = ["index", "about", "projects", "education", "experience", "hackathons"]
MORE_NAV = ["volunteering", "honors", "cv", "contact"]

ICON = {
 "github": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 .5C5.65.5.5 5.65.5 12c0 5.08 3.29 9.39 7.86 10.91.58.1.79-.25.79-.56v-2c-3.2.7-3.87-1.37-3.87-1.37-.52-1.33-1.28-1.69-1.28-1.69-1.04-.71.08-.7.08-.7 1.15.08 1.76 1.18 1.76 1.18 1.03 1.76 2.69 1.25 3.35.96.1-.74.4-1.25.73-1.54-2.55-.29-5.24-1.28-5.24-5.68 0-1.25.45-2.28 1.18-3.08-.12-.29-.51-1.46.11-3.05 0 0 .97-.31 3.17 1.18a11 11 0 0 1 5.78 0c2.2-1.49 3.17-1.18 3.17-1.18.62 1.59.23 2.76.11 3.05.74.8 1.18 1.83 1.18 3.08 0 4.41-2.69 5.38-5.25 5.67.41.36.78 1.06.78 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 23.5 12C23.5 5.65 18.35.5 12 .5Z"/></svg>',
 "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.03-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.34V9h3.42v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28ZM5.34 7.43a2.07 2.07 0 1 1 0-4.14 2.07 2.07 0 0 1 0 4.14ZM7.12 20.45H3.56V9h3.56v11.45ZM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0Z"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
 "download": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m0 0 4-4m-4 4-4-4M4 19h16"/></svg>',
 "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>',
 "ext": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg>',
 "file": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8l-5-5Z"/><path d="M14 3v5h5M9 13h6M9 17h6"/></svg>',
 "image": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="1"/><circle cx="9" cy="10" r="2"/><path d="m21 17-5-5-9 8"/></svg>',
 "copy": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="11" height="11" rx="1"/><path d="M5 15V5a1 1 0 0 1 1-1h10"/></svg>',
 "chev": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>',
 "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M4 8h16M4 16h16"/></svg>',
}

JS_FLAG = '<script>document.documentElement.classList.add("js")</script>'


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


def crumbs_ld(items):
    """items: list of (name, absolute url)."""
    return ld({"@context": "https://schema.org", "@type": "BreadcrumbList",
               "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]})


# --------------------------------------------------------------------------- shell
def head(title, desc, path, p, extra=""):
    canon = URL + "/" + ("" if path == "index.html" else path)
    og = URL + "/assets/img/site/og.png"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="author" content="{NAME}">
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#f4eee3">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{NAME}, AI and Big Data engineering student">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{p}favicon.ico" sizes="any">
<link rel="icon" href="{p}assets/img/site/favicon-32.png" type="image/png" sizes="32x32">
<link rel="manifest" href="{p}site.webmanifest">
<link rel="apple-touch-icon" href="{p}assets/img/site/apple-touch-icon.png">
<link rel="preload" href="{p}assets/fonts/fraunces-latin-opsz-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{p}assets/fonts/inter-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
{JS_FLAG}
<link rel="stylesheet" href="{p}assets/css/style.css">
{extra}
</head>'''


def header(p, current):
    def link(k):
        lbl, f, _ = PAGE[k]
        cur = ' aria-current="page"' if k == current else ""
        return f'<a href="{p}{f}"{cur}>{lbl}</a>'
    main = "".join(link(k) for k in MAIN_NAV)
    more_cur = " is-current" if current in MORE_NAV else ""
    more = "".join(link(k) for k in MORE_NAV)
    return f'''<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
<div class="container">
<a class="brand" href="{p}index.html" aria-label="{NAME}, home"><img class="brand__mark" src="{p}assets/img/site/avatar.webp" alt="" width="96" height="96"><span class="brand__name">Abdessamad <em>Ait Brahim</em></span></a>
<nav class="nav" id="nav" aria-label="Main">
{main}
<div class="nav__more{more_cur}">
<button class="nav__more-btn" type="button" aria-expanded="false" aria-controls="more-menu">More {ICON['chev']}</button>
<div class="nav__menu" id="more-menu"><span class="nav__label">More</span>{more}</div>
</div>
</nav>
<div class="tools">
<button class="icon-btn menu-btn" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="nav">{ICON['menu']}</button>
</div>
</div>
</header>
<main id="main">'''


def footer(p):
    links = "".join(f'<li><a href="{p}{f}">{lbl}</a></li>' for k, lbl, f, _ in PAGES)
    return f'''</main>
<footer class="site-footer">
<div class="container">
<div class="foot__brand">
<p class="foot__name">Abdessamad <em>Ait Brahim</em></p>
<p>Big Data and AI engineering student, ENSA Tétouan. Open to a 6-month PFE internship from January 2027.</p>
</div>
<nav class="foot__nav foot__nav--pages" aria-label="Site"><p class="eyebrow">Pages</p><ul>{links}</ul></nav>
<div class="foot__nav"><p class="eyebrow">Elsewhere</p><ul>
<li><a href="{SITE['github']}" rel="me noopener">GitHub</a></li>
<li><a href="{SITE['linkedin']}" rel="me noopener">LinkedIn</a></li>
<li class="foot__mail"><a href="{p}contact.html#email" data-email data-user="{SITE['email_user']}" data-domain="{SITE['email_domain']}">Email</a><button class="copy copy--sm" type="button" data-copy-email data-user="{SITE['email_user']}" data-domain="{SITE['email_domain']}" aria-label="Copy email address" hidden>{ICON['copy']}<span>Copy</span></button><span class="sr-only" role="status" aria-live="polite" data-copy-status></span></li>
</ul></div>
<div class="foot__base"><span>&copy; 2026 {NAME}</span><span class="foot__motto">{e(D["about"]["quote"])}</span><a href="#top">Back to top &uarr;</a></div>
</div>
</footer>
<script src="{p}assets/js/main.js" defer></script>
</body>
</html>
'''


def intro(eyebrow, title, lead="", crumb="", extra=""):
    c = f'<nav class="crumb" aria-label="Breadcrumb">{crumb}</nav>' if crumb else ""
    l = f'<p class="lead">{lead}</p>' if lead else ""
    return f'''<div id="top"></div>
<header class="intro">
<div class="container">
{c}
<p class="eyebrow">{eyebrow}</p>
<h1>{title}</h1>
{l}
{extra}
</div>
</header>'''


def crumb_home(p, label):
    return f'<a href="{p}index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">{e(label)}</span>'


def with_toc(items, body):
    """items: list of (id, label). Long pages get a sticky 'On this page' column."""
    toc = "".join(f'<li><a href="#{i}" data-spy>{e(l)}</a></li>' for i, l in items)
    return f'''<div class="container layout">
<aside class="toc" aria-label="On this page"><p class="toc__title">On this page</p><ol>{toc}</ol></aside>
<div class="content">
{body}
</div>
</div>'''


def block(id_, num, label, title, body, cls=""):
    return f'''<section class="block {cls}" id="{id_}" aria-labelledby="{id_}-h">
<div class="block__head reveal"><p class="eyebrow"><span class="num">{num}</span>{label}</p><h2 id="{id_}-h">{title}</h2></div>
{body}
</section>'''


def pager(prev, nxt, back=None):
    """prev/nxt: (href, small, title) or None."""
    out = []
    if prev:
        out.append(f'<a class="pager__prev" href="{prev[0]}"><small>&larr; {prev[1]}</small><b>{e(prev[2])}</b></a>')
    else:
        out.append("<span></span>")
    if nxt:
        out.append(f'<a class="pager__next" href="{nxt[0]}"><small>{nxt[1]} &rarr;</small><b>{e(nxt[2])}</b></a>')
    b = f'<p class="pager__back"><a href="{back[0]}">{back[1]}</a></p>' if back else ""
    return f'<nav class="container pager" aria-label="Pages">{"".join(out)}</nav>{b}'


def seq_pager(key, p=""):
    keys = [k for k, *_ in PAGES]
    i = keys.index(key)
    prev = (p + PAGE[keys[i - 1]][1], "Previous", PAGE[keys[i - 1]][0]) if i > 0 else None
    nxt = (p + PAGE[keys[i + 1]][1], "Next", PAGE[keys[i + 1]][0]) if i + 1 < len(keys) else None
    return pager(prev, nxt)


def img(src, alt, w, h, p, lazy=True, cls="", sizes=""):
    """src is relative to assets/."""
    extra = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return f'<img src="{p}assets/{src}" alt="{e(alt)}" width="{w}" height="{h}"{extra}{c}>'


def pimg(key, alt, w, h, p, lazy=True):
    return img(f"img/projects/{key}.webp", alt, w, h, p, lazy)


def chips(items, n=None):
    items = items[:n] if n else items
    return '<ul class="chips">' + "".join(f'<li class="chip">{e(s)}</li>' for s in items) + "</ul>"


def write(path, html):
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")


# --------------------------------------------------------------------------- shared pieces
def card(pr, i, p, compact=False):
    cats = " ".join(pr["cats"])
    label = " · ".join(CAT_LABEL[c] for c in pr["cats"])
    href = f'{p}projects/{pr["slug"]}.html'
    if pr.get("cover"):
        cls = "card__media card__media--contain" if pr.get("cover_fit") == "contain" else "card__media"
        media = f'<a class="{cls}" href="{href}" tabindex="-1" aria-hidden="true">{pimg(pr["cover"], "", pr["cover_w"], pr["cover_h"], p)}</a>'
    else:
        media = f'<a class="card__media" href="{href}" tabindex="-1" aria-hidden="true"><span class="ph">{e(pr.get("label", pr["title"]))}</span></a>'
    extra = " is-extra" if (not compact and i >= INITIAL) else ""
    links = f'<a href="{href}">Case study {ICON["arrow"]}</a><a href="{pr["repo"]}" rel="noopener">Code {ICON["ext"]}</a>'
    if pr.get("demo"):
        links += f'<a href="{pr["demo"]}" rel="noopener">Live demo {ICON["ext"]}</a>'
    return f'''<article class="card reveal{extra}" data-cats="{cats}">
{media}
<div class="card__body">
<p class="card__cats">{"" if compact else f'<span class="num">{i + 1:02d}</span>'}{e(label)}</p>
<h3><a href="{href}">{e(pr["title"])}</a></h3>
<p>{e(pr["short"])}</p>
{chips(pr["stack"], 4)}
<div class="card__links">{links}</div>
</div>
</article>'''


def portrait(p):
    return f'''<figure class="portrait reveal">
<div class="portrait__disc">{img("img/site/portrait.webp", "Portrait of Abdessamad Ait Brahim", 600, 639, p, lazy=False)}</div>
</figure>'''


def facts_dl(rows, cls="facts"):
    return f'<dl class="{cls}">' + "".join(f'<div class="fact"><dt>{e(a)}</dt><dd>{b}</dd></div>' for a, b in rows if b) + "</dl>"


def ul(items):
    return "<ul class=\"list\">" + "".join(f"<li>{e(x)}</li>" for x in items) + "</ul>" if items else ""


# --------------------------------------------------------------------------- home
def page_index():
    p = ""
    a = D["about"]
    featured = [pr for pr in PROJECTS if pr["featured"]][:4]
    cards = "\n".join(card(pr, PROJECTS.index(pr), p, compact=True) for pr in featured)
    latest = HACKS[-1]
    li = latest["images"][0]
    explore = "".join(
        f'<li class="reveal"><a href="{f}"><span class="num">{i:02d}</span><b>{lbl}</b><span class="desc">{e(d)}</span>{ICON["arrow"]}</a></li>'
        for i, (k, lbl, f, d) in enumerate(PAGES[1:], start=1))
    others = ", ".join(f'<a href="hackathons/{h["slug"]}.html">{e(h["short"])}</a>' for h in HACKS[:-1])
    desc = "Final-year Big Data and AI engineering student at ENSA Tétouan. NLP, computer vision, deep learning and Big Data projects. Open to a 6-month PFE internship starting January 2027."
    person = {"@context": "https://schema.org", "@type": "Person", "name": NAME, "url": URL + "/",
              "image": URL + "/assets/img/site/portrait.webp",
              "jobTitle": "Big Data and Artificial Intelligence engineering student",
              "alumniOf": {"@type": "CollegeOrUniversity", "name": "ENSA Tétouan, Abdelmalek Essaâdi University"},
              "knowsAbout": ["Machine learning", "Deep learning", "Computer vision", "Natural language processing", "Big Data"],
              "knowsLanguage": [l[0] for l in D["languages"]],
              "award": [f'{h["title"]}, {h["event"]}' for h in D["honors"]],
              "sameAs": [SITE["github"], SITE["linkedin"]]}
    site = {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": URL + "/"}
    cv_btn = f'<a class="btn" href="{SITE["cv"]}" download>{ICON["download"]} Download CV</a>' if CV_EXISTS else f'<a class="btn" href="cv.html">CV</a>'
    return head(f"{NAME} | AI and Big Data Engineering Student", desc, "index.html", p, ld(person) + "\n" + ld(site)) + header(p, "index") + f'''
<div id="top"></div>
<section class="hero" aria-label="Introduction">
<canvas id="hero-canvas" aria-hidden="true"></canvas>
<div class="container hero__grid">
<div class="hero__text">
<p class="eyebrow reveal">ENSA Tétouan &middot; Big Data &amp; AI engineering &middot; Class of 2027</p>
<h1 class="reveal">Abdessamad <em>Ait&nbsp;Brahim</em></h1>
<p class="lead reveal">Final-year engineering student building reliable, data-driven AI systems: natural language processing, computer vision and Big Data.</p>
<p class="status reveal"><i aria-hidden="true"></i>Open to a 6-month PFE internship starting January 2027</p>
<div class="actions reveal">
<a class="btn btn--primary" href="projects.html">View projects {ICON['arrow']}</a>
{cv_btn}
<a class="btn btn--ghost" href="contact.html">{ICON['mail']} Contact</a>
</div>
</div>
{portrait(p)}
</div>
</section>

<div class="container home">
<section class="block" id="about" aria-labelledby="about-h">
<div class="block__head reveal"><p class="eyebrow"><span class="num">01</span>About</p><h2 id="about-h">Rigorous experiments, reliable systems</h2></div>
<div class="split">
<div class="reveal">
<p class="big">{e(a["short"])}</p>
<blockquote class="quote"><p>{e(a["quote"])}</p><cite>Abdessamad</cite></blockquote>
<p><a class="more-link" href="about.html">More about me {ICON['arrow']}</a></p>
</div>
{facts_dl([(x, e(y)) for x, y in a["facts"]], "facts facts--stack reveal")}
</div>
</section>

<section class="block" id="work" aria-labelledby="work-h">
<div class="block__head reveal"><p class="eyebrow"><span class="num">02</span>Selected projects</p><h2 id="work-h">Four projects to start with</h2></div>
<div class="grid grid--4">
{cards}
</div>
<p class="center"><a class="btn" href="projects.html">All {len(PROJECTS)} projects {ICON['arrow']}</a></p>
</section>

<section class="block" id="latest" aria-labelledby="latest-h">
<div class="block__head reveal"><p class="eyebrow"><span class="num">03</span>Latest hackathon</p><h2 id="latest-h">{e(latest["title"])}</h2></div>
<article class="teaser reveal">
<a class="teaser__media" href="hackathons/{latest['slug']}.html" tabindex="-1" aria-hidden="true">{img(li["src"], "", li["w"], li["h"], p)}</a>
<div class="teaser__body">
<p class="meta">{e(latest["date"])} &middot; {e(latest["org"])}</p>
<p>{e(latest["summary"])}</p>
<p class="tag">{e(latest["result"])}</p>
<p><a class="more-link" href="hackathons/{latest['slug']}.html">Read about it {ICON['arrow']}</a></p>
<p class="small">Also in 2026: {others}.</p>
</div>
</article>
</section>

<section class="block" id="explore" aria-labelledby="explore-h">
<div class="block__head reveal"><p class="eyebrow"><span class="num">04</span>Explore</p><h2 id="explore-h">Everything on this site</h2></div>
<ol class="index">{explore}</ol>
</section>
</div>
''' + footer(p)


# --------------------------------------------------------------------------- about
def page_about():
    p = ""
    a = D["about"]
    paras = "".join(f"<p>{e(x)}</p>" for x in a["paragraphs"])
    interests = "".join(f'<div class="interest reveal"><b>{e(t)}</b><span>{e(s)}</span></div>' for t, s in D["interests"])
    skills = "".join(f'<div class="skill reveal"><h3>{e(t)}</h3>{chips(items)}</div>' for t, items in D["skills"])
    langs = "".join(
        f'<li class="lang reveal"><b>{e(n)}</b><span class="lvl">{e(l)}</span><span class="dots" aria-hidden="true">' + "".join(f'<i class="{"on" if j < v else ""}"></i>' for j in range(5)) + "</span></li>"
        for n, l, v in D["languages"])
    body = (block("profile", "01", "Profile", "Rigorous experiments, reliable systems",
                  f'<div class="prose reveal">{paras}</div><blockquote class="quote reveal"><p>{e(a["quote"])}</p><cite>Abdessamad</cite></blockquote>{facts_dl([(x, e(y)) for x, y in a["facts"]], "facts reveal")}')
            + block("interests", "02", "Interests", "What I like to work on", f'<div class="interests">{interests}</div>')
            + block("skills", "03", "Skills", "Tools I work with", f'<div class="skills">{skills}</div>')
            + block("languages", "04", "Languages", "Five languages", f'<ul class="langs">{langs}</ul><p class="note">Levels as listed on my LinkedIn profile.</p>'))
    toc = [("profile", "Profile"), ("interests", "Interests"), ("skills", "Skills"), ("languages", "Languages")]
    desc = "About Abdessamad Ait Brahim: profile, research interests, technical skills and languages."
    return (head(f"About | {NAME}", desc, "about.html", p, crumbs_ld([("Home", URL + "/"), ("About", URL + "/about.html")]))
            + header(p, "about")
            + intro("About", "A data-minded engineer in training", e(a["short"]), crumb_home(p, "About"))
            + with_toc(toc, body) + seq_pager("about") + footer(p))


# --------------------------------------------------------------------------- projects
def page_projects():
    p = ""
    counts = {c: sum(1 for x in PROJECTS if c in x["cats"]) for c, _ in CATS if c != "all"}
    counts["all"] = len(PROJECTS)
    filters = "".join(
        f'<button class="filter" type="button" data-filter="{c}" aria-pressed="{"true" if c == "all" else "false"}">{l}<span class="n">{counts[c]}</span></button>'
        for c, l in CATS if counts[c])
    cards = "\n".join(card(pr, i, p) for i, pr in enumerate(PROJECTS))
    desc = f"{len(PROJECTS)} projects by Abdessamad Ait Brahim in NLP, computer vision, deep learning, machine learning, Big Data and BI, each with a case study."
    items = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": f'{URL}/projects/{pr["slug"]}.html', "name": pr["title"]} for i, pr in enumerate(PROJECTS)]}
    return (head(f"Projects | {NAME}", desc, "projects.html", p, crumbs_ld([("Home", URL + "/"), ("Projects", URL + "/projects.html")]) + "\n" + ld(items))
            + header(p, "projects")
            + intro("Projects", "Selected work", "AI, machine learning and NLP projects come first. Every card opens a case study; code is on GitHub.", crumb_home(p, "Projects"))
            + f'''<div class="container wide">
<div class="filters reveal" role="group" aria-label="Filter projects">{filters}</div>
<p class="sr-only" id="filter-status" role="status" aria-live="polite"></p>
<div class="grid grid--3" id="project-grid">
{cards}
</div>
<div class="more"><button class="btn" type="button" id="show-more">Show all {len(PROJECTS)} projects</button></div>
</div>''' + seq_pager("projects") + footer(p))


def page_project(i):
    pr = PROJECTS[i]
    p = "../"
    prev = PROJECTS[i - 1]
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    label = " · ".join(CAT_LABEL[c] for c in pr["cats"])
    gal = pr["gallery"]
    cover = ""
    if gal:
        g = gal[0]
        cls = "cover cover--contain" if pr.get("cover_fit") == "contain" or g["img"] != pr.get("cover") else "cover"
        cover = f'<figure class="{cls}">{pimg(g["img"], g["alt"], g["w"], g["h"], p, lazy=False)}<figcaption>{e(g["caption"])}</figcaption></figure>'
    links = f'<a class="btn btn--primary" href="{pr["repo"]}" rel="noopener">{ICON["github"]} Code on GitHub</a>'
    if pr.get("demo"):
        links += f'<a class="btn" href="{pr["demo"]}" rel="noopener">Live demo {ICON["ext"]}</a>'
    related = []
    if pr.get("hackathon"):
        h = next(x for x in HACKS if x["slug"] == pr["hackathon"])
        related.append(f'<a href="../hackathons/{h["slug"]}.html">{e(h["title"])}</a>')
    if pr.get("experience"):
        x = next(x for x in D["experience"] if x["id"] == pr["experience"])
        related.append(f'<a href="../experience.html#{x["id"]}">{e(x["org"])} internship</a>')
    rows = [("Context", e(pr.get("context", ""))), ("Area", e(label)), ("Stack", chips(pr["stack"])),
            ("Related", " &middot; ".join(related))]
    sections, toc = [], []

    def sec(id_, title, body):
        n = f"{len(sections) + 1:02d}"
        sections.append(block(id_, n, title, title, body))
        toc.append((id_, title))

    sec("overview", "Overview", f'{facts_dl(rows, "facts facts--table reveal")}<div class="actions reveal">{links}</div>')
    if pr.get("problem"):
        sec("problem", "The problem", f'<div class="prose reveal"><p>{e(pr["problem"])}</p></div>')
    if pr.get("built"):
        sec("built", "What I built", f'<div class="prose reveal">{ul(pr["built"])}</div>')
    if pr["results"]:
        title = "Results" if pr["slug"] not in ("numerical-linear-algebra", "cryptography", "scout-ai") else "Results and limits"
        sec("results", title, f'<div class="prose reveal">{ul(pr["results"])}</div>')
    if len(gal) > 1:
        figs = "".join(f'<figure class="reveal"><a href="{p}assets/img/projects/{x["img"]}.webp">{pimg(x["img"], x["alt"], x["w"], x["h"], p)}</a><figcaption>{e(x["caption"])}</figcaption></figure>' for x in gal[1:])
        sec("gallery", "Gallery", f'<div class="gallery">{figs}</div>')
    desc = pr["short"]
    code = {"@context": "https://schema.org", "@type": "SoftwareSourceCode", "name": pr["title"], "description": desc,
            "author": {"@type": "Person", "name": NAME, "url": URL + "/"}, "codeRepository": pr["repo"],
            "keywords": ", ".join(pr["stack"]), "url": f'{URL}/projects/{pr["slug"]}.html'}
    if gal:
        code["image"] = f'{URL}/assets/img/projects/{gal[0]["img"]}.webp'
    crumb = f'<a href="../index.html">Home</a><span aria-hidden="true">/</span><a href="../projects.html">Projects</a><span aria-hidden="true">/</span><span aria-current="page">{e(pr["title"])}</span>'
    return (head(f'{pr["title"]} | {NAME}', desc, f'projects/{pr["slug"]}.html', p,
                 ld(code) + "\n" + crumbs_ld([("Home", URL + "/"), ("Projects", URL + "/projects.html"), (pr["title"], f'{URL}/projects/{pr["slug"]}.html')]))
            + header(p, "projects")
            + intro(f'Case study {i + 1:02d} / {len(PROJECTS)} &middot; {e(label)}', e(pr["title"]), e(pr["short"]), crumb,
                    f'<div class="intro__cover">{cover}</div>' if cover else "")
            + with_toc(toc, "".join(sections))
            + pager((f'{prev["slug"]}.html', "Previous", prev["title"]), (f'{nxt["slug"]}.html', "Next", nxt["title"]), ("../projects.html", "&larr; All projects"))
            + footer(p))


# --------------------------------------------------------------------------- education / experience
def entry(id_, dates, title, org, body, extra=""):
    return f'''<article class="entry reveal" id="{id_}">
<div class="entry__when"><span>{dates}</span></div>
<div class="entry__body">
<h2 class="entry__title">{title}</h2>
<p class="entry__org">{org}</p>
{body}
{extra}
</div>
</article>'''


def page_education():
    p = ""
    out, toc = [], []
    for x in D["education"]:
        lg = x.get("logo")
        logo = img(lg["src"], lg["alt"], lg["w"], lg["h"], p, cls="logo") if lg and (ROOT / "assets" / lg["src"]).exists() else ""
        body = (f'<p>{e(x["detail"])}</p>' if x["detail"] else "") + chips(x["skills"])
        out.append(entry(x["id"], e(x["dates"]), e(x["degree"]), e(x["school"]), body, logo))
        toc.append((x["id"], x["degree"].split(",")[0].replace("Two-year integrated preparatory programme", "Preparatory programme").replace("Engineering cycle in Big Data and Artificial Intelligence", "Engineering cycle")))
    desc = "Education of Abdessamad Ait Brahim: engineering cycle in Big Data and AI at ENSA Tétouan, integrated preparatory programme and scientific baccalaureate."
    return (head(f"Education | {NAME}", desc, "education.html", p, crumbs_ld([("Home", URL + "/"), ("Education", URL + "/education.html")]))
            + header(p, "education")
            + intro("Education", "From the baccalaureate to Big Data and AI", "Five years at ENSA Tétouan, Abdelmalek Essaâdi University: two integrated preparatory years, then the engineering cycle in Big Data and Artificial Intelligence.", crumb_home(p, "Education"))
            + with_toc(toc, f'<div class="entries">{"".join(out)}</div>') + seq_pager("education") + footer(p))


def page_experience():
    p = ""
    out, toc = [], []
    for x in D["experience"]:
        body = f'<p class="entry__lead">{e(x["summary"])}</p>{ul(x["points"])}{chips(x["skills"])}'
        extra = ""
        if x.get("project"):
            pr = next(q for q in PROJECTS if q["slug"] == x["project"])
            extra = f'<p><a class="more-link" href="projects/{pr["slug"]}.html">Read the {e(pr["title"].split(":")[0])} case study {ICON["arrow"]}</a></p>'
        if x.get("note"):
            extra += f'<p class="note">{e(x["note"])}</p>'
        when = f'{e(x["dates"])}<small>{e(x["length"])} &middot; {e(x["kind"])}</small>'
        out.append(entry(x["id"], when, e(x["role"]), f'{e(x["org"])} &middot; {e(x["place"])}', body, extra))
        toc.append((x["id"], x["org"]))
    desc = "Experience of Abdessamad Ait Brahim: AI engineering internships at STMicroelectronics, Labex (Botground) and Cloud Marketing Hub, and mathematics tutoring."
    return (head(f"Experience | {NAME}", desc, "experience.html", p, crumbs_ld([("Home", URL + "/"), ("Experience", URL + "/experience.html")]))
            + header(p, "experience")
            + intro("Experience", "Internships and teaching", "Three AI engineering internships, from NLP and recommendation to LLM agents on industrial data, and a semester of mathematics tutoring.", crumb_home(p, "Experience"))
            + with_toc(toc, f'<div class="entries">{"".join(out)}</div>') + seq_pager("experience") + footer(p))


# --------------------------------------------------------------------------- hackathons
def hack_card(h, p):
    im = h["images"][0]
    return f'''<article class="hcard reveal" id="{h["slug"]}">
<a class="hcard__media" href="{p}hackathons/{h["slug"]}.html" tabindex="-1" aria-hidden="true">{img(im["src"], "", im["w"], im["h"], p)}</a>
<div class="hcard__body">
<p class="meta">{e(h["date"])}{(" &middot; " + e(h["place"])) if h["place"] else ""}</p>
<h2><a href="{p}hackathons/{h["slug"]}.html">{e(h["title"])}</a></h2>
<p class="tag">{e(h["result"])}</p>
<p>{e(h["summary"])}</p>
<p><a class="more-link" href="{p}hackathons/{h["slug"]}.html">Full story {ICON["arrow"]}</a></p>
</div>
</article>'''


def page_hackathons():
    p = ""
    hs = list(reversed(HACKS))  # most recent first
    cards = "".join(hack_card(h, p) for h in hs)
    toc = [(h["slug"], h["short"]) for h in hs]
    desc = "Hackathons and competitions of Abdessamad Ait Brahim in 2026: Water4Future (Montpellier), Game4Health (Rabat) and MECA WORLD CUP."
    return (head(f"Hackathons | {NAME}", desc, "hackathons.html", p, crumbs_ld([("Home", URL + "/"), ("Hackathons", URL + "/hackathons.html")]))
            + header(p, "hackathons")
            + intro("Hackathons", "Three competitions in 2026", "Short, intense projects built in a team: water and agriculture in Montpellier, games for health in Rabat, and a robotics competition at ENSA Tétouan&rsquo;s mechatronics club.", crumb_home(p, "Hackathons"))
            + with_toc(toc, f'<div class="hcards">{cards}</div>') + seq_pager("hackathons") + footer(p))


def page_hackathon(i):
    h = HACKS[i]
    p = "../"
    n = len(HACKS)
    prev, nxt = HACKS[i - 1], HACKS[(i + 1) % n]
    sections, toc = [], []

    def sec(id_, title, body):
        sections.append(block(id_, f"{len(sections) + 1:02d}", title, title, body))
        toc.append((id_, title))

    proj = ""
    if h["project"]:
        pr = next(q for q in PROJECTS if q["slug"] == h["project"])
        proj = f'<a href="../projects/{pr["slug"]}.html">{e(pr["title"])}</a>'
    rows = [("Date", e(h["date"])), ("Place", e(h["place"])), ("Organiser", e(h["org"])), ("Team", e(h["team"])),
            ("Result", e(h["result"])), ("Project", proj or e(h["project_note"]))]
    sec("overview", "Overview", facts_dl(rows, "facts facts--table reveal"))
    sec("event", "The event", '<div class="prose reveal">' + "".join(f"<p>{e(x)}</p>" for x in h["description"]) + "</div>")
    sec("built", "What we built", f'<div class="prose reveal">{ul(h["built"])}</div>')
    if h["images"]:
        figs = "".join(f'<figure class="reveal"><a href="../assets/{x["src"]}">{img(x["src"], x["alt"], x["w"], x["h"], p)}</a><figcaption>{e(x["caption"])}</figcaption></figure>' for x in h["images"])
        sec("images", "Images", f'<div class="gallery">{figs}</div>')
    files = [f for f in h["files"] if (ROOT / "assets" / f["src"]).exists()]
    if files:
        lis = ""
        for f in files:
            kb = (ROOT / "assets" / f["src"]).stat().st_size / 1024
            sz = f"{kb / 1024:.1f} MB" if kb > 1024 else f"{kb:.0f} KB"
            ic = ICON["file"] if f["kind"] == "PDF" else ICON["image"]
            lis += f'<li><a href="../assets/{f["src"]}" rel="noopener">{ic}<span><b>{e(f["label"])}</b><small>{f["kind"]} &middot; {sz}</small></span></a></li>'
        note = '<p class="note">Presentations are published without the slides that show photos of people.</p>' if any(f["kind"] == "PDF" for f in files) else ""
        sec("documents", "Documents", f'<ul class="files reveal">{lis}</ul>{note}')
    if h["project"]:
        pr = next(q for q in PROJECTS if q["slug"] == h["project"])
        sec("project", "Related project", f'<div class="grid grid--1">{card(pr, PROJECTS.index(pr), p, compact=True)}</div>')
    event = {"@context": "https://schema.org", "@type": "Event", "name": h["title"], "startDate": h["start"], "endDate": h["end"],
             "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode", "description": h["summary"],
             "organizer": {"@type": "Organization", "name": h["org"]},
             "location": {"@type": "Place", "name": h["place"] or "ENSA Tétouan", "address": h["place"] or "Tétouan, Morocco"},
             "url": f'{URL}/hackathons/{h["slug"]}.html'}
    if h["images"]:
        event["image"] = f'{URL}/assets/{h["images"][0]["src"]}'
    crumb = f'<a href="../index.html">Home</a><span aria-hidden="true">/</span><a href="../hackathons.html">Hackathons</a><span aria-hidden="true">/</span><span aria-current="page">{e(h["short"])}</span>'
    return (head(f'{h["title"]} | {NAME}', h["summary"], f'hackathons/{h["slug"]}.html', p,
                 ld(event) + "\n" + crumbs_ld([("Home", URL + "/"), ("Hackathons", URL + "/hackathons.html"), (h["title"], f'{URL}/hackathons/{h["slug"]}.html')]))
            + header(p, "hackathons")
            + intro(f'Hackathon &middot; {e(h["month"])}', e(h["title"]), e(h["summary"]), crumb, f'<p class="tag tag--lg">{e(h["result"])}</p>')
            + with_toc(toc, "".join(sections))
            + pager((f'{prev["slug"]}.html', "Previous", prev["title"]), (f'{nxt["slug"]}.html', "Next", nxt["title"]), ("../hackathons.html", "&larr; All hackathons"))
            + footer(p))


# --------------------------------------------------------------------------- volunteering / honors
def file_link(src, label, kind, p):
    """A document link in the 'files' card style; empty when the file does not exist."""
    path = ROOT / "assets" / src
    if not path.exists():
        return ""
    kb = path.stat().st_size / 1024
    sz = f"{kb / 1024:.1f} MB" if kb > 1024 else f"{kb:.0f} KB"
    ic = ICON["file"] if kind == "PDF" else ICON["image"]
    return f'<li><a href="{p}assets/{src}" rel="noopener">{ic}<span><b>{e(label)}</b><small>{kind} &middot; {sz}</small></span></a></li>'


def certificate(c, p):
    if not c:
        return ""
    link = file_link(c["pdf"], c["label"], "PDF", p)
    if not link:
        return ""
    prev = ""
    if (ROOT / "assets" / c["preview"]).exists():
        prev = f'<a class="cert__preview" href="{p}assets/{c["pdf"]}" rel="noopener" tabindex="-1" aria-hidden="true">{img(c["preview"], c["alt"], c["w"], c["h"], p)}</a>'
    note = f'<p class="note">{e(c["note"])}</p>' if c.get("note") else ""
    return f'<div class="cert">{prev}<div class="cert__body"><p class="eyebrow">Certificate</p><ul class="files">{link}</ul>{note}</div></div>'


def page_volunteering():
    p = ""
    out, toc = [], []
    for x in D["volunteering"]:
        body = f'<p class="entry__lead">{e(x["text"])}</p>{ul(x["points"])}<p class="meta">Cause: {e(x["cause"])}</p>'
        out.append(entry(x["id"], e(x["dates"]), e(x["role"]), e(x["org"]), body, certificate(x.get("certificate"), p)))
        toc.append((x["id"], x["org"].split(",")[0]))
    desc = "Volunteering of Abdessamad Ait Brahim: Erasmus+ youth exchange Hand in Hand (2021) and the Amazigh New Year cultural evening (2022)."
    return (head(f"Volunteering | {NAME}", desc, "volunteering.html", p, crumbs_ld([("Home", URL + "/"), ("Volunteering", URL + "/volunteering.html")]))
            + header(p, "volunteering")
            + intro("Volunteering", "Schools, culture and exchange", "Two experiences from my high school years: an Erasmus+ youth exchange between Belgium and Morocco, and a cultural evening for the Amazigh New Year.", crumb_home(p, "Volunteering"))
            + with_toc(toc, f'<div class="entries">{"".join(out)}</div>') + seq_pager("volunteering") + footer(p))


def page_honors():
    p = ""
    out, toc = [], []
    for i, x in enumerate(D["honors"]):
        id_ = x["hackathon"]
        body = f'<p>{e(x["text"])}</p><p class="meta">Issued by {e(x["issuer"])}</p>'
        extra = f'<p><a class="more-link" href="hackathons/{x["hackathon"]}.html">About the hackathon {ICON["arrow"]}</a></p>'
        out.append(entry(f"honor-{id_}", e(x["date"]), e(x["title"]), e(x["event"]), body, extra))
        toc.append((f"honor-{id_}", x["event"].split(",")[0].replace(" International Hackathon", "")))
    desc = "Honors and awards of Abdessamad Ait Brahim: Water4Future semi-finalist and Water Talent Prize, Game4Health finalist, MECA WORLD CUP participant (2026)."
    return (head(f"Honors | {NAME}", desc, "honors.html", p, crumbs_ld([("Home", URL + "/"), ("Honors", URL + "/honors.html")]))
            + header(p, "honors")
            + intro("Honors and awards", "Recognition in 2026", "Results from three competitions. Each links to the full hackathon page with documents and images.", crumb_home(p, "Honors"))
            + with_toc(toc, f'<div class="entries">{"".join(out)}</div>') + seq_pager("honors") + footer(p))


# --------------------------------------------------------------------------- cv / contact
def page_cv():
    p = ""
    if CV_EXISTS:
        kb = (ROOT / SITE["cv"]).stat().st_size / 1024
        action = (f'<a class="btn btn--primary" href="{SITE["cv"]}" download>{ICON["download"]} Download CV (PDF, {kb:.0f} KB)</a>'
                  f'<a class="btn" href="{SITE["cv"]}" rel="noopener">Open in the browser {ICON["ext"]}</a>')
    else:
        action = '<p>The CV is available on request: please use the <a href="contact.html">contact page</a>.</p>'
    rows = "".join(f'<li><a href="{f}"><b>{lbl}</b><span>{e(d)}</span>{ICON["arrow"]}</a></li>' for k, lbl, f, d in PAGES if k in ("experience", "education", "projects", "about", "volunteering"))
    desc = "Download the CV of Abdessamad Ait Brahim, final-year Big Data and AI engineering student at ENSA Tétouan (PDF, English)."
    return (head(f"CV | {NAME}", desc, "cv.html", p, crumbs_ld([("Home", URL + "/"), ("CV", URL + "/cv.html")]))
            + header(p, "cv")
            + intro("Curriculum vitae", "Résumé", "One page in English: experience, education, selected projects, technical skills and languages.", crumb_home(p, "CV"))
            + f'''<div class="container narrow">
<div class="panel reveal">
<p class="eyebrow">PDF &middot; English &middot; updated 2026</p>
<h2>Abdessamad Ait Brahim, CV</h2>
<p>AI engineering student, machine learning and data analytics. Seeking a final-year internship (PFE) starting January 2027.</p>
<div class="actions">{action}</div>
</div>
<p class="eyebrow gap">The same content, in more detail</p>
<ul class="index index--compact">{rows}</ul>
</div>''' + seq_pager("cv") + footer(p))


def page_contact():
    p = ""
    desc = "Contact Abdessamad Ait Brahim about internships, research and collaboration in AI: email, LinkedIn or GitHub."
    return (head(f"Contact | {NAME}", desc, "contact.html", p, crumbs_ld([("Home", URL + "/"), ("Contact", URL + "/contact.html")]))
            + header(p, "contact")
            + intro("Contact", "Let&rsquo;s talk", "Open to internships, research and collaboration in AI. The fastest way to reach me is by email or LinkedIn.", crumb_home(p, "Contact"))
            + f'''<div class="container narrow">
<div class="contact reveal">
<div class="contact__item" id="email">
<a class="contact__row" data-email data-user="{SITE['email_user']}" data-domain="{SITE['email_domain']}" href="#email">{ICON['mail']}<span><b>Email</b><small data-email-text>Shown when JavaScript is on, to keep it away from spam bots</small></span>{ICON['ext']}</a>
<div class="contact__alt" role="group" aria-label="Email actions">
<button class="copy" type="button" data-copy-email data-user="{SITE['email_user']}" data-domain="{SITE['email_domain']}" aria-label="Copy email address" hidden>{ICON['copy']}<span>Copy address</span></button>
<a class="copy" href="#email" data-email data-user="{SITE['email_user']}" data-domain="{SITE['email_domain']}">{ICON['mail']}<span>Open in Gmail</span></a>
<a class="copy" href="#email" data-email-outlook data-user="{SITE['email_user']}" data-domain="{SITE['email_domain']}">{ICON['mail']}<span>Open in Outlook</span></a>
</div>
<p class="contact__fallback"><a href="#email" data-email-app data-user="{SITE['email_user']}" data-domain="{SITE['email_domain']}" hidden>or use your default mail app</a></p>
<span class="sr-only" role="status" aria-live="polite" data-copy-status></span>
</div>
<a class="contact__row" href="{SITE['linkedin']}" rel="me noopener">{ICON['linkedin']}<span><b>LinkedIn</b><small>in/abdessamad-aitbrahim</small></span>{ICON['ext']}</a>
<a class="contact__row" href="{SITE['github']}" rel="me noopener">{ICON['github']}<span><b>GitHub</b><small>@abdessamadaitbrahim</small></span>{ICON['ext']}</a>
</div>
<p class="note">Open to international opportunities.</p>
</div>''' + seq_pager("contact") + footer(p))


def page_404():
    p = "/"
    html = (head(f"Page not found | {NAME}", "Page not found.", "404.html", p) + header(p, "")
            + intro("Error 404", "Page not found", "The page you are looking for does not exist or has moved.")
            + f'''<div class="container narrow"><div class="actions"><a class="btn btn--primary" href="/index.html">Back to the home page {ICON['arrow']}</a><a class="btn" href="/projects.html">See the projects</a></div></div>'''
            + footer(p))
    return html.replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"')


# --------------------------------------------------------------------------- main
def main():
    pages = {
        "index.html": page_index(), "about.html": page_about(), "projects.html": page_projects(),
        "education.html": page_education(), "experience.html": page_experience(), "hackathons.html": page_hackathons(),
        "volunteering.html": page_volunteering(), "honors.html": page_honors(), "cv.html": page_cv(), "contact.html": page_contact(),
    }
    for i, pr in enumerate(PROJECTS):
        pages[f'projects/{pr["slug"]}.html'] = page_project(i)
    for i, h in enumerate(HACKS):
        pages[f'hackathons/{h["slug"]}.html'] = page_hackathon(i)
    # remove stale generated pages
    for d in ("projects", "hackathons"):
        for f in (ROOT / d).glob("*.html") if (ROOT / d).exists() else []:
            if f"{d}/{f.name}" not in pages:
                f.unlink()
    for path, html in pages.items():
        write(path, html)
    write("404.html", page_404())

    def prio(path):
        return "1.0" if path == "index.html" else "0.8" if "/" not in path else "0.6"
    urls = "".join(f'<url><loc>{URL}/{"" if path == "index.html" else path}</loc><lastmod>{TODAY}</lastmod><priority>{prio(path)}</priority></url>\n' for path in pages)
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /tools/\nSitemap: {URL}/sitemap.xml\n")
    (ROOT / "favicon.svg").unlink(missing_ok=True)  # replaced by the portrait icons from tools/make_icons.py
    write("site.webmanifest", json.dumps({"name": NAME, "short_name": "A. Ait Brahim", "start_url": "./index.html", "display": "browser",
                                          "background_color": "#f4eee3", "theme_color": "#f4eee3",
                                          "icons": [{"src": "assets/img/site/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
                                                    {"src": "assets/img/site/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=1) + "\n")
    write(".nojekyll", "")
    print("built:", len(pages) + 1, "pages")


if __name__ == "__main__":
    main()
