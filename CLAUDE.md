# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GO SEMI & BEYOND is the static site mockup for Advantest's semiconductor industry newsletter website. The newsletter focuses on semiconductor test innovation, industry trends, and emerging technologies.

**Publication Details:**
- Quarterly publication (January, April, July, October)
- Target Audience: Semiconductor test professionals, engineers, and industry decision-makers

## Project Structure

```
GOSEMI/
├── docs/                   # Built output for GitHub Pages (auto-generated)
├── static_mockup/          # Static HTML/CSS/JS design mockup
│   ├── src/                # Source templates (edit these!)
│   │   ├── partials/       # Reusable template partials
│   │   │   ├── header.html # Site header with navigation
│   │   │   ├── footer.html # Site footer
│   │   │   └── head.html   # HTML head (meta, CSS, fonts)
│   │   ├── index.html      # Homepage template (current issue)
│   │   ├── about.html      # About page template
│   │   ├── archive.html    # Newsletter archive template
│   │   ├── subscribe.html  # Subscription page template
│   │   ├── sponsors.html   # Sponsors page template
│   │   └── article.html    # Article page template
│   ├── build.py            # Template build script
│   ├── css/
│   │   └── style.css       # Main stylesheet
│   ├── js/
│   │   └── main.js         # Main JavaScript
│   └── images/
│       ├── sponsors/       # Sponsor logo images
│       └── [logos & placeholders]
├── CLAUDE.md               # This file
└── .gitignore
```

## Templating System

The project uses a simple Python-based templating system with partials.

**Template Syntax:**
```html
{{> partial_name }}
```
This includes the content of `src/partials/partial_name.html`.

**Building Templates:**
```bash
cd static_mockup
python3 build.py
```

This processes all `.html` files in `src/` (except partials), replaces partial includes, and outputs to the `/docs` directory for GitHub Pages deployment.

**Watch Mode:**
```bash
python3 build.py --watch
```

**Development Workflow:**
1. Edit templates in `src/` directory
2. Run `python3 build.py` to compile
3. View output in `/docs` folder in browser

## Deployment (GitHub Pages)

The site is configured for GitHub Pages deployment from the `/docs` folder on the `main` branch.

**To deploy:**
1. Run the build: `cd static_mockup && python3 build.py`
2. Commit and push to `main` branch
3. Configure GitHub Pages in repo settings:
   - Go to Settings > Pages
   - Source: Deploy from a branch
   - Branch: `main` / `/docs`
   - Save

The site will be available at: `https://<username>.github.io/<repo-name>/`

## Site Pages

**Homepage (index.html)**
- Hero section with newsletter title and CTA buttons
- Featured article section (top story)
- Article grid (In This Issue section)
- Featured Products section
- Sidebar with subscribe widget, recent issues, podcast spotlight, sponsors
- Featured Events section
- Subscribe CTA

**About Page (about.html)**
- Publication description and mission
- Content categories covered
- Publication schedule
- Team information
- Contact details

**Archive Page (archive.html)**
- Grid of past newsletter issues organized by year
- Issue cards with title, date, and topic summary

**Subscribe Page (subscribe.html)**
- Large subscription form
- Benefits of subscribing
- FAQ section

**Sponsors Page (sponsors.html)**
- Sponsorship information and benefits
- Sponsor tiers (Platinum, Gold, Silver)
- Contact CTA

**Article Page (article.html)**
- Full article layout with header, hero image, body content
- Related articles section

## Design System

**Brand Colors (CSS Variables):**
- Primary: `--COLOR_BRAND_PRIMARY: #91003c` (Burgundy/Maroon)
- Secondary: `--COLOR_BRAND_SECONDARY: #c31f66` (Pink)
- Accent: `--COLOR_BRAND_SUB_2: #007B7F` (Teal)
- Plus additional brand sub-colors

**Typography:**
- Font Family: 'Open Sans', Roboto, sans-serif
- Google Fonts: Open Sans (weights: 400, 600, 700)

**Layout:**
- Container max-width: 1200px
- Responsive design with mobile breakpoints

## JavaScript Functionality

**main.js includes:**
- Dropdown menu toggle and close-on-outside-click
- Mobile navigation setup
- Smooth scrolling for anchor links
- Newsletter subscription form handler
- Lazy image loading

## Content Sections (from Newsletter)

Based on the draft content document, the newsletter includes:
- **Top Stories** — Technical articles (e.g., Singulated Die Test, Digital Twins & AI/ML)
- **Executive Viewpoints** — Industry leader perspectives
- **Spotlight on Business** — Executive interviews
- **Featured Products** — New Advantest products
- **Featured Events** — Event coverage and upcoming events
- **Podcast Spotlight** — Industry podcast features
- **ESG Spotlight** — Sustainability initiatives
- **Advantest in the News** — Press coverage
- **Upcoming Events** — Calendar of events
- **On the Lighter Side** — Fun content
- **GO POLL** — Reader poll

## WordPress Theme Conversion Notes

When converting to WordPress:

1. **Template Hierarchy:**
   - index.html → front-page.php
   - archive.html → archive.php or page-archive.php
   - article.html → single.php
   - Header/footer extracted to header.php/footer.php

2. **Dynamic Content:**
   - Articles: Custom Post Type for newsletter articles
   - Issues: Custom taxonomy for organizing by issue
   - Sponsors: Custom Post Type with logo uploads
   - Subscribe: Newsletter plugin integration

3. **Asset Management:**
   - CSS/JS enqueued via functions.php
   - Images uploaded to WordPress Media Library

## Contact Information

- General: corpcomms@advantest.com
- Marketing: mktgcomms@advantest.com
