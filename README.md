# abdessamadaitbrahim.github.io

Personal portfolio of Abdessamad Ait Brahim: a static site in HTML, CSS and JavaScript, with no framework, hosted on GitHub Pages.

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
- `python tools/make_icons.py`: regenerates the header photo (`abdessamad-prof-96/192.webp`) and the circular favicons (`favicon.ico`, 32 / 180 / 512 px PNGs) from `incoming/site/abdessamad-prof.png`.
- `python tools/import_incoming.py`: copies the publishable hackathon files from the private, git-ignored
  `incoming/` folder into `assets/hackathons/` and `assets/volunteering/` (WebP images including event photos, lighter PDFs,
  a redacted Youthpass without the birth date and place; needs Pillow and pypdf, plus pypdfium2 for the Youthpass step).

The CV download appears when `assets/cv/Abdessamad_Ait_Brahim_CV.pdf` exists.
