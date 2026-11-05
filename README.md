# abdessamadaitbrahim.github.io

Personal portfolio of Abdessamad Ait Brahim. Plain HTML, CSS and JavaScript, no framework, hosted on GitHub Pages.

## Structure

- `index.html`, `about.html`, `projects.html`, `education.html`, `experience.html`, `hackathons.html`,
  `volunteering.html`, `honors.html`, `cv.html`, `contact.html`
- `projects/<slug>.html`: one case study per project
- `hackathons/<slug>.html`: one page per hackathon
- `assets/css/style.css`, `assets/js/main.js`, `assets/img/`, `assets/hackathons/`, `assets/cv/`

All HTML pages, `404.html`, `sitemap.xml`, `robots.txt` and `favicon.svg` are generated. Do not edit them by hand.

## Updating the site

1. Edit the content in `tools/make_content.py` (projects, experience, education, hackathons, volunteering, honors, skills, languages).
2. Regenerate:

   ```bash
   python tools/make_content.py
   python tools/build.py
   ```

Other scripts:

- `python tools/make_og.py`: regenerates the Open Graph image `assets/img/site/og.png` (Pillow).
- `python tools/make_icons.py`: regenerates the portrait icons (header avatar, `favicon.ico`, 32 / 180 / 512 px PNGs).
- `python tools/import_incoming.py`: copies the publishable hackathon files from the private, git-ignored
  `incoming/` folder into `assets/hackathons/` (WebP images including event photos, lighter PDFs; needs Pillow and pypdf).

The CV download appears when `assets/cv/Abdessamad_Ait_Brahim_CV.pdf` exists.
