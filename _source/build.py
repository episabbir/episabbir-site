import time as _t
VER=str(int(_t.time()))
import json, html, shutil, os, re
from urllib.parse import quote

OUT = 'site'
os.makedirs(f'{OUT}/images/logos', exist_ok=True)
shutil.copy('headshot.jpg', f'{OUT}/images/headshot.jpg')

E = html.escape

# ---------- icons (generic stroke icons) ----------
P = {
 'image': '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="8.5" cy="9.5" r="1.5"/><path d="m21 16-5-5-9 9"/>',
 'stopwatch': '<circle cx="12" cy="14" r="8"/><path d="M12 10v4l2.5 2.5M10 2h4M12 2v4M19 6l1.5-1.5"/>',
 'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
 'link': '<path d="M10 13a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/><path d="M14 11a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/>',
 'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
 'ext': '<path d="M14 4h6v6M20 4l-9 9"/><path d="M19 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h5"/>',
 'x': '<path d="M6 6l12 12M18 6 6 18"/>',
 'db': '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
 'doc': '<path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
 'chat': '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
 'shield': '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
 'users': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M21.5 20a6.5 6.5 0 0 0-4-6"/>',
 'chart': '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
 'pen': '<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="m13 7 4 4"/>',
 'home': '<path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/>',
 'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
 'coin': '<circle cx="12" cy="12" r="9"/><path d="M15 9.5c-.5-1-1.6-1.5-3-1.5-1.7 0-3 .8-3 2s1.3 1.7 3 2 3 .8 3 2-1.3 2-3 2c-1.4 0-2.5-.5-3-1.5M12 6v12"/>',
 'plane': '<path d="M21 15.5 13.5 11V5a1.5 1.5 0 0 0-3 0v6L3 15.5V18l7.5-2.5V19L8 20.5V22l4-1 4 1v-1.5L13.5 19v-3.5L21 18z"/>',
 'trophy': '<path d="M8 4h8v5a4 4 0 0 1-8 0z"/><path d="M8 6H4v1a4 4 0 0 0 4 4M16 6h4v1a4 4 0 0 1-4 4M12 13v4M8 21h8M9 17h6"/>',
 'cap': '<path d="m2 9 10-5 10 5-10 5z"/><path d="M6 11v5c3 2 9 2 12 0v-5M22 9v6"/>',
 'medal': '<circle cx="12" cy="15" r="5"/><path d="M8.5 11 6 3h4l2 4 2-4h4l-2.5 8"/>',
 'flask': '<path d="M9 3h6M10 3v6L4.5 19a1.5 1.5 0 0 0 1.3 2h12.4a1.5 1.5 0 0 0 1.3-2L14 9V3"/><path d="M7 15h10"/>',
}
def ic(name, cls='icon'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{P[name]}</svg>'

REMOTE = {}
def logo(file, fallback, size=''):
    r = REMOTE.get(file)
    # try the local file first, then the online copy, then show the text badge
    onerr = (f"if(!this.dataset.r){{this.dataset.r=1;this.src='{r}'}}else{{this.remove()}}" if r else 'this.remove()')
    return (f'<span class="logo {size}"><span class="fallback">{fallback}</span>'
            f'<img src="images/logos/{file}" alt="" onerror="{onerr}"></span>')


PERSON_LD = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Person","name":"Md Sabbir Ahmed","jobTitle":"Epidemiologist",
"url":"https://episabbir.ca/","image":"https://episabbir.ca/images/headshot.jpg",
"address":{"@type":"PostalAddress","addressRegion":"SK","addressCountry":"CA"},
"alumniOf":[{"@type":"CollegeOrUniversity","name":"University of Saskatchewan"},{"@type":"CollegeOrUniversity","name":"Patuakhali Science and Technology University"}],
"knowsAbout":["Epidemiology","Childhood immunization","Population health","SAS","R"],
"sameAs":["https://www.linkedin.com/in/sabbirepidemiologist/","https://orcid.org/0000-0002-7663-2181"]}
</script>"""

# ---------- shared parts ----------
NAV = [('index.html', 'Home'), ('about.html', 'About me'), ('research.html', 'My Research'),
       ('blog.html', 'Blog'), ('work.html', 'Want to work with me?')]  # Gallery hidden from menu Nov 7, 2026 (no photos); re-add ('gallery.html', 'Gallery') to bring it back

def nav(current):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if label == current else ''
        cls = ' class="cta"' if label.startswith('Want') else ''
        items.append(f'<li><a href="{href}"{cur}{cls}>{E(label)}</a></li>')
    return ('<nav class="site-nav" aria-label="Main">'
            f'<div class="nav-bar"><span class="nav-here">{E(current)}</span>'
            '<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="main-menu">'
            '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>Menu</button></div>'
            '<ul id="main-menu">' + ''.join(items) + '</ul></nav>')

NAV_JS = """<script>
(function(){var b=document.querySelector('.menu-toggle'),n=document.querySelector('.site-nav');
if(b){b.addEventListener('click',function(){var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});}})();
</script>"""

def external_new_tab(html_text):
    # every link to another website opens in a new tab
    def fix(m):
        tag = m.group(0)
        if 'target=' in tag: return tag
        return tag[:-1] + ' target="_blank" rel="noopener">'
    return re.sub(r'<a\b[^>]*href="https?://[^"]*"[^>]*>', fix, html_text)

FOOTER = f'''<footer class="contact" id="contact">
<div class="wrap">
<div>
<h2>Get in touch</h2>
<p>Questions, collaborations or a data project in mind? Send me a note.</p>
</div>
<div class="contact-links">
<a class="icon-only" href="mailto:sabbir.epidemiologist@gmail.com" aria-label="Email me: sabbir.epidemiologist@gmail.com" title="sabbir.epidemiologist@gmail.com">{ic('mail')}</a>
<a class="icon-only" href="https://www.linkedin.com/in/sabbirepidemiologist/" aria-label="LinkedIn profile" title="LinkedIn">{logo('linkedin.png', 'in', 'sm')}</a>
<a class="icon-only" href="https://orcid.org/0000-0002-7663-2181" aria-label="ORCID profile" title="ORCID">{logo('orcid.png', 'iD', 'sm')}</a>
</div>
<div class="small-print footnotes">
<p>The views expressed on this site are my own and do not represent the views or positions of my employer.</p>
<p>© 2026 Md Sabbir Ahmed · Built to WCAG 2.1 AA accessibility standards</p>
</div>
</div>
</footer>'''

SITE_URL = 'https://episabbir.ca/'

def page(title, desc, current, body, script='', og_img='images/og-card.png', path=''):
    out = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="icon" type="image/png" sizes="32x32" href="images/favicon-32.png">
<link rel="apple-touch-icon" href="images/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Md Sabbir Ahmed">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{SITE_URL}{og_img}">
<meta property="og:url" content="{SITE_URL}{path}">
<link rel="canonical" href="{SITE_URL}{path}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="css/style.css?v={VER}">
</head>
<body>
{nav(current)}
<main>
{body}
</main>
{FOOTER}
{script}
{NAV_JS}
</body>
</html>
'''
    return external_new_tab(out)

# ---------- BLOG DATA (newest first; first = featured) ----------
from blog_posts import POSTS
BLOG_CATS = ['Global health hot topics', 'Reading health data', 'Public health essentials', 'Careers and higher study']
THEME_STYLE = {'Global health hot topics': ('pill-peach', '#fbefd2', '#6b4e0e'),
               'Reading health data': ('pill-mint', '#dff1ee', '#0b5a54'),
               'Public health essentials': ('pill-peach', '#fbefd2', '#6b4e0e'),
               'Careers and higher study': ('pill-mint', '#dff1ee', '#0b5a54')}
os.makedirs(f'{OUT}/images/blog', exist_ok=True)
def post_url(p): return f"post-{p['slug']}.html"
def post_img(p, cls='post-img'):
    pill, bg, fg = THEME_STYLE[p['theme']]
    return (f'<div class="{cls}" style="background:{bg};color:{fg}">{ic("image")}'
            f'<img src="images/blog/{p["image"]}?v={VER}" alt="{E(p["image_alt"])}" onerror="this.remove()"></div>')
def post_card(p, extra_cls='', data=True):
    pill = THEME_STYLE[p['theme']][0]
    d = f' data-cat="{E(p["theme"])}"' if data else ''
    return f'''<a class="card {extra_cls}" href="{post_url(p)}"{d}>
{post_img(p)}
<div class="card-body"><span class="pill {pill}">{E(p['theme'])}</span><h3>{E(p['title'])}</h3>
<p class="excerpt">{E(p['summary'])}</p><p>{E(p['date'])} · {E(p['read'])}</p></div>
</a>'''

# ---------- HOME ----------
fb_page = 'https://www.facebook.com/profile.php?id=61571197702458'
fb_src = ('https://www.facebook.com/plugins/page.php?href=' + quote(fb_page, safe='') +
          '&tabs=timeline&width=500&height=520&small_header=true&adapt_container_width=true&hide_cover=false&show_facepile=false')

post_cards = ''.join(post_card(p, data=False) for p in POSTS[:3])

_pubs = sorted(json.load(open('pubs.json')), key=lambda p: -p['n'])[:3]
FEATURED = ''.join(f'''<a class="paper" href="https://doi.org/{E(p['doi'])}" target="_blank" rel="noopener">
<div class="paper-thumb"><img src="images/papers/p{p['n']:02d}.jpg" alt="First page of the article" loading="lazy"></div>
<div class="paper-top"><span class="j">{E(p['journal'])}</span><span>{p['year']}</span></div>
<div class="paper-body"><h3>{E(p['title'])}</h3></div>
<div class="paper-foot"><span></span><span class="read">Read article {ic('ext')}</span></div>
</a>''' for p in _pubs)

home = f'''<div class="wrap">
<section class="hero" aria-labelledby="hero-title">
<div class="hero-text">
<span class="pill pill-mint" style="font-size:14px;padding:7px 14px;text-transform:uppercase;letter-spacing:.08em;font-weight:700">Md Sabbir Ahmed</span>
<h1 id="hero-title">Translating health data into <span>evidence for action.</span></h1>
<p>Hi, I'm Sabbir Ahmed, an epidemiologist at the provincial Ministry of Health in Saskatchewan, Canada. I work on childhood immunization surveillance and population health research.</p>
<div style="display:flex;flex-wrap:wrap;gap:12px">
<a class="btn btn-primary" href="about.html">About me {ic('arrow')}</a>
</div>
</div>
<div class="hero-photo"><img src="images/headshot.jpg?v={VER}" alt="Md Sabbir Ahmed"></div>
</section>

<section class="section" aria-labelledby="feat-title">
<div class="row-head">
<h2 class="section-title" id="feat-title">Latest research</h2>
<a href="research.html" style="font-weight:700">See all 38 papers {ic('arrow')}</a>
</div>
<div class="papers three">{FEATURED}</div>
</section>

<section class="section" style="padding-top:0" id="latest" aria-labelledby="latest-title">
<div class="row-head">
<div><span class="brand-kicker">Latest posts</span><h2 class="section-title brand-title" id="latest-title">{ic('stopwatch')}2-Minute Public Health</h2></div>
<a href="blog.html" style="font-weight:700">See all posts {ic('arrow')}</a>
</div>
<div class="grid">{post_cards}</div>
</section>

<section aria-label="Facebook">
<a class="fb-strip" href="{fb_page}">
<span class="logo fb-logo"><span class="fallback">{ic('chat')}</span><img src="images/logos/facebook.png" alt="" onerror="this.remove()"></span>
<span class="fb-strip-text"><strong>Looking for career and graduate study opportunities?</strong><span>Follow EpiTalk with Sabbir on Facebook for public health job postings and study opportunities in Canada and around the world.</span></span>
<span class="fb-strip-cta">Follow EpiTalk {ic('arrow')}</span>
</a>
</section>
</div>'''

open(f'{OUT}/index.html', 'w').write(page(
    'Md Sabbir Ahmed | Epidemiologist', 'Md Sabbir Ahmed is an epidemiologist in Saskatchewan, Canada, working on childhood immunization surveillance and population health research.', 'Home', home, PERSON_LD))

# ---------- ABOUT ----------
edu = [
    ('usask.png', 'USask', 'MSc, Community and Population Health Science', 'Department of Community Health and Epidemiology, College of Medicine, University of Saskatchewan, Canada', '2023'),
    ('pstu.png', 'PSTU', 'MS, Nutrition and Food Science', 'Major in Community Health and Hygiene, Patuakhali Science and Technology University, Bangladesh', '2021'),
    ('pstu.png', 'PSTU', 'BSc (Hons), Nutrition and Food Science', 'Patuakhali Science and Technology University, Bangladesh', '2019'),
]
edu_tiles = ''.join(f'''<div class="tile">
{logo(f, fb, 'edu-logo')}
<div><span class="year">{y}</span><h3>{E(d)}</h3></div>
<p class="meta">{E(m)}</p>
</div>''' for f, fb, d, m, y in edu)

jobs = [
    dict(id='moh', current=True, file='gov-sk.png', fb='SK', title='Epidemiologist', org='Ministry of Health, Government of Saskatchewan',
         when='Sep 2024 – present', duties=[
            ('db', 'Analyze administrative health data from Panorama and other databases, such as the Discharge Abstract Database, for surveillance and reporting in SAS.'),
            ('doc', 'Write briefing notes and reports on immunization coverage for vaccine-preventable diseases, and submit data to the Public Health Agency of Canada.'),
            ('chat', "Handle data requests from the Minister's office, media and external partners."),
            ('link', 'Oversee external research projects: data extraction, data linkage, data sharing agreements and guidance for data analysts.'),
            ('shield', 'Support the Communicable Disease team with immunization surveillance during public health events and emergencies.'),
            ('users', "Lead and work with multidisciplinary teams to deliver the branch's workplan."),
         ], projects=[]),
    dict(id='spheru', current=False, file='spheru.png', fb='SPHERU', title='Research Officer',
         org='Saskatchewan Population Health and Evaluation Research Unit (SPHERU), University of Saskatchewan',
         when='Sep 2023 – Aug 2024', duties=[
            ('chart', 'Analyzed survey data and shared findings with researchers, policymakers and the public.'),
            ('pen', 'Wrote manuscripts, reports, research briefs and posters.'),
            ('home', "Analyzed Canadian Housing Survey data in Statistics Canada's Research Data Centre, including access, security and vetting requests."),
            ('globe', 'Analyzed Mozambique Demographic and Health Survey data for a maternal health project.'),
            ('coin', 'Helped write and submit a CIHR grant application.'),
            ('users', 'Led a working group and helped steer research decisions with a multidisciplinary team.'),
         ], projects=['Building Back Better', 'People, Places, Policies and Prospects: affordable rental housing', 'Mozambique-Canada Maternal Health Project', 'Long COVID Web (CIHR-funded)', 'Mental Health and COVID-19 in Saskatchewan Adults', 'Remember Rebuild Saskatchewan']),
]
def status(j):
    return ('<span class="status now">Current</span>' if j['current'] else '<span class="status past">Former</span>')
job_tiles = ''.join(f'''<button class="tile" type="button" data-open="dlg-{j['id']}">
<div class="tile-top">{logo(j['file'], j['fb'], 'edu-logo')}{status(j)}</div>
<div><h3>{E(j['title'])}</h3><p class="meta" style="margin-top:4px">{E(j['org'])}</p></div>
<p class="meta">{E(j['when'])}</p>
<span class="hint">{'What I do here' if j['current'] else 'What I did here'} {ic('arrow')}</span>
</button>''' for j in jobs)

def dialog(j):
    duties = ''.join(f'<li><span class="ico">{ic(i)}</span><span>{E(t)}</span></li>' for i, t in j['duties'])
    proj = ''
    if j['projects']:
        proj = '<h4>Projects</h4><div style="display:flex;flex-wrap:wrap;gap:8px">' + ''.join(
            f'<span class="pill pill-blue">{E(p)}</span>' for p in j['projects']) + '</div>'
    return f'''<dialog id="dlg-{j['id']}" aria-labelledby="dlg-{j['id']}-t">
<div class="dlg-head">{logo(j['file'], j['fb'], 'edu-logo dlg-logo')}<div><h3 id="dlg-{j['id']}-t">{E(j['title'])}</h3><p>{E(j['org'])}</p></div>
<button class="dlg-close" type="button" data-close aria-label="Close">{ic('x')}</button></div>
<div class="dlg-body"><h4>{'What I do' if j['current'] else 'What I did'}</h4><ul class="duties">{duties}</ul>{proj}</div>
</dialog>'''

awards = [
    ('cap', 'pill-mint', "Dean's Scholarship", '2021 · University of Saskatchewan · MSc program', 36000, ''),
    ('trophy', 'pill-mint', 'Best research poster award', '2023 · Graduate Research Conference, Graduate Students\' Association, University of Saskatchewan', 500, ''),
    ('plane', 'pill-blue', 'Travel award', '2023 · College of Medicine, University of Saskatchewan · Canadian Society for Epidemiology and Biostatistics Conference, Halifax', 1500, ''),
    ('plane', 'pill-blue', 'Travel award', '2022 · College of Medicine, University of Saskatchewan · Canadian Conference on Global Health, Toronto', 2000, ''),
    ('plane', 'pill-blue', 'Travel award', '2022 · Bangladesh-Sweden Trust Fund · travel to Canada for graduate study', 500, '≈'),
]
total = sum(a[4] for a in awards)
def award_li(i, c, t, m, v, eq):
    if t == "Dean's Scholarship":
        return f'''<li class="feature"><span class="award-ico feat-ico">{ic(i)}</span>
<span class="what"><strong>{E(t)}</strong><span>{E(m)}</span></span>
<span class="amt">{eq}CA${v:,}</span></li>'''
    return f'''<li><span class="award-ico pill {c}">{ic(i)}</span>
<span class="what"><strong>{E(t)}</strong><span>{E(m)}</span></span>
<span class="amt">{eq}CA${v:,}</span></li>'''
award_items = ''.join(award_li(*a) for a in awards)

grants = [
    ('Young Researchers Fellowship grant', '2021 · Share-Net Bangladesh', 2500, 'Project',
     'Perceptions on the effect of climate change on child marriage in Bhola district: a qualitative exploration based on the social ecological model',
     'https://doi.org/10.13140/RG.2.2.29623.60323'),
    ('Young Researchers Fellowship grant', '2019 · WaterAid Bangladesh', 1000, 'Project',
     'Availability and quality of WASH infrastructure in community clinics and associated factors: a cross-sectional mixed-method study in rural coastal Bangladesh',
     'https://doi.org/10.13140/RG.2.2.29654.83522'),
    ('National Science and Technology Fellowship', '2020 · Ministry of Science and Technology, Bangladesh', 650, 'Purpose',
     'To support MS thesis research at Patuakhali Science and Technology University', ''),
]
grant_total = sum(g[2] for g in grants)
grant_items = ''.join(f'''<li><span class="award-ico pill pill-mint">{ic('flask')}</span>
<span class="what"><strong>{E(t)}</strong><span>{E(m)}</span>
<span class="proj">{lbl}: {E(pt)}</span></span>
<span class="amt">≈CA${v:,}</span></li>''' for t, m, v, lbl, pt, u in grants)

software = [('sas.png', 'SAS', 'SAS'), ('sql.png', 'SQL', 'SQL'), ('r.png', 'R', 'R'), ('powerbi.png', 'BI', 'Power BI'),
            ('arcgis.png', 'GIS', 'ArcGIS'), ('msoffice.png', 'MS', 'Microsoft Office'), ('canva.png', 'Ca', 'Canva')]
skill_groups = [
    ('db', 'Programming and data management', ['SAS programming: Base SAS, macros and PROC SQL', 'R', 'Data cleaning, linkage and validation']),
    ('chart', 'Analytical methods', ['Regression modelling', 'Multilevel modelling', 'Spatial analysis and mapping', 'Survey data analysis']),
    ('shield', 'Health data I have worked with', ['Panorama immunization data', 'Discharge Abstract Database (DAD)', 'Canadian Housing Survey', 'Demographic and Health Surveys (DHS)', 'Multiple Indicator Cluster Surveys (MICS)', 'Global School-based Student Health Survey (GSHS)']),
    ('pen', 'Communication', ['Briefing notes', 'Scientific manuscripts', 'Research posters', 'Data visualization (Power BI, ArcGIS)']),
]
skill_group_html = ''.join(f'''<div class="sk-group"><div class="sk-head"><span class="ico">{ic(i)}</span><h3>{E(h)}</h3></div>
<ul class="sk-tags">{''.join(f'<li>{E(t)}</li>' for t in tags)}</ul></div>''' for i, h, tags in skill_groups)
skill_items = ''.join(f'<div class="skill">{logo(f, fb, "skill-logo")}<span class="sr-only">{E(n)}</span></div>' for f, fb, n in software)

about = f'''<div class="wrap">
<section class="summary" aria-labelledby="about-title">
<img src="images/headshot.jpg?v={VER}" alt="Md Sabbir Ahmed">
<div class="summary-text">
<h1 id="about-title">About me</h1>
<p>As an epidemiologist at the Ministry of Health, Government of Saskatchewan, I work on childhood immunization surveillance. Since 2024, I have been measuring vaccine coverage, reporting to the Public Health Agency of Canada and turning data into briefing notes that support decisions.</p>
<p>I have more than six years of experience managing and analyzing large-scale administrative health data. I hold an MSc in Community and Population Health Science from the University of Saskatchewan, and I have published 38 peer-reviewed articles, 25 of them as lead author.</p>
</div>
</section>

<section class="section" aria-labelledby="edu-title">
<h2 class="section-title" id="edu-title">Education</h2>
<p class="section-sub">From Bangladesh to Canada: my journey from nutrition science to epidemiology.</p>
<div class="grid">{edu_tiles}</div>
</section>

<section class="section" style="padding-top:0" aria-labelledby="work-title">
<h2 class="section-title" id="work-title">Work</h2>
<p class="section-sub">Click a tile to see my role there.</p>
<div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(min(340px,100%),1fr))">{job_tiles}</div>
{''.join(dialog(j) for j in jobs)}
</section>

<section class="section" style="padding-top:0" aria-labelledby="expert-title">
<h2 class="section-title" id="expert-title">Skills</h2>
<p class="section-sub">What I bring to a data or research project.</p>
<div class="sk-grid">{skill_group_html}</div>
</section>

<section class="section" style="padding-top:0" aria-labelledby="skills-title">
<h2 class="section-title" id="skills-title">Software</h2>
<p class="section-sub">The tools I use in my everyday work.</p>
<div class="skills">{skill_items}</div>
</section>

<section class="section" style="padding-top:0" aria-labelledby="awards-title">
<div class="row-head">
<h2 class="section-title" id="awards-title">Scholarships and awards</h2>
<span class="total">Total <b>CA${total:,}</b></span>
</div>
<ul class="awards">{award_items}</ul>
</section>

<section class="section" style="padding-top:0" aria-labelledby="grants-title">
<div class="row-head">
<h2 class="section-title" id="grants-title">Research grants</h2>
<span class="total">Total <b>CA${grant_total:,}</b></span>
</div>
<ul class="awards">{grant_items}</ul>
<p style="font-size:13px;color:var(--muted);margin:10px 4px 0">≈ Canadian-dollar equivalent of an amount paid in another currency.</p>
</section>




</div>'''

about_js = '''<script>
document.querySelectorAll('[data-open]').forEach(function(b){
  b.addEventListener('click',function(){document.getElementById(b.dataset.open).showModal();});
});
document.querySelectorAll('dialog').forEach(function(d){
  d.querySelector('[data-close]').addEventListener('click',function(){d.close();});
  d.addEventListener('click',function(e){if(e.target===d)d.close();});
});
</script>'''
open(f'{OUT}/about.html', 'w').write(page('About me | Md Sabbir Ahmed', 'About Md Sabbir Ahmed, epidemiologist: education at the University of Saskatchewan, work in public health, skills in SAS and R, awards and grants.', 'About me', about, about_js, path='about'))

# ---------- RESEARCH ----------
pubs = sorted(json.load(open('pubs.json')), key=lambda p: -p['n'])
def authors_html(a):
    s = E(a)
    return s.replace('Ahmed MS', '<b>Ahmed MS</b>')
tiles = []
for p in pubs:
    last = p['authors'].rstrip('.').endswith('Ahmed MS') and not p['lead']
    badge = ('<span class="lead role-lead">Lead author</span>' if p['lead'] else
             '<span class="lead role-senior">Senior author</span>' if last else
             '<span class="lead role-co">Co-author</span>')
    tiles.append(f'''<a class="paper" href="https://doi.org/{E(p['doi'])}" target="_blank" rel="noopener" data-lead="{'1' if p['lead'] else '0'}" data-topics="{' '.join(p['topics'])}">
<div class="paper-thumb"><img src="images/papers/p{p['n']:02d}.jpg" alt="First page of the article" loading="lazy"></div>
<div class="paper-top"><span class="j">{E(p['journal'])}</span><span>{p['year']}</span></div>
<div class="paper-body">
<h3>{E(p['title'])}</h3>
</div>
<div class="paper-foot">{badge}<span class="read">Read article {ic('ext')}</span></div>
</a>''')

TOPICS = json.load(open('topics.json'))
from collections import Counter as _C
_cnt = _C(t for p in pubs for t in p['topics'])
TOPIC_BTNS = '<button type="button" aria-pressed="true" data-f="all">All topics (38)</button>' + ''.join(
    f'<button type="button" aria-pressed="false" data-f="{k}">{E(v)} ({_cnt[k]})</button>' for k, v in TOPICS.items())

research = f'''<div class="wrap">
<section class="summary" aria-labelledby="res-title">
<div class="summary-text">
<h1 id="res-title">My Research</h1>
<p>My research covers mental health and substance use, maternal and child health, nutrition, sleep, housing and water and sanitation, in Canada, Bangladesh and Mozambique. Most of it uses large population surveys and administrative health data.</p>
<div class="stats">
<div class="stat"><b>38</b><span>peer-reviewed publications</span></div>
<div class="stat"><b>25</b><span>as lead author</span></div>
<div class="stat"><b>600+</b><span>citations</span></div>
<div class="stat"><b>16</b><span>h-index</span></div>
</div>
<div style="display:flex;flex-wrap:wrap;gap:12px">
<a class="scholar-btn" href="https://scholar.google.com/citations?user=Qf_XbP8AAAAJ&amp;hl=en" target="_blank" rel="noopener"><img src="images/logos/google-scholar.png" alt="Google Scholar"><span>View my profile {ic('ext')}</span></a>
</div>
</div>
</section>

<section class="section" aria-labelledby="pubs-title">
<div class="row-head">
<h2 class="section-title" id="pubs-title">Publications</h2>
<span style="color:var(--muted)">Newest first · click any paper to read it</span>
</div>
<div class="filters" role="group" aria-label="Filter publications by topic">{TOPIC_BTNS}</div>
<label class="lead-toggle"><input type="checkbox" id="leadOnly"> Show only papers where I am lead author</label>
<p class="filter-count" id="filterCount" aria-live="polite">Showing all 38 papers</p>
<div class="papers">{''.join(tiles)}</div>
</section>
</div>'''

res_js = '''<script>
(function(){
  var btns=document.querySelectorAll('.filters button'), lead=document.getElementById('leadOnly'),
      out=document.getElementById('filterCount'), topic='all';
  function apply(){
    var n=0;
    document.querySelectorAll('.paper').forEach(function(p){
      var ok=(topic==='all'||p.dataset.topics.split(' ').indexOf(topic)>-1)&&(!lead.checked||p.dataset.lead==='1');
      p.style.display=ok?'':'none'; if(ok)n++;
    });
    out.textContent='Showing '+n+' paper'+(n===1?'':'s');
  }
  btns.forEach(function(b){b.addEventListener('click',function(){
    topic=b.dataset.f; btns.forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');}); apply();});});
  lead.addEventListener('change',apply);
})();
</script>'''
open(f'{OUT}/research.html', 'w').write(page('My Research | Md Sabbir Ahmed', '38 peer-reviewed publications by epidemiologist Md Sabbir Ahmed on mental health, maternal and child health, chronic disease, sleep, and water and hygiene.', 'My Research', research, res_js, path='research'))

open(f'{OUT}/images/logos/README.txt', 'w').write('''Put logo image files in this folder with exactly these names (PNG, square works best).
Until a file is here, the site shows a small text badge in its place.

usask.png          University of Saskatchewan
pstu.png           Patuakhali Science and Technology University
gov-sk.png         Government of Saskatchewan
spheru.png         SPHERU
linkedin.png       LinkedIn
google-scholar.png Google Scholar
researchgate.png   ResearchGate
sas.png r.png stata.png spss.png sql.png powerbi.png arcgis.png panorama.png excel.png canva.png
''')
print('built', total)


# ---------- BLOG ----------
feat = POSTS[0]
fpill = THEME_STYLE[feat['theme']][0]
blog_cat_btns = '<button type="button" aria-pressed="true" data-c="all">All posts</button>' + ''.join(
    f'<button type="button" aria-pressed="false" data-c="{E(c)}">{E(c)}</button>' for c in BLOG_CATS)
blog_cards = ''.join(post_card(p, 'blog-card') for p in POSTS)
blog = f'''<div class="wrap">
<section class="summary" aria-labelledby="blog-title">
<div class="summary-text">
<span class="brand-kicker">Blog</span>
<h1 id="blog-title" class="brand-title">{ic('stopwatch')}2-Minute Public Health</h1>
<p class="brand-tag">Public health insights you can read in 2 minutes. By Sabbir Ahmed, epidemiologist.</p>
<p>I write about global health hot topics, how to read health data, public health essentials, and careers and higher study in public health.</p>
</div>
</section>

<section class="section" aria-label="Featured post">
<a class="feature-post" href="{post_url(feat)}">
{post_img(feat, 'feature-img')}
<div class="feature-body">
<span class="pill {fpill}" style="align-self:flex-start">{E(feat['theme'])}</span>
<h2>{E(feat['title'])}</h2>
<p class="excerpt">{E(feat['summary'])}</p>
<p class="meta-line">{E(feat['date'])} · {E(feat['read'])}</p>
<span class="btn btn-primary" style="align-self:flex-start">Read the post {ic('arrow')}</span>
</div>
</a>
</section>

<section class="section" style="padding-top:0" aria-labelledby="all-posts-title">
<h2 class="section-title" id="all-posts-title">All posts</h2>
<div class="filters blog-filters" role="group" aria-label="Filter posts by theme">{blog_cat_btns}</div>
<p class="empty-note" id="emptyNote" hidden>No posts in this theme yet. Coming soon.</p>
<div class="grid">{blog_cards}</div>
</section>
</div>'''
blog_js = '''<script>
(function(){
  var b=document.querySelectorAll('.blog-filters button'), note=document.getElementById('emptyNote');
  b.forEach(function(x){x.addEventListener('click',function(){
    b.forEach(function(y){y.setAttribute('aria-pressed',y===x?'true':'false');});
    var n=0;
    document.querySelectorAll('.blog-card').forEach(function(c){var ok=(x.dataset.c==='all'||c.dataset.cat===x.dataset.c);c.style.display=ok?'':'none';if(ok)n++;});
    note.hidden=n>0;
  });});
})();
</script>'''
open(f'{OUT}/blog.html', 'w').write(page('Blog | Md Sabbir Ahmed', 'Public health explained in plain language: health news, how to read health numbers, and career tips, written by epidemiologist Md Sabbir Ahmed.', 'Blog', blog, blog_js, path='blog'))

# ---------- ONE PAGE PER POST ----------
def body_html(blocks):
    out = []
    for kind, val in blocks:
        if kind == 'h': out.append(f'<h2>{E(val)}</h2>')
        elif kind == 'p': out.append(f'<p>{E(val)}</p>')
        elif kind == 'ul': out.append('<ul>' + ''.join(f'<li>{E(i)}</li>' for i in val) + '</ul>')
    return '\n'.join(out)
for i, p in enumerate(POSTS):
    pill = THEME_STYLE[p['theme']][0]
    srcs = ''.join(f'''<li>{E(a) + ' ' if a else ''}<a href="{E(u)}" target="_blank" rel="noopener">{E(t)}</a>{(' ' + E(x)) if x else ''}</li>''' for a, t, u, x in p['sources'])
    others = [q for q in POSTS if q is not p][:2]
    more = ''.join(post_card(q, data=False) for q in others)
    art = f'''<div class="wrap">
<article class="post" aria-labelledby="post-title">
<a class="back" href="blog.html">{ic('arrow')}<span>Back to all posts</span></a>
<span class="brand-kicker brand-title">{ic('stopwatch')}2-Minute Public Health</span>
<span class="pill {pill}">{E(p['theme'])}</span>
<h1 id="post-title">{E(p['title'])}</h1>
<p class="meta-line">By Md Sabbir Ahmed · {E(p['date'])} · {E(p['read'])}</p>
{post_img(p, 'post-hero')}
<div class="post-body">
{body_html(p['body'])}
<h2>Sources</h2>
<ul class="sources">{srcs}</ul>
</div>
</article>
{('<section class="section" aria-labelledby="more-title"><h2 class="section-title" id="more-title">More posts</h2><div class="grid">' + more + '</div></section>') if more else ''}
</div>'''
    open(f'{OUT}/{post_url(p)}', 'w').write(page(f"{p['title']} | Md Sabbir Ahmed", p['summary'], 'Blog', art, og_img=f"images/blog/{p['image']}", path=post_url(p)[:-5]))

# ---------- WORK WITH ME ----------
MAIL = 'mailto:sabbir.epidemiologist@gmail.com'
work = f'''<div class="wrap">
<section class="summary" aria-labelledby="work-page-title">
<div class="summary-text">
<span class="pill pill-mint" style="font-size:14px;padding:7px 14px">Open to collaboration and mentoring</span>
<h1 id="work-page-title" style="margin-top:14px">Want to work with me?</h1>
<p>I am happy to work with researchers and students. Here are two ways we can work together.</p>
</div>
</section>

<section class="section" aria-label="Ways to work together">
<div class="offer-grid">
<div class="offer">
<span class="ico">{ic('users')}</span>
<h2>Research collaboration</h2>
<p>Do you have a research idea or project? Send me a short note about it. Then we will set up a call to talk more.</p>
<ol class="mini-steps"><li>Send me a note about your project</li><li>We set up a call</li><li>We plan the work together</li></ol>
<a class="btn btn-primary" href="{MAIL}?subject=Research%20collaboration">{ic('mail')} Send me a note</a>
</div>
<div class="offer">
<span class="ico">{ic('cap')}</span>
<h2>Research mentoring</h2>
<p>Do you need help with research, writing a paper or applying for graduate study? Email me to find out more.</p>
<a class="btn btn-primary" href="{MAIL}?subject=Research%20mentoring">{ic('mail')} Email me</a>
</div>
</div>
</section>

<section aria-label="Note on independence">
<p class="indep"><svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/></svg><span class="sr-only">Note: </span>My collaboration and mentoring work is independent of my current employment.</p>
</section>
</div>'''
open(f'{OUT}/work.html', 'w').write(page('Work with me | Md Sabbir Ahmed', 'Work with epidemiologist Md Sabbir Ahmed on research collaboration or get research mentoring.', 'Want to work with me?', work, path='work'))


# ---------- GALLERY ----------
gallery = f'''<div class="wrap">
<section class="summary" aria-labelledby="gallery-title">
<div class="summary-text">
<h1 id="gallery-title">Gallery</h1>
<p>Photos from conferences, presentations, fieldwork and awards.</p>
</div>
</section>
<section class="section">
<div class="soon">
<span class="soon-ico">{ic('image')}</span>
<h2>Coming soon</h2>
<p>I am putting together photos to share here. Please check back later.</p>
</div>
</section>
</div>'''
open(f'{OUT}/gallery.html', 'w').write(page('Gallery | Md Sabbir Ahmed', 'Photos from conferences, presentations, fieldwork and awards.', 'Gallery', gallery, path='gallery').replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"', 1))


# ---------- SEO: sitemap + robots ----------
import datetime as _dt, glob as _glob, os as _os
_today = _dt.date.today().isoformat()
_pages = [''] + [_os.path.basename(f)[:-5] for f in sorted(_glob.glob(f'{OUT}/*.html')) if not f.endswith(('index.html','404.html','gallery.html'))]
open(f'{OUT}/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{SITE_URL}{p}</loc><lastmod>{_today}</lastmod></url>\n' for p in _pages) + '</urlset>\n')
open(f'{OUT}/robots.txt','w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n')
