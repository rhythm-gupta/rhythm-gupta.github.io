# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Jekyll-based personal blog/portfolio website hosted on GitHub Pages. The site is built using the Jekyll Now theme, which provides a minimal, responsive blog template optimized for GitHub Pages deployment.

**Key Information:**
- **Owner:** Rhythm Gupta (Product Guy)
- **Theme:** Jekyll Now (fork-based theme)
- **Hosting:** GitHub Pages
- **Domain:** Custom domain configured via CNAME
- **Analytics:** Google Analytics (UA-85168588-1)

## Architecture & Structure

### Core Jekyll Structure
- `_config.yml`: Main Jekyll configuration with site metadata, social links, and build settings
- `_layouts/`: HTML templates for different page types
  - `default.html`: Base template with header navigation (Bucket List, Blog, Work)
  - `page.html`: Template for static pages
  - `post.html`: Template for blog posts
- `_includes/`: Reusable HTML components (analytics, meta tags, social icons, etc.)
- `_posts/`: Blog posts in Markdown format with YYYY-MM-DD-title.md naming convention
- `_sass/`: SCSS partials for styling
  - `_variables.scss`: Color scheme, fonts, and responsive breakpoints
  - `_highlights.scss`: Syntax highlighting styles
  - `_svg-icons.scss`: Social media icon styles
- `_site/`: Generated static site (excluded from version control)

### Content Structure
- **Main Pages:** Bucket List, Blog, Work (defined in navigation)
- **Blog Posts:** Personal reflections, product management insights, book reviews
- **Book Notes:** Separate collection under `booknotes/` directory
- **Styling:** Custom color scheme with warm tones (beige background: #FFFBEC, brown text: #5B553A)

### Development Workflow
The site uses Jekyll Now's "fork-first" workflow designed for GitHub.com editing, but local development is supported.

## Common Development Commands

### Local Development Setup
```bash
# Install Jekyll and GitHub Pages dependencies
gem install github-pages

# Serve the site locally with auto-reload
jekyll serve

# View at http://127.0.0.1:4000/
```

### Content Creation
```bash
# Create new blog post (follow naming convention)
# File: _posts/YYYY-MM-DD-title.md
# Include YAML front matter:
# ---
# layout: post
# title: "Post Title"
# ---
```

### Deployment
- **Automatic:** Push to master branch triggers GitHub Pages rebuild
- **Manual:** Any change to `_config.yml` forces rebuild
- **Verification:** Changes appear at the live site within minutes

## Theme Customization

### Color Scheme
The site uses a custom warm color palette defined in `_sass/_variables.scss`:
- Background: `#FFFBEC` (warm white/beige)
- Primary text: `#5B553A` (dark brown)
- Links: `#4183C4` (GitHub blue)
- Gray scale: `#666`, `#eee`, `#000`

### Navigation
Main navigation is hardcoded in `_layouts/default.html` with three primary sections:
- Bucket List (`/bucket-list`)
- Blog (`/blog`) 
- Work (`/work`)

### Responsive Design
Uses a mobile-first approach with breakpoint at 640px defined in `_variables.scss`.

## Content Guidelines

### Blog Posts
- Use descriptive filenames following YYYY-MM-DD-title.md format
- Include proper YAML front matter with layout and title
- Topics focus on: product management, entrepreneurship, personal development, book reviews

### Markdown Support
- GitHub Flavored Markdown (GFM) enabled
- Syntax highlighting via Rouge
- Kramdown processor for enhanced Markdown features

## Configuration Notes

### Jekyll Settings
- Permalink structure: `/:categories/:year/:month/:day/:title:output_ext`
- Theme: Minima with Jekyll Now customizations
- Plugins: jekyll-sitemap, jekyll-feed, jekyll-seo-tag
- Sass compilation: expanded style (not minified)

### Analytics & SEO
- Google Analytics tracking enabled for production environment
- Jekyll SEO Tag plugin for meta tags and structured data
- RSS feed automatically generated
- Sitemap.xml automatically generated

## File Exclusions
The following files are excluded from the generated site:
- Gemfile, Gemfile.lock
- LICENSE, README.md
- CNAME (used for GitHub Pages domain configuration)