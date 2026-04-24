# CLAUDE.md — Codebase Index

> **If you are an LLM modifying this repository:**
> 1. Update the relevant sections of this file to reflect your changes before finishing.
> 2. **Anti-AI defense is a hard requirement.** Every new page, layout, or include you create MUST follow the anti-AI defense checklist in the "Anti-AI Defense" section below. Do not skip this, even for dev-only pages.
>
> Last updated: 2026-04-24

## Project Overview

Jekyll 3.8 personal website and blog for **Ryan Ye** (CS @ Cornell). Deployed on GitHub Pages at `ryanmye.github.io/aboutme`. Features data-driven pages (homepage bio, projects, research, CV), a 5-theme color system, a local blog editor + standalone album editor with Sinatra API, standalone photo albums (Jekyll collection), a gallery page, and automated Spotify "recently played" integration via GitHub Actions.

## Quick Reference

```bash
# Local development (Jekyll)
bundle exec jekyll serve --livereload --baseurl ""

# Local editor server (separate terminal, port 4001)
bundle exec ruby scripts/local_editor_server.rb

# Production build (CI uses both configs)
bundle exec jekyll build --config _config.yml,_config_prod.yml
```

- **Base URL:** `/aboutme` (GitHub Pages project site)
- **Permalink format:** `/blog/:year/:month/:day/:title/`
- **Themes:** 5 color themes via CSS custom properties — warm (default), linen, pure, barely, dark-mono
- **Fonts:** Inter (body), DM Serif Display (headings/brand), JetBrains Mono (code)
- **Spotify:** GitHub Actions updates `_data/now-playing.json` every 30 minutes

## Directory Tree

```
.
├── _config.yml              # Main Jekyll config
├── _config_prod.yml         # Production overrides (disables editor)
├── Gemfile                  # Ruby deps: jekyll 3.8, sinatra, kramdown-parser-gfm
├── .gitignore
├── CLAUDE.md                # This file (excluded from Jekyll build)
├── robots.txt               # Anti-AI crawler rules (blocks GPTBot, CCBot, etc.)
├── ai.txt                   # Machine-readable AI opt-out (Spawning.ai standard)
│
├── _layouts/
│   ├── default.html         # Base layout (head + navbar + footer + theme.js)
│   ├── post.html            # Blog post layout (title, date, tags, album grid, prev/next nav)
│   ├── album.html           # Standalone album detail page layout
│   ├── editor.html          # Local editor layout (Toast UI Editor, dev-only)
│   └── album-editor.html   # Album editor layout (dev-only, tabs for post/standalone albums)
│
├── _includes/
│   ├── head.html            # <head>: meta, OG tags, fonts, CSS
│   ├── navbar.html          # Sticky nav, 5-theme dots, mobile hamburger menu
│   └── footer.html          # Copyright, social links, faith statement
│
├── _data/
│   ├── about.yml            # Bio (long + short), interests, education, skills, teaching, honors, blog_blurb
│   ├── projects.yml         # 5 portfolio projects with tags/descriptions (3 have cv: true)
│   ├── research.yml         # Research positions (2), publications, interests
│   └── now-playing.json     # Spotify track (auto-updated by GitHub Actions)
│
├── _posts/                  # Blog posts (YYYY-MM-DD-slug.md) — currently 3 posts
├── _drafts/                 # Unpublished drafts (slug.md) — currently 2 drafts
├── _albums/                 # Standalone photo albums (slug.md, Jekyll collection)
│
├── index.md                 # Homepage (profile + research + blog + selected pubs, Spotify widget)
├── blog.md                  # Blog listing
├── projects.md              # Projects showcase
├── research.md              # Research page
├── cv.md                    # CV page (data-driven from about.yml, research.yml, projects.yml)
├── publications.md          # All publications listing (pub-tiles, no filter)
├── editor.md                # Editor page (dev-only)
├── album-editor.md          # Album editor page (dev-only)
├── gallery.md               # Photo gallery page (album cards + all photos grid)
├── now-playing.json.html    # Exposes _data/now-playing.json as static JSON endpoint
│
├── assets/
│   ├── css/styles.css       # Full stylesheet (~25 sections)
│   ├── js/theme.js          # Theme switcher (localStorage persistence)
│   ├── js/editor.js         # Post editor UI (CRUD, image upload, Toast UI)
│   ├── js/album-editor.js   # Album editor UI (post albums + standalone albums + image deletion)
│   └── images/
│       ├── headshot.jpeg    # Profile photo
│       ├── posts/           # Published post images (timestamped)
│       ├── drafts/          # Draft post images (gitignored)
│       └── albums/          # Standalone album images
│
├── scripts/
│   ├── local_editor_server.rb      # Sinatra REST API for editing (port 4001)
│   ├── migrate_images_to_figures.rb # Converts md images to <figure> blocks
│   ├── extract_base64_images.rb     # Extracts inline base64 to files
│   ├── backfill_titles.rb           # Auto-generates missing post titles
│   └── get-spotify-refresh-token.py # One-time Spotify OAuth setup
│
├── .github/workflows/
│   └── update-spotify.yml   # Cron job: fetch Spotify → commit now-playing.json
│
├── _editor_tmp/             # Temp images during editing (not committed)
├── _site/                   # Built output (not committed)
├── 25Dec_Ye_Ryan_Resume.pdf # PDF resume
├── README.md                # Setup instructions
└── LOCAL_DEV.md             # Local dev guide
```

---

## Configuration Files

### _config.yml (~50 lines)
Main Jekyll configuration. Key settings:
- `title: "Ryan Ye"`, `baseurl: "/aboutme"`, `url: "https://ryanmye.github.io"`
- `twitter_username: "ryanmye0"` — used for Twitter Card meta tags
- `markdown: kramdown` with GFM input, Rouge syntax highlighter
- `permalink: /blog/:year/:month/:day/:title/`
- `local_editor: true` — enables editor nav link and page in development
- `plugins: [jekyll-sitemap, jekyll-feed]` — auto-generates `sitemap.xml` and `feed.xml`
- `collections.albums`: `output: true`, `permalink: /albums/:title/` — standalone album Jekyll collection
- Defaults: `post` layout applied to all files in `_posts/`, `album` layout applied to all files in `_albums/`
- Excludes: README.md, CLAUDE.md, Gemfile, Gemfile.lock, node_modules, vendor

### _config_prod.yml (5 lines)
Production overlay (used in CI build). Overrides:
- `local_editor: false` — hides editor
- Excludes `editor.md`, `album-editor.md`, and `scripts/local_editor_server.rb` from build

### Gemfile
Dependencies: `jekyll ~> 3.8`, `webrick ~> 1.7`, `kramdown-parser-gfm`, `ffi ~> 1.15`, `jekyll-sitemap`, `jekyll-feed`, `sinatra ~> 3.0` (development group)

---

## Layouts

### _layouts/default.html (25 lines)
Base HTML5 layout for all non-post, non-album pages. Includes `head.html`, `navbar.html`, `footer.html`. Loads `theme.js` before `</body>`. Also conditionally loads `album-lightbox.js` when the page sets `album_lightbox: true` in its front matter (currently used by `gallery.md`). **Used by:** `index.md`, `blog.md`, `projects.md`, `research.md`, `publications.md`, `cv.md`, `gallery.md`.

### _layouts/post.html (97 lines)
Blog post layout. Renders: `<article>` with title, ISO 8601 date (`date_to_xmlschema`), human-readable date (`"%B %-d, %Y"`), tag list (iterates `page.tags`), post content, optional photocard album grid (if `page.images` present — each image wrapped in `<button class="album-photo-trigger">` for lightbox), previous/next navigation links. Includes BlogPosting JSON-LD structured data (headline, datePublished, author, image, keywords). Loads `theme.js` and `album-lightbox.js`. **Used by:** all files in `_posts/` via default collection config.

### _layouts/album.html (53 lines)
Standalone photo album detail page layout. Renders: title, date, optional description, photocard grid of `page.images` (`<figure>` + `<button class="album-photo-trigger">` + `<figcaption>`), and a "Back to gallery" link. Loads `theme.js` and `album-lightbox.js` for lightbox support. **Used by:** all files in `_albums/` via default collection config. Permalink: `/albums/:title/`.

### _layouts/editor.html (105 lines)
Local blog post editor layout. Loads Toast UI Editor CSS/JS. Contains: post title input, datetime picker, tags input, draft checkbox, Toast UI Editor div, image upload form (file + caption + upload button), action buttons (new/save/publish/delete), post list sidebar. Includes inline CSS that highlights editor "Caption:" hints (stripped on publish). **Conditionally rendered:** only when `site.local_editor == true` AND `jekyll.environment == "development"`. Loads `editor.js`.

### _layouts/album-editor.html (80 lines)
Local album editor layout. Contains: standalone album metadata section (title, description with 500-char counter, draft checkbox — hidden for post albums), album image upload row, album items grid (with captions and delete buttons), action buttons (new/save/delete), and a tabbed sidebar ("Post Albums" / "Standalone Albums") with two lists. **Conditionally rendered:** only when `site.local_editor == true` AND `jekyll.environment == "development"`. Loads `album-editor.js`.

---

## Includes

### _includes/head.html (110 lines)
HTML `<head>` contents:
- Meta: charset, viewport, dynamic title, description (priority: `page.description` > `page.excerpt` truncated to 160 chars > `site.description`), author
- Canonical URL: `<link rel="canonical">` using `absolute_url`
- Feed discovery: `{% feed_meta %}` (Atom feed link from jekyll-feed)
- Anti-AI/crawler: `<meta name="robots" content="noai, noimageai">`, `<meta name="tdm-reservation" content="1">`
- Open Graph: type ("article" for posts, "website" otherwise), URL, title, description, site_name, image (post's first image or headshot fallback). Posts also get `article:published_time`, `article:author`, `article:tag`
- Twitter Card: summary card with site handle (@ryanmye0), title, description, image
- CSS: preloads `styles.css` with cache-busting timestamp
- Fonts: Google Fonts preconnect, loads Inter, DM Serif Display, JetBrains Mono
- Font Awesome 6.4.2 (loaded with `media="print" onload` for non-blocking)
- Favicon: inline base64 SVG graduation cap emoji
- JSON-LD structured data: WebSite schema on all pages; Person schema (with `sameAs` links to GitHub, LinkedIn, Twitter, Google Scholar) on homepage only. Person schema includes `jobTitle`, `memberOf`/`affiliation` (Cornell), `knowsAbout` keywords.
- Inline theme-bootstrap `<script>` at end: reads `localStorage.theme` and applies CSS custom properties synchronously to prevent flash of wrong theme on load.

### _includes/navbar.html (55 lines)
Sticky top navigation bar:
- Brand link (`site.author`) to homepage
- 5 theme color dot buttons (`data-theme` attribute) with inline background-color previews
- Nav links (order): about (`/`), research (`/research`), projects (`/projects`), blog (`/blog`), cv (`/cv`). Blog link is also active on `/gallery`. Gallery is linked from blog page header, not navbar.
- Dev-only nav links: editor (`/editor`), albums (`/album-editor`) — between `blog` and `cv`
- Conditional: dev-only links shown only when `site.local_editor == true` AND `jekyll.environment == "development"`
- Mobile: hamburger toggle button (3 spans), click-outside-to-close JS, ARIA attributes
- Active link detection via `page.url` comparison

### _includes/footer.html (16 lines)
Site footer with: dynamic copyright year, "Jesus is King" statement, social links (GitHub, LinkedIn, email from site config). All external links use `target="_blank" rel="noopener noreferrer"`.

---

## Root Pages

### index.md — Homepage
**Layout:** default. **Title:** "Computer Science Student at Cornell University". **Data deps:** `site.data.about.bio_profile`, `site.data.about.education`, `site.data.about.blog_blurb`, `site.data.research.positions` (filtered by `homepage: true`), `site.data.research.publications` (filtered by `selected: true`), `site.posts` (limit 3), `_config.yml` (author, email, github_username, linkedin_username). Has page-specific `description` for SEO meta.

Sections (top to bottom):
1. **Profile card** (`.profile-section`) — two columns:
   - **Left (`.profile-left`):** headshot, name (`site.author`), position ("Computer Science" + Cornell link), social icons (email, GitHub, LinkedIn), "Jesus is King" note.
   - **Right (`.profile-right`):** bio from `site.data.about.bio_profile`, education one-liner (institution · degree · GPA), **Spotify widget** (`#spotify-now-playing` span, populated by inline `<script>` that fetches `/assets/data/now-playing.json` with 5s timeout; helpers: `timeAgo(isoStr)`, `escapeHtml(str)`; renders track name, artists, context (playlist/album/artist), relative time).
2. **Research preview** — from `site.data.research.positions` where `homepage: true`. Uses `position.index_title` and `position.index_description`. Followed by "Selected Publications" subsection (publications where `selected: true`, rendered as `.pub-tile`), with "see more →" link to `/research`.
3. **Blog preview** — `site.data.about.blog_blurb` as subtitle, then table of latest 3 posts (date + title + truncated excerpt).

### blog.md (43 lines) — Blog Listing
**Layout:** default. Lists all `site.posts` in reverse chronological order. Each entry shows date, title link, and truncated excerpt. Page header has a "gallery →" link next to the "Blog" title.

### projects.md (47 lines) — Projects
**Layout:** default. **Data deps:** `site.data.projects.projects`.
Renders project cards by iterating `site.data.projects.projects`. Each card: title (with optional URL link), date range, description, tech tags, bullet points, optional GitHub link.

### research.md (81 lines) — Research
**Layout:** default. **Data deps:** `site.data.research`.
Sections: subtitle, Google Scholar link, selected publications (`where: selected, true`) as `.pub-tile`, "more publications →" link, research positions (with role, lab, description, nested `focus: [{title, detail}]` areas, optional note), research interests.

### publications.md — Publications
**Layout:** default. **Data deps:** `site.data.research.publications`, `site.data.research.google_scholar`.
Shows ALL publications as `.pub-tile` horizontal tiles (no `selected` filter). Linked from "more publications →" on `research.md`.

### cv.md — CV
**Layout:** default. **Data deps:** `site.data.about` (education, skills, teaching, honors), `site.data.research.positions` (filtered by `cv: true`), `site.data.research.publications`, `site.data.projects.projects` (filtered by `cv: true`).
Fully data-driven Liquid template. To add/edit CV content, edit the data files — do not hardcode HTML in this file.

### editor.md (15 lines) — Editor Page
**Layout:** editor. Minimal wrapper that activates the editor layout. Only rendered in development when `local_editor: true`.

### gallery.md — Gallery Page
**Layout:** default. **Permalink:** `/gallery/`. **Front matter:** sets `album_lightbox: true` so `default.html` loads `album-lightbox.js`. Linked from blog page header ("gallery →"). Iterates both `site.posts` and `site.albums` (Jekyll collection), renders album cards for items with `images` frontmatter (cover image, title, date, photo count). Post-album cards link to the post URL; standalone album cards link to `/albums/:slug/`. Below albums, shows "All Photos" as a photocard masonry grid (`.album-grid` / `.album-photo` + `.album-photo-trigger`) matching the blog post / album detail format — clicking any photo opens the full-screen lightbox with prev/next across every photo in document order. A running Liquid counter (`photo_idx`) assigns a global `data-album-index` across both the posts and albums loops. Standalone albums with `draft: true` are excluded.

### album-editor.md — Album Editor Page
**Layout:** album-editor. **Permalink:** `/album-editor/`. Dev-only. Tabbed interface: "Post Albums" tab lists blog posts for managing their photo albums; "Standalone Albums" tab lists standalone albums. Supports creating new standalone albums with title, description (max 500 chars), and draft flag. Removing an image from an album also deletes the file from disk (if not referenced elsewhere). Post albums use `PUT /posts/:kind/:slug/images`; standalone albums use `POST/PUT/DELETE /albums/:slug`.

### now-playing.json.html (5 lines) — Spotify JSON Endpoint
**Layout:** null. **Permalink:** `/assets/data/now-playing.json`.
Outputs `site.data['now-playing']` as JSON via Liquid `jsonify` filter. This is how the homepage JS fetches Spotify data from the static site.

---

## Data Files

> **Contact info lives in `_config.yml`** (`author`, `email`, `github_username`, `linkedin_username`). There is no `_data/profile.yml` — it was removed as a duplicate. Templates use `site.email`, `site.github_username`, `site.linkedin_username`, and `site.author` directly.

### _data/about.yml
Structured personal data:
- `bio`: multi-line description (longer, first-person; reserved — no page currently renders it since `about.md` was removed)
- `bio_profile`: short 1-paragraph intro (used by index.md profile-right column)
- `interests`: list of 4 research areas (ML/CV, AI for science, representation learning, data-efficient learning)
- `education`: institution (Cornell), degree (B.S. CS, College of Engineering), expected May 2028, GPA 4.05, coursework array (joined with ", " for cv.md)
- `skills`: programming (Python, Java, C/C++, OCaml), machine_learning (PyTorch, HF Transformers, NumPy, pandas, Matplotlib), tools (Git, VS Code, Jupyter, IntelliJ, PyCharm, SSH, vibe-coding)
- `teaching`: array of teaching/leadership entries, each with title, date, subtitle, bullets (used by cv.md)
- `honors`: array of honor strings (used by cv.md) — CIDA Grant Recipient, 4× AIME Qualifier, USACO Silver, Conestoga HS CS Award
- `blog_blurb`: one-line tagline under Blog heading on homepage

### _data/projects.yml
Top-level key `projects` — ordered list of 5 projects, each with: `title`, `date` (range string), `description`, `tags` (array), `bullets` (array), optional `url`. Current projects (in order):
1. **Automated Calf Behavior Analysis System** (May 2025 - present) — YOLO/DINO/VLMs for calf posture
2. **Traveling Salesman** (Mar 2026) — hackathon conversational flight search
3. **Sisyphus** (Nov 2025) — AI productivity app, top 5 of 40+ teams
4. **Transformer-Based Piano Melody Generation** (Aug 2023 - Apr 2024)
5. **Personal Website** (Mar 2026) — this site

CV display fields (on 3 projects: Traveling Salesman, Sisyphus, Piano Melody Generation):
- `cv: true` — flags project to appear in cv.md
- `cv_tech` — tech subtitle string shown under project title on CV
- `cv_bullets` — array of resume-style bullet points for CV (may differ from `bullets`)

### _data/research.yml
- `subtitle`: research focus statement
- `google_scholar`: Google Scholar link
- `positions`: 2 entries:
  1. **MABe25 - Animal Behavior Benchmark** (Feb 2025 - Present)
  2. **AI for Animal Behavior Monitoring** (May 2025 - Present) — accepted to ADSA 2026 Poster
  Each entry has `title`, `role`, `lab`, `institution`, `date`, multi-line `description`, and a `focus` array of `{title, detail}` objects (rendered as nested bullets on `research.md`). Position 2 also has `note` (BURE/CIDA grant).
- `publications`: 1 entry (economics paper, 2023) — each publication has `title`, `authors`, `venue`, `url`, `description`, `tags`, `selected` (boolean), plus `cv_year` and `cv_subtitle` for CV display.
- `interests`: 4 research interest areas.

Homepage and CV display fields (on position 2 — AI for Animal Behavior):
- `homepage: true` — flags this position to appear on index.md research preview
- `index_title` — shortened title for homepage display
- `index_description` — homepage-specific summary paragraph (first-person, different from `description`)
- `cv: true` — flags position to appear in cv.md
- `cv_title` — formatted title line for CV (e.g. "Role — Lab")
- `cv_date` — date range string for CV
- `cv_subtitle` — subtitle line for CV (e.g. grant/program info)
- `cv_bullets` — array of resume-style bullet points for CV

### _data/now-playing.json
Auto-updated by GitHub Actions every 30 min. Schema:
```json
{
  "track": {
    "name": "...", "url": "spotify:track:...",
    "artists": [{"name": "...", "url": "..."}],
    "played_at": "ISO8601"
  },
  "fetched_at": "ISO8601",
  "context": { "type": "playlist|album|artist", "name": "...", "url": "..." }
}
```

---

## Blog Posts & Albums

Published posts (in `_posts/`):

| File | Title | Date | Tags |
|------|-------|------|------|
| `2025-12-01-i-was-part-of-an-art-exhibit.md` | I Was Part of an Art Exhibit | Dec 1, 2025 | life-update, i'm an artist now |
| `2026-03-12-research-symposium-accepted.md` | Abstract accepted to ADSA! | Mar 12, 2026 | research, life-update |
| `2026-03-17-first-real-blog-post.md` | first real blog post | Mar 17, 2026 | brief life update, test post |

Unpublished drafts (in `_drafts/`):

| File | Title |
|------|-------|
| `first-post.md` | Hello, World — Welcome to My Blog |
| `spring-semester-started.md` | Spring 2026 Semester Started |

Standalone albums (in `_albums/`):

| File | Title | Date |
|------|-------|------|
| `some-cornell-propoganda.md` | Some Cornell Propoganda | Apr 23, 2026 |

Post front matter schema: `layout: post`, `title`, `date` (YYYY-MM-DD or ISO 8601 with timezone), `tags` (array), optional `excerpt`, optional `images` (array of `{src, caption?}` for photo album — displayed at bottom of post page and on gallery page).

---

## Assets

### assets/css/styles.css (1942 lines)
Single stylesheet. CSS custom properties for theming (11 variables: `--bg`, `--surface`, `--border`, `--text`, `--muted`, `--accent`, `--accent-soft`, `--accent-dark`, `--color-code-bg`, `--color-code-text`, `--theme-dot-border`). Max width: 960px (`--max-width`).

**Section index (line numbers approximate):**

| Line | Section |
|------|---------|
| 1 | CSS Reset & Base |
| 10 | Custom Properties (theme defaults: linen palette) |
| 55 | Base Typography |
| 138 | Layout (site wrapper, container) |
| 159 | Navigation (sticky, al-folio tab style) |
| 290 | Footer |
| 354 | Editor (form styling) |
| 551 | Profile Section (avatar, social, bio, skills, Spotify widget) |
| 706 | Content / Page Sections |
| 730 | Section Headers (blog/page headings) |
| 755 | Page Header (inner pages) |
| 777 | Cards (projects) |
| 855 | Tags |
| 878 | Blog / Post List |
| 916 | Blog Post Page (article, figures, code blocks, album grid) |
| 1055 | Gallery Page (album cards grid) |
| 1106 | Album Detail Page (album grid, photocard styling, description, nav) |
| 1185 | Album Lightbox (fullscreen overlay, prev/next, caption, counter) |
| 1345 | Editor Album Section (thumbnail rows, caption inputs, tabs) |
| 1441 | Research / Publications |
| 1494 | Publication Tiles (horizontal pub-tile cards) |
| 1567 | CV / Resume Page |
| 1687 | Skills list (inline tags) |
| 1708 | Responsive (mobile breakpoints) |
| 1785 | Spotify Widget |
| 1816 | Announcements / News Table (al-folio style) |

Key patterns: always use `var(--name)` for colors, never hardcode hex values in component styles. Reduced-motion media query at L36 disables transitions.

### assets/js/theme.js (108 lines)
IIFE that manages the 5-theme color system:
- **Themes:** warm (cream/terracotta, default), linen (neutral warm), pure (black-on-white), barely (dark warm), dark-mono (dark grayscale)
- **`setTheme(key)`** — applies CSS custom properties to `document.documentElement.style`, saves to `localStorage["theme"]`
- **`updateToggleUI(key)`** — highlights active theme dot button
- Runs synchronously on load (prevents flash of wrong theme)
- Event listeners on `.theme-dot` buttons

### assets/js/album-lightbox.js (~145 lines)
IIFE that powers the album photocard lightbox on post and album pages. **Depends on:** `.album-photo-trigger` buttons rendered by `post.html` / `album.html` with `data-album-index`, `data-full-src`, `data-caption` attributes.

Key behavior:
- On `DOMContentLoaded`, collects all `.album-photo-trigger` buttons on the page. If none, no-ops (no DOM injected, no listeners).
- Injects a single `<div class="album-lightbox" role="dialog" aria-modal="true" hidden>` overlay into `<body>` with close/prev/next buttons, full-size `<img>`, `<figcaption>`, and a counter (`n / total`).
- `showAt(i)` updates image src, alt, caption text, counter. Wraps around via modulo.
- Click a trigger → open at that index; click backdrop or close button → close.
- Keyboard: `Esc` closes; `ArrowLeft` / `ArrowRight` navigate when >1 photo.
- Focus management: saves previously focused element, focuses close button on open, restores focus on close, traps Tab within the overlay.
- Locks body scroll (`document.body.style.overflow = 'hidden'`) while open.
- Sets `data-single="true"` on the overlay when only one photo (hides prev/next and counter via CSS).

### assets/js/editor.js (438 lines)
Blog post editor UI. **Depends on:** Toast UI Editor library (loaded by editor.html layout), `local_editor_server.rb` API on port 4001.

Key functions:
- **`serializeForm()`** — collects title, date, tags, draft status, body, slug from form
- **`toSlug(str)`** — converts titles to URL-safe slugs
- **`refreshPostList()`** — `GET /posts`, renders post/draft list with click-to-load
- **`loadPostIntoForm(post)`** — populates form fields
- **Image upload:** `POST /images` with caption, inserts as markdown `![alt](url)` + `*caption*`. Keyboard shortcut: Cmd+Shift+K (Mac) / Ctrl+Shift+K. Intercepts Toast UI Editor paste to prevent base64 embedding.

API origin configurable via `data-api-origin` attribute (defaults to `http://localhost:4001`).

### assets/js/album-editor.js (445 lines)
Album editor UI with tabs for post albums and standalone albums. **Depends on:** `local_editor_server.rb` API on port 4001.

Key features:
- **Tabbed interface:** "Post Albums" tab lists blog posts; "Standalone Albums" tab lists standalone albums
- **Post albums:** separates body-detected images (read-only, shown dimmed) from album-only images (editable). Saves via `PUT /posts/:kind/:slug/images`
- **Standalone albums:** title, description (max 500 chars with counter), draft checkbox. Saves via `POST/PUT /albums/:slug`
- Upload images to album (up to 25 total), add captions, remove
- **Image deletion:** removing an image calls `POST /images/delete` to delete the file from disk (server checks if referenced elsewhere first)
- Delete standalone album button (calls `DELETE /albums/:slug`, cleans up orphaned images)

### assets/images/
- `headshot.jpeg` — profile photo (412KB)
- `posts/` — published post images, naming convention: `YYYYMMDDHHMMSS-originalname.ext`
- `drafts/` — draft post images (same naming convention, gitignored)
- `albums/` — standalone album images (same naming convention)

---

## Scripts

### scripts/local_editor_server.rb (861 lines)
Sinatra REST API on `127.0.0.1:4001` for local blog editing. **Depends on:** sinatra, json, yaml, fileutils, time, base64 (all stdlib or development-group gems).

**Endpoints:**

| Method | Route | Purpose |
|--------|-------|---------|
| `GET` | `/posts` | List all posts + drafts (metadata only) |
| `GET` | `/posts/:kind/:slug` | Read single post/draft with full body |
| `POST` | `/posts` | Create new post or draft |
| `PUT` | `/posts/:kind/:slug` | Update existing post/draft |
| `PUT` | `/posts/:kind/:slug/images` | Save album images only (used by album editor) |
| `DELETE` | `/posts/:kind/:slug` | Delete post/draft + orphaned images |
| `POST` | `/publish/:slug` | Convert draft to published post |
| `GET` | `/albums` | List all standalone albums |
| `GET` | `/albums/:slug` | Read single standalone album |
| `POST` | `/albums` | Create standalone album |
| `PUT` | `/albums/:slug` | Update standalone album |
| `DELETE` | `/albums/:slug` | Delete standalone album + orphaned images |
| `POST` | `/images` | Upload image file (supports `album=true` param) |
| `POST` | `/images/delete` | Delete image file if not referenced elsewhere |
| `GET` | `/assets/images/*` | Serve images from temp or final dirs |
| `OPTIONS` | `*` | CORS preflight |

**Key helpers:**
- `parse_post(path)` — extracts YAML front matter (including `images` array) + markdown body
- `parse_album(path)` — extracts album YAML front matter (title, description, images, draft)
- `album_to_file(album)` — serializes album hash to YAML frontmatter file content
- `parse_images_from_data(data)` — validates and normalizes `images` array from request JSON
- `images_to_frontmatter(images)` — serializes images array to YAML for frontmatter output
- `extract_body_images(body)` — parses markdown body for `![alt](url)` + optional `*caption*` patterns, returns `[{src, caption}]`
- `merge_images(body_images, album_images)` — deduplicates by src, album images take priority for captions
- `promote_temp_images(body, images=[])` — moves images from `_editor_tmp/` to `assets/images/`, scans body + album `src` paths (supports posts/drafts/albums subdirs)
- `find_image_references(src, exclude_path:)` — scans all posts + albums for references to an image src
- `delete_image_if_orphaned(src, exclude_path:)` — deletes image file only if no other post/album references it
- `extract_base64_images(body, kind, slug)` — decodes inline base64 data URLs, saves as files
- `ext_for_mime(mime)` — MIME type to file extension mapping

**Image flow:** upload → `_editor_tmp/{posts|drafts|albums}/YYYYMMDDHHMMSS-filename.ext` → promoted to `assets/images/{posts|drafts|albums}/` on save. Draft↔post conversion rewrites paths in `images` frontmatter. Deleting a post/album also deletes orphaned image files.

**CORS:** restricted to localhost origins only.

### scripts/migrate_images_to_figures.rb (114 lines)
One-time migration script. Converts markdown image+caption patterns:
```
![alt](url)
*caption*
```
to HTML `<figure class="post-image">` blocks with `<figcaption>`. Skips files already using `<figure>`.

### scripts/extract_base64_images.rb (98 lines)
One-time cleanup script. Finds base64 `data:image/...;base64,...` URLs in post markdown, decodes and saves as files to `assets/images/posts/`, replaces inline data with file paths. Naming: `embedded-{slug}-{index}.{ext}`.

### scripts/backfill_titles.rb (75 lines)
Maintenance script. Reads all posts/drafts, fills in missing `title` front matter by humanizing the slug (e.g., `hello-world` → `Hello World`).

### scripts/get-spotify-refresh-token.py (152 lines)
One-time setup script for Spotify integration. Runs OAuth 2.0 authorization code flow:
1. Opens browser to Spotify auth page
2. Captures callback on `localhost:8888`
3. Exchanges code for refresh token
4. Prints token for GitHub Secrets setup

**Scope:** `user-read-recently-played`. **Dependencies:** Python stdlib only.

---

## GitHub Actions

### .github/workflows/update-spotify.yml (111 lines)
Automated Spotify "recently played" sync.

**Trigger:** cron every 30 min (`*/30 * * * *`) + manual `workflow_dispatch`.

**Steps:**
1. Checkout repo
2. Embedded Python script: exchanges refresh token → access token → `GET /v1/me/player/recently-played?limit=1` → extracts track metadata (name, URL, artists, played_at, context) → writes `_data/now-playing.json`
3. Auto-commit with `[skip ci]` flag as `github-actions[bot]`

**Required secrets:** `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, `SPOTIFY_REFRESH_TOKEN`

---

## Architecture & Data Flow

### Build Pipeline
`_config.yml` + `_config_prod.yml` (overlay) → Jekyll 3.8 → `_site/`

### Page Rendering
`page.md` → selects layout from front matter → layout includes `head.html`, `navbar.html`, `footer.html` → loads `theme.js` → Liquid reads from `_data/*.yml`

### Theme System
`navbar.html` renders 5 theme dots → user clicks → `theme.js` reads dot's `data-theme`, calls `setTheme()` → applies CSS custom properties to `:root` → `styles.css` uses `var(--*)` throughout → persisted to `localStorage["theme"]`

### Spotify Widget
`update-spotify.yml` (cron 30min) → Spotify API → writes `_data/now-playing.json` → Jekyll builds `now-playing.json.html` (permalink `/assets/data/now-playing.json`) → `index.md` inline JS fetches JSON → renders track info in `#spotify-now-playing`

### Local Editor System
`editor.md` (layout: editor) → `editor.html` loads Toast UI Editor + `editor.js` → `editor.js` CRUD calls to `local_editor_server.rb:4001` → server reads/writes `_posts/`, `_drafts/`, manages images in `_editor_tmp/` and `assets/images/`.

### Photo Gallery
`gallery.md` (linked from blog page) iterates both `site.posts` and `site.albums` → renders album cards (cover, title, count) + an "All Photos" photocard grid. Post-album cards link to the post URL (album grid rendered at bottom of post page). Standalone album cards link to `/albums/:slug/` (dedicated detail page). The All Photos grid uses the same `.album-photo` + lightbox components as post / album pages — clicking any photo opens the shared full-screen lightbox (loaded via `album_lightbox: true` front-matter flag on `gallery.md`, wired up in `default.html`). Draft standalone albums (`draft: true`) excluded from gallery.

**Image sources for post albums:**
1. **Auto-detected:** server extracts `![alt](url)` patterns from post body on save → merged into `images` frontmatter
2. **Album editor:** separate page (`/album-editor/`) for adding extra images with captions → saved via `PUT /posts/:kind/:slug/images`

**Standalone albums:** `_albums/` collection with `output: true`. Each `.md` file has frontmatter: `title`, `date`, `description` (max 500 chars), `draft`, `images: [{src, caption}]`. Layout: `album.html`. Images stored in `assets/images/albums/`.

**Image deletion security:** removing an image from an album calls `POST /images/delete` → server checks all posts + albums for references → only deletes if orphaned. Deleting a post/album also cleans up orphaned images. Draft images in `assets/images/drafts/` are gitignored and won't be published.

---

## Conventions & Patterns

- **Post filenames:** `YYYY-MM-DD-slug.md` in `_posts/`, `slug.md` in `_drafts/`
- **Page front matter (root pages):** `layout: default`, `title: "..."`, `permalink: /slug/`, `description: "..."` (SEO meta description, ~150 chars)
- **Post front matter:** `layout: post` (applied by default), `title: "..."`, `date: YYYY-MM-DD` (or ISO 8601), `tags: [array]`, optional `excerpt: "..."`, optional `images: [{src, caption?}]` (photo album, max 25). The `caption` key on each image is optional.
- **Album filenames:** `slug.md` in `_albums/`
- **Album front matter:** `layout: album` (applied by default), `title: "..."`, `date: YYYY-MM-DD`, `description: "..."` (max 500 chars), optional `draft: true`, `images: [{src, caption?}]`
- **Image naming:** `YYYYMMDDHHMMSS-originalname.ext` (timestamp prefix, set by editor server)
- **CSS theming:** always use `var(--name)` for colors; never hardcode hex in component styles
- **Data access:** `_data/` files accessed as `site.data.filename` in Liquid
- **Conditional editor:** nav link + page only appear when `site.local_editor == true` AND `jekyll.environment == "development"`
- **External deps:** Font Awesome 6.4.2, Google Fonts (Inter, DM Serif Display, JetBrains Mono), Toast UI Editor (editor only)
- **Blog post images:** use markdown `![caption](url)` followed by `*caption*` on the next line (styled by CSS `:has()` selector). Avoid `<figure>` HTML — Toast UI Editor strips it during round-trip.
- **Links:** all external links use `target="_blank" rel="noopener noreferrer"`
- **Anti-AI defense:** See dedicated section below. All 4 layers must be maintained when adding new pages or layouts.

---

## Anti-AI Defense

> **LLM instruction:** This section is a hard requirement. Every time you create or modify a page, layout, or include, verify ALL checklist items below are satisfied. Do not treat this as optional.

The site uses 4 independent layers to block AI crawlers and opt out of AI training data collection. Each layer targets a different mechanism; all four must remain intact.

### Layer 1 — `robots.txt` (crawler-level block)

**File:** [`robots.txt`](robots.txt)

Blocks 20+ known AI training crawlers by `User-Agent`. Legitimate search engines (Googlebot, Bingbot, DuckDuckBot, Applebot) are explicitly allowed. All other crawlers default to allowed (so standard SEO indexing works).

**Blocked agents include:** GPTBot, ChatGPT-User, Google-Extended, anthropic-ai, Claude-Web, CCBot, Bytespider, PerplexityBot, Applebot-Extended, Meta-ExternalAgent, FacebookBot, Amazonbot, Cohere-ai, AI2Bot, Diffbot, img2dataset, and more.

**LLM instruction:** When new major AI crawlers become publicly identified, add a `User-agent: <BotName> / Disallow: /` block to `robots.txt`. Do not remove any existing entries.

### Layer 2 — `<meta name="robots">` (page-level signal)

**File:** [`_includes/head.html`](_includes/head.html)

Every page rendered through any layout that includes `head.html` automatically gets:
```html
<meta name="robots" content="noai, noimageai">
```

- `noai` — signals that page text should not be used for AI training
- `noimageai` — signals that images should not be used for AI training

**LLM instruction:** `head.html` is included in ALL layouts (`default.html`, `post.html`, `album.html`, `editor.html`, `album-editor.html`). Any new layout you create MUST include `{% include head.html %}`. Never create a layout that bypasses `head.html` — doing so removes this protection from that page type.

### Layer 3 — `<meta name="tdm-reservation">` (W3C TDM protocol)

**File:** [`_includes/head.html`](_includes/head.html)

Every page also gets:
```html
<meta name="tdm-reservation" content="1">
```

This implements the [W3C Text and Data Mining Reservation Protocol](https://www.w3.org/2022/tdmrep/). A value of `1` reserves all rights — the site owner has not granted permission for text/data mining (including AI training). This is a formal machine-readable rights declaration, separate from `robots.txt`.

**LLM instruction:** Same as Layer 2 — covered automatically by `head.html`. Do not remove this meta tag from `head.html`.

### Layer 4 — `ai.txt` (Spawning.ai standard)

**File:** [`ai.txt`](ai.txt)

A machine-readable opt-out following the [Spawning.ai `ai.txt` standard](https://site.spawning.ai/spawning-ai-txt). Declares that no content (text, images, media) from this site may be used for AI/ML training. Format mirrors `robots.txt` syntax.

Current content disallows all user-agents:
```
User-Agent: *
Disallow: /
```

**LLM instruction:** This file covers the whole site by default. No per-page action needed. Do not modify the `Disallow` directive.

### LLM Checklist — New Page or Layout

When you create a **new layout file** (`_layouts/*.html`):
- [ ] It must contain `{% include head.html %}` — this automatically adds Layers 2 and 3

When you create a **new root page** (`*.md` or `*.html` with a layout):
- [ ] Verify it uses a layout that includes `head.html` (all current layouts do)
- [ ] No special action needed if using an existing layout

When you create a **new standalone HTML file** (no Jekyll layout, rare):
- [ ] Manually add both meta tags to the `<head>`:
  ```html
  <meta name="robots" content="noai, noimageai">
  <meta name="tdm-reservation" content="1">
  ```

When you **add a new prominent AI crawler** to block:
- [ ] Add to `robots.txt` under the "Block AI training crawlers" section:
  ```
  User-agent: NewBotName
  Disallow: /
  ```

### Summary Table

| Layer | File | Scope | Mechanism |
|-------|------|-------|-----------|
| 1 | `robots.txt` | Crawl-time | User-Agent blocklist |
| 2 | `_includes/head.html` | Every rendered page | `<meta name="robots" content="noai, noimageai">` |
| 3 | `_includes/head.html` | Every rendered page | `<meta name="tdm-reservation" content="1">` (W3C TDM) |
| 4 | `ai.txt` | Whole site | Spawning.ai opt-out standard |
