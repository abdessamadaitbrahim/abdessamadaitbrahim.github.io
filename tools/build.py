"""Static site generator for the portfolio.

Run from the repository root:  python tools/build.py
Reads tools/content.json and writes index.html, projects/*.html, 404.html,
sitemap.xml, robots.txt and favicon.svg.
"""
import json
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "tools" / "content.json").read_text(encoding="utf-8"))
SITE, PROJECTS = DATA["site"], DATA["projects"]
URL = SITE["url"]

CATS = [("all", "All"), ("nlp", "NLP"), ("vision", "Computer Vision"), ("dl", "Deep Learning"),
        ("ml", "Machine Learning"), ("bigdata", "Big Data"), ("embedded", "Embedded & IoT"),
        ("bi", "Data & BI"), ("foundations", "Foundations")]
CAT_LABEL = dict(CATS)
FEATURED = 8

ICON = {
 "github": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 .5C5.65.5.5 5.65.5 12c0 5.08 3.29 9.39 7.86 10.91.58.1.79-.25.79-.56v-2c-3.2.7-3.87-1.37-3.87-1.37-.52-1.33-1.28-1.69-1.28-1.69-1.04-.71.08-.7.08-.7 1.15.08 1.76 1.18 1.76 1.18 1.03 1.76 2.69 1.25 3.35.96.1-.74.4-1.25.73-1.54-2.55-.29-5.24-1.28-5.24-5.68 0-1.25.45-2.28 1.18-3.08-.12-.29-.51-1.46.11-3.05 0 0 .97-.31 3.17 1.18a11 11 0 0 1 5.78 0c2.2-1.49 3.17-1.18 3.17-1.18.62 1.59.23 2.76.11 3.05.74.8 1.18 1.83 1.18 3.08 0 4.41-2.69 5.38-5.25 5.67.41.36.78 1.06.78 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 23.5 12C23.5 5.65 18.35.5 12 .5Z"/></svg>',
 "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.03-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.34V9h3.42v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28ZM5.34 7.43a2.07 2.07 0 1 1 0-4.14 2.07 2.07 0 0 1 0 4.14ZM7.12 20.45H3.56V9h3.56v11.45ZM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0Z"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
 "download": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m0 0 4-4m-4 4-4-4M4 19h16"/></svg>',
 "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>',
 "moon": '<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5Z"/></svg>',
 "sun": '<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4M2 12h2m16 0h2M4.9 19.1l1.4-1.4m11.4-11.4 1.4-1.4"/></svg>',
 "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
}

NAV = [("about", "About"), ("projects", "Projects"), ("skills", "Skills"), ("experience", "Experience"), ("cv", "CV"), ("contact", "Contact")]

SKILLS = [
 ("Machine learning and deep learning", ["PyTorch", "TensorFlow", "scikit-learn", "XGBoost", "Isolation Forest", "Reinforcement learning"]),
 ("NLP and LLMs", ["Hugging Face", "Transformers", "XLM-RoBERTa", "BERT fine-tuning", "LLMs", "TF-IDF"]),
 ("Computer vision", ["OpenCV", "YOLOv8", "CNN: VGG, ResNet", "Image captioning", "BLIP"]),
 ("Big Data", ["Apache Spark", "Apache Kafka", "Hadoop MapReduce", "MongoDB", "ETL / ELT"]),
 ("Languages and databases", ["Python", "C++", "SQL", "T-SQL", "PostgreSQL", "MySQL", "MariaDB", "SQL Server", "SQLite"]),
 ("Data visualisation and BI", ["Power BI", "Tableau", "SSIS", "SSAS", "Streamlit", "Matplotlib"]),
 ("Backend and tools", ["Flask", "FastAPI", "Docker", "Git and GitHub", "Linux", "AWS", "SciPy"]),
 ("Embedded and IoT", ["ESP32", "Arduino", "WebSocket", "Signal processing"]),
]

THEME_JS = '''<script>(function(){try{var t=localStorage.getItem("theme");if(!t){t=matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light"}document.documentElement.setAttribute("data-theme",t)}catch(e){}document.documentElement.classList.add("js")})();</script>'''

def page_head(title, desc, path, depth, extra_ld=""):
    p = "../" * depth
    canon = URL + "/" + path
    og = URL + "/assets/img/site/og.png"
    return f'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#2447f5">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{p}favicon.svg" type="image/svg+xml">
<link rel="preload" href="{p}assets/fonts/fraunces-latin-opsz-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{p}assets/fonts/inter-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
{THEME_JS}
<link rel="stylesheet" href="{p}assets/css/style.css">
{extra_ld}
</head>'''

def header(depth):
    p = "../" * depth
    home = f"{p}index.html" if depth else ""
    links = "".join(f'<a href="{home}#{i}" data-spy>{l}</a>' for i, l in NAV[:2] + NAV[2:3] + NAV[3:4] + NAV[5:])
    return f'''<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
<div class="container">
<a class="brand" href="{p or './'}" aria-label="Abdessamad Ait Brahim, home">Abdessamad <span>Ait Brahim</span></a>
<nav class="nav" id="nav" aria-label="Main">{links}</nav>
<div class="tools">
<a class="icon-btn" href="{SITE['github']}" aria-label="GitHub profile" rel="me noopener">{ICON['github']}</a>
<a class="icon-btn" href="{SITE['linkedin']}" aria-label="LinkedIn profile" rel="me noopener">{ICON['linkedin']}</a>
<button class="icon-btn theme-toggle" type="button" aria-label="Switch color theme">{ICON['moon']}{ICON['sun']}</button>
<button class="icon-btn menu-btn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav">{ICON['menu']}</button>
</div>
</div>
</header>'''

def footer(depth):
    p = "../" * depth
    return f'''<footer class="site-footer">
<div class="container">
<span>&copy; 2026 Abdessamad Ait Brahim</span>
<span>Plain HTML, CSS and JavaScript. Hosted on GitHub Pages.</span>
<a href="#top">Back to top</a>
</div>
</footer>
<script src="{p}assets/js/main.js" defer></script>
</body>
</html>
'''

def img_tag(key, alt, w, h, depth, lazy=True, cls=""):
    p = "../" * depth
    extra = ' loading="lazy" decoding="async"' if lazy else ""
    c = f' class="{cls}"' if cls else ""
    return f'<img src="{p}assets/img/projects/{key}.webp" alt="{e(alt)}" width="{w}" height="{h}"{extra}{c}>'

def card(pr, i):
    cats = " ".join(pr["cats"])
    label = " · ".join(CAT_LABEL[c] for c in pr["cats"])
    href = f'projects/{pr["slug"]}.html' if pr["detail"] else pr["repo"]
    ext = "" if pr["detail"] else ' rel="noopener"'
    if pr.get("cover"):
        cls = "card__media card__media--contain" if pr.get("cover_fit") == "contain" else "card__media"
        media = f'<a class="{cls}" href="{href}"{ext} tabindex="-1" aria-hidden="true">{img_tag(pr["cover"], pr["title"] + " preview", pr["cover_w"], pr["cover_h"], 0)}</a>'
    else:
        media = f'<a class="card__media" href="{href}"{ext} tabindex="-1" aria-hidden="true"><div class="ph">{e(pr.get("label", pr["title"]))}</div></a>'
    chips = "".join(f'<li class="chip">{e(s)}</li>' for s in pr["stack"][:4])
    links = ""
    if pr["detail"]:
        links += f'<a href="projects/{pr["slug"]}.html">Case study &rarr;</a>'
    links += f'<a href="{pr["repo"]}" rel="noopener">GitHub &#8599;</a>'
    if pr.get("demo"):
        links += f'<a href="{pr["demo"]}" rel="noopener">Live demo &#8599;</a>'
    extra = " is-extra" if i >= FEATURED else ""
    return f'''<article class="card reveal{extra}" data-cats="{cats}">
{media}
<div class="card__body">
<div class="card__cats">{e(label)}</div>
<h3><a href="{href}"{ext}>{e(pr["title"])}</a></h3>
<p>{e(pr["short"])}</p>
<ul class="chips">{chips}</ul>
<div class="card__links">{links}</div>
</div>
</article>'''

def index_html():
    counts = {c: sum(1 for p in PROJECTS if c in p["cats"]) for c, _ in CATS if c != "all"}
    counts["all"] = len(PROJECTS)
    filters = "".join(
        f'<button class="filter" type="button" data-filter="{c}" aria-pressed="{"true" if c == "all" else "false"}">{l}<span class="n">{counts[c]}</span></button>'
        for c, l in CATS if counts[c])
    cards = "\n".join(card(p, i) for i, p in enumerate(PROJECTS))
    skills = "".join(f'<div class="skill reveal"><h3>{e(t)}</h3><ul class="chips">' + "".join(f'<li class="chip">{e(s)}</li>' for s in items) + "</ul></div>" for t, items in SKILLS)
    toc = "".join(f'<li><a href="#{i}" data-spy>{l}</a></li>' for i, l in NAV)
    desc = "Final-year Big Data and AI engineering student at ENSA Tétouan. NLP, computer vision, deep learning and Big Data projects. Open to a 6-month PFE internship starting January 2027."
    ld = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "Person", "name": SITE["name"], "url": URL + "/",
        "image": URL + "/assets/img/site/portrait.webp",
        "jobTitle": "Big Data and Artificial Intelligence engineering student",
        "alumniOf": {"@type": "CollegeOrUniversity", "name": "ENSA Tétouan, Abdelmalek Essaâdi University"},
        "knowsAbout": ["Machine learning", "Deep learning", "Computer vision", "Natural language processing", "Big Data"],
        "sameAs": [SITE["github"], SITE["linkedin"]]}, ensure_ascii=False) + "</script>"
    return page_head("Abdessamad Ait Brahim | AI and Big Data Engineering Student", desc, "", 0, ld) + header(0) + f'''
<main id="main">
<div id="top"></div>
<section class="hero" aria-label="Introduction">
<canvas id="hero-canvas" aria-hidden="true"></canvas>
<div class="container">
<div>
<p class="eyebrow">ENSA Tétouan &middot; Big Data &amp; AI engineering &middot; Class of 2027</p>
<h1>Abdessamad <em>Ait Brahim</em></h1>
<p class="lead">Final-year engineering student building reliable, data-driven AI systems: natural language processing, computer vision and Big Data.</p>
<p class="status"><i aria-hidden="true"></i>Open to a 6-month PFE internship starting January 2027</p>
<div class="actions">
<a class="btn btn--primary" href="#projects">View projects {ICON['arrow']}</a>
<a class="btn" href="#cv">{ICON['download']} Download CV</a>
<a class="btn" href="#contact">{ICON['mail']} Contact</a>
</div>
<div class="social">
<a href="{SITE['github']}" rel="me noopener">{ICON['github']} GitHub</a>
<a href="{SITE['linkedin']}" rel="me noopener">{ICON['linkedin']} LinkedIn</a>
</div>
</div>
<div class="portrait">
<div class="portrait__frame"><img src="assets/img/site/portrait.webp" alt="Portrait of Abdessamad Ait Brahim" width="600" height="639" fetchpriority="high"></div>
<div class="portrait__tag"><b>Morocco</b>Machine learning &middot; NLP &middot; Vision</div>
</div>
</div>
</section>

<div class="container layout">
<aside class="toc" aria-label="On this page"><h2>On this page</h2><ol>{toc}</ol></aside>
<div>

<section class="block" id="about">
<div class="block__head reveal"><p class="eyebrow">01 &middot; About</p><h2>Rigorous experiments, reliable systems</h2></div>
<div class="about reveal">
<p>I am a final-year engineering student in Big Data and Artificial Intelligence at ENSA Tétouan (Abdelmalek Essaâdi University), Morocco.</p>
<p>My interests are machine learning, deep learning, computer vision, NLP and multimodal AI, with a focus on building reliable, data-driven solutions through careful experimentation and evaluation. I enjoy exploring AI research as well as real-world applications in scientific and industrial settings.</p>
<p>I am looking for a 6-month PFE internship starting in January 2027, with a long-term goal of pursuing a PhD in AI.</p>
<blockquote class="quote">Everything will come in its time, right and fittingly.<cite>Abdessamad</cite></blockquote>
<dl class="facts">
<div class="fact"><dt>Studying</dt><dd>Big Data &amp; AI engineering, ENSA Tétouan</dd></div>
<div class="fact"><dt>Looking for</dt><dd>6-month PFE internship, January 2027</dd></div>
<div class="fact"><dt>Long-term goal</dt><dd>PhD in AI</dd></div>
<div class="fact"><dt>Based in</dt><dd>Morocco</dd></div>
</dl>
<div class="interests">
<div class="interest"><b>Natural language processing</b><span>Transformers, multilingual and low-resource text</span></div>
<div class="interest"><b>Computer vision</b><span>Detection, recognition, image captioning</span></div>
<div class="interest"><b>Deep learning</b><span>Architectures built and compared from scratch</span></div>
<div class="interest"><b>Multimodal AI</b><span>Vision and language together</span></div>
<div class="interest"><b>Big Data</b><span>Streaming, distributed processing, pipelines</span></div>
</div>
</div>
</section>

<section class="block" id="projects">
<div class="block__head reveal"><p class="eyebrow">02 &middot; Projects</p><h2>Selected work</h2><p>AI, machine learning and NLP projects come first. Each card links to a case study or to the code on GitHub.</p></div>
<div class="filters reveal" role="group" aria-label="Filter projects">{filters}</div>
<div class="grid" id="project-grid">
{cards}
</div>
<div class="more"><button class="btn" type="button" id="show-more">Show all {len(PROJECTS)} projects</button></div>
</section>

<section class="block" id="skills">
<div class="block__head reveal"><p class="eyebrow">03 &middot; Skills</p><h2>Tools I work with</h2></div>
<div class="skills">{skills}</div>
</section>

<section class="block" id="experience">
<div class="block__head reveal"><p class="eyebrow">04 &middot; Experience &amp; education</p><h2>Path so far</h2></div>
<ol class="timeline">
<li class="tl reveal"><div class="tl__meta">August 2026</div><h3>AI Engineer Intern, LLM Conversational Agent (POC)</h3><p class="tl__org">STMicroelectronics &middot; Bouskoura, Casablanca</p><p>Built a conversational AI proof of concept for analysing industrial production data: Python/Pandas pipelines for cleaning, validation and flow indicators, and a read-only REST API on MariaDB, FastAPI and Dify, with data quality checks and prompt engineering to improve answer reliability.</p></li>
<li class="tl reveal"><div class="tl__meta">June &ndash; July 2026</div><h3>AI Engineer Intern, Labex / Botground</h3><p class="tl__org">Sentiment analysis SaaS project &middot; Casablanca</p><p>Built a multilingual NLP pipeline (French, English, Darija), annotated 4,000+ conversations across three domains, benchmarked XLM-RoBERTa, mBERT and DarijaBERT (up to 84.3% accuracy) and deployed a Flask analytics dashboard on AWS. <a href="projects/botground.html">Read the case study</a>.</p></li>
<li class="tl reveal"><div class="tl__meta">July &ndash; August 2025</div><h3>AI Engineer Intern, SmartMatchRH</h3><p class="tl__org">Cloud Marketing Hub &middot; Tangier</p><p>Developed a candidate/job matching model (deep learning and multilingual NLP) with an end-to-end data pipeline served through a Flask REST API, plus three Power BI dashboards for HR KPIs.</p></li>
<li class="tl reveal"><div class="tl__meta">2024 &ndash; present</div><h3>Engineering degree, Big Data &amp; Artificial Intelligence</h3><p class="tl__org">ENSA Tétouan, Abdelmalek Essaâdi University</p><img class="tl__logo" src="assets/img/site/ensa-logo.webp" alt="ENSA Tétouan logo" width="640" height="239" loading="lazy"></li>
<li class="tl reveal"><div class="tl__meta">2022 &ndash; 2024</div><h3>Integrated preparatory years for engineering schools</h3><p class="tl__org">ENSA Tétouan</p></li>
<li class="tl reveal"><div class="tl__meta">2021 &ndash; 2022</div><h3>Scientific Baccalaureate, French option</h3><p class="tl__org">Lycée Tarik Ibn Ziad, Kelaat M&rsquo;Gouna</p></li>
</ol>
<h3 class="subhead reveal">Hackathons</h3>
<div class="events">
<div class="event reveal"><p class="eyebrow">2026 &middot; National robotics competition</p><h4>MECA WORLD CUP</h4><p>Organised by the Club Mécatronique of ENSA Tétouan. Built SportLineBot, an autonomous field-marking robot, with a mechatronics teammate. Certificate of participation.</p><a href="projects/sportlinebot.html">SportLineBot case study &rarr;</a></div>
<div class="event reveal"><p class="eyebrow">3&ndash;4 April 2026 &middot; Rabat</p><h4>Game4Health Hackathon</h4><p>Innovation competition organised by the SmartTech Lab of ISMAGI. Team Health Hackers built Heart Guardian, an ECG-driven adaptive game. Certificate of participation.</p><a href="projects/heart-guardian.html">Heart Guardian case study &rarr;</a></div>
</div>
</section>

<section class="block" id="cv">
<div class="block__head reveal"><p class="eyebrow">05 &middot; Curriculum vitae</p><h2>Résumé</h2></div>
<div class="cv-card reveal">
<div><h3>Abdessamad Ait Brahim, CV</h3><p id="cv-missing" hidden>The CV is available on request: please use the contact section below.</p><p>PDF, English. Includes experience, education and skills.</p></div>
<a class="btn btn--primary" id="cv-download" data-href="assets/cv/Abdessamad_Ait_Brahim_CV.pdf" href="#contact" hidden download>{ICON['download']} Download CV (PDF)</a>
</div>
</section>

<section class="block" id="contact">
<div class="block__head reveal"><p class="eyebrow">06 &middot; Contact</p><h2>Let&rsquo;s talk</h2></div>
<div class="contact-card reveal">
<h3>Open to internships, research and collaboration in AI.</h3>
<p>The fastest way to reach me is by email or LinkedIn.</p>
<div class="contact-links">
<a class="btn btn--primary" href="{SITE['linkedin']}" rel="me noopener">{ICON['linkedin']} LinkedIn</a>
<a class="btn" data-email data-user="{SITE['email_user']}" data-domain="{SITE['email_domain']}" href="{SITE['linkedin']}">{ICON['mail']} Email me</a>
<a class="btn" href="{SITE['github']}" rel="me noopener">{ICON['github']} GitHub</a>
</div>
</div>
</section>

</div>
</div>
</main>
''' + footer(0)

def detail_html(idx):
    pr = DETAIL[idx]
    prev = DETAIL[idx - 1]
    nxt = DETAIL[(idx + 1) % len(DETAIL)]
    chips = "".join(f'<li class="chip">{e(s)}</li>' for s in pr["stack"])
    ctx = f'<p class="eyebrow">{e(pr["context"])}</p>' if pr.get("context") else ""
    built = "".join(f"<li>{e(x)}</li>" for x in pr["built"])
    results = f'<h2>Results</h2><ul>{"".join(f"<li>{e(x)}</li>" for x in pr["results"])}</ul>' if pr["results"] else ""
    p1 = "../"
    cover = ""
    gal = ""
    if pr["gallery"]:
        g = pr["gallery"][0]
        cover = f'<div class="cover">{img_tag(g["img"], g["alt"], g["w"], g["h"], 1, lazy=False)}</div>'
        rest = []
        for x in pr["gallery"][1:]:
            rest.append('<figure><a href="' + p1 + 'assets/img/projects/' + x["img"] + '.webp">' + img_tag(x["img"], x["alt"], x["w"], x["h"], 1) + '</a><figcaption>' + e(x["caption"]) + '</figcaption></figure>')
        if rest:
            gal = '<h2>More</h2><div class="gallery">' + "".join(rest) + '</div>'
    desc = pr["short"]
    ld = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "CreativeWork", "name": pr["title"], "description": desc,
        "author": {"@type": "Person", "name": SITE["name"], "url": URL + "/"},
        "codeRepository": pr["repo"], "url": f'{URL}/projects/{pr["slug"]}.html'}, ensure_ascii=False) + "</script>"
    demo = f'<a class="btn" href="{pr["demo"]}" rel="noopener">Live demo &#8599;</a>' if pr.get("demo") else ""
    return page_head(f'{pr["title"]} | Abdessamad Ait Brahim', desc, f'projects/{pr["slug"]}.html', 1, ld) + header(1) + f'''
<main id="main">
<div id="top"></div>
<div class="container page">
<a class="crumb" href="../index.html#projects">&larr; All projects</a>
{ctx}
<h1>{e(pr["title"])}</h1>
<p class="lead">{e(pr["short"])}</p>
{cover}
</div>
<div class="container article">
<div>
<h2>The problem</h2>
<p>{e(pr["problem"])}</p>
<h2>What I built</h2>
<ul>{built}</ul>
{results}
{gal}
</div>
<aside class="aside">
<div class="aside__box"><h3>Code</h3><a class="btn btn--primary" href="{pr["repo"]}" rel="noopener">{ICON['github']} View on GitHub</a>{demo}</div>
<div class="aside__box"><h3>Stack</h3><ul class="chips">{chips}</ul></div>
</aside>
</div>
<div class="container pager">
<a href="{prev["slug"]}.html"><small>Previous</small><b>{e(prev["title"])}</b></a>
<a class="next" href="{nxt["slug"]}.html"><small>Next</small><b>{e(nxt["title"])}</b></a>
</div>
</main>
''' + footer(1)

DETAIL = [p for p in PROJECTS if p["detail"]]

def main():
    (ROOT / "index.html").write_text(index_html(), encoding="utf-8")
    (ROOT / "projects").mkdir(exist_ok=True)
    for i, pr in enumerate(DETAIL):
        (ROOT / "projects" / f'{pr["slug"]}.html').write_text(detail_html(i), encoding="utf-8")
    nf = page_head("Page not found | Abdessamad Ait Brahim", "Page not found.", "404.html", 0) + header(0).replace('href="#', 'href="/#').replace('href=""', 'href="/"') + '''
<main id="main"><div class="container page"><p class="eyebrow">404</p><h1>Page not found</h1><p class="lead">The page you are looking for does not exist.</p><a class="btn btn--primary" href="/">Back to the portfolio</a></div></main>
''' + footer(0)
    nf = nf.replace('src="assets/', 'src="/assets/').replace('href="assets/', 'href="/assets/').replace('href="favicon', 'href="/favicon')
    (ROOT / "404.html").write_text(nf, encoding="utf-8")
    urls = [URL + "/"] + [f'{URL}/projects/{p["slug"]}.html' for p in DETAIL]
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {URL}/sitemap.xml\n", encoding="utf-8")
    (ROOT / "favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#2447f5"/><text x="32" y="45" text-anchor="middle" font-family="Georgia,serif" font-size="38" font-weight="700" fill="#fff">A</text></svg>\n', encoding="utf-8")
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    print("built:", 1 + len(DETAIL), "pages")

if __name__ == "__main__":
    main()
