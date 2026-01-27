#!/usr/bin/env python3
"""
Template build script for Go Semi and Beyond static site.

Usage:
    python build.py          # Build once
    python build.py --watch  # Watch for changes and rebuild automatically

URL Structure:
    /                           - Homepage
    /about/                     - About page
    /issues/                    - Archive (list of all issues)
    /issues/{issue-slug}/       - Issue page (list of articles in issue)
    /issues/{issue-slug}/{article}/  - Article page

Template syntax:
    {{> partial_name }}  - Include a partial from src/partials/partial_name.html
    {{title}}            - Page title (set in front-matter)
    {{content}}          - Page content (in layouts)
"""

import os
import re
import sys
import time
import shutil
import argparse
import json
from pathlib import Path

try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False
    print("Warning: markdown library not installed. Run: pip install markdown")

# Configuration
SRC_DIR = Path(__file__).parent / 'src'
PARTIALS_DIR = SRC_DIR / 'partials'
LAYOUTS_DIR = SRC_DIR / 'layouts'
PAGES_DIR = SRC_DIR / 'pages'
CONTENT_DIR = Path(__file__).parent / 'content'
STATIC_MOCKUP_DIR = Path(__file__).parent
OUTPUT_DIR = Path(__file__).parent.parent / 'docs'

# Static asset directories to copy
STATIC_DIRS = ['css', 'js', 'images']

# Files/directories to ignore
IGNORE_PATTERNS = ['partials', 'layouts', 'pages']

# Category display name mappings (empty string = hide label)
CATEGORY_MAPPING = {
    'Upcoming Events': 'Events',
    'Uncategorized': '',
}

# Current issue slug (update this when publishing a new issue)
CURRENT_ISSUE_SLUG = 'january-2026'

# Base path for GitHub Pages (set to '' for local/root deployment, '/GOSEMI' for project site)
BASE_PATH = '/GOSEMI'

# Constant Contact subscribe URL
CC_SUBSCRIBE_URL = 'https://visitor.r20.constantcontact.com/manage/optin?v=001y_Bo5goCBKQ5mpCMPMk9NZ99QMnLrLllc1SVvjz3oBDPSK7NuaD2lmbp7Qd60Oy3ftqVE4iZfLT8xvaduZ92LDuKgDRcJgGp19iRFGA-2EqbiZuQnFXcLv5m5oWB7xioLSQR2RO7XNixpn3YPSNXUJ4X2lHntVromrWTUzGfYQ4%3D'


def normalize_category(category):
    """Normalize category names for display. Returns empty string to hide label."""
    return CATEGORY_MAPPING.get(category, category)


def write_page(path, content):
    """Write a page using directory-based URLs (path/index.html)."""
    if path.endswith('/'):
        path = path[:-1]

    output_path = OUTPUT_DIR / path
    output_path.mkdir(parents=True, exist_ok=True)

    output_file = output_path / 'index.html'
    output_file.write_text(content, encoding='utf-8')
    return output_file


def load_partials():
    """Load all partial templates from the partials directory."""
    partials = {}
    if PARTIALS_DIR.exists():
        for partial_file in PARTIALS_DIR.glob('*.html'):
            name = partial_file.stem
            partials[name] = partial_file.read_text(encoding='utf-8')
            print(f"  Loaded partial: {name}")
    return partials


def load_layouts():
    """Load all layout templates from the layouts directory."""
    layouts = {}
    if LAYOUTS_DIR.exists():
        for layout_file in LAYOUTS_DIR.glob('*.html'):
            name = layout_file.stem
            layouts[name] = layout_file.read_text(encoding='utf-8')
            print(f"  Loaded layout: {name}")
    return layouts


def parse_front_matter(content):
    """Parse front-matter from page content."""
    metadata = {
        'title': 'Go Semi & Beyond',
        'layout': 'base'
    }

    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            front_matter = parts[1].strip()
            for line in front_matter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip().strip('"\'')
            return metadata, parts[2].strip()

    return metadata, content


def clean_markdown(content):
    """Clean up pandoc-generated markdown artifacts."""
    content = re.sub(r'\{\.mark\}', '', content)
    content = re.sub(r'\{width="[^"]*"\s*height="[^"]*"\}', '', content)
    content = re.sub(r'\{width="[^"]*"\}', '', content)
    content = re.sub(r'\{height="[^"]*"\}', '', content)
    content = content.replace('\\#', '#')
    content = content.replace('\\[', '[')
    content = content.replace('\\]', ']')
    content = re.sub(r'AI-generated content may be incorrect\.?', '', content)
    content = re.sub(r'\^(\d+)\^', r'<sup>\1</sup>', content)
    content = re.sub(r'\s*end \.et_[a-z_0-9]+\s*', ' ', content)
    content = re.sub(r'\s*\.et_builder\s*', ' ', content)
    content = re.sub(r'\s*end \.post_content\s*', '', content)
    content = re.sub(r'  +', ' ', content)
    return content


def convert_markdown_to_html(md_content, base_image_path='/images/'):
    """Convert markdown content to HTML."""
    if not MARKDOWN_AVAILABLE:
        return f"<pre>{md_content}</pre>"

    md_content = clean_markdown(md_content)

    def fix_image_path(match):
        alt_text = match.group(1).strip()
        img_path = match.group(2)
        filename = Path(img_path).name
        return f'![{alt_text}]({base_image_path}{filename})'

    md_content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', fix_image_path, md_content)

    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'])
    html = md.convert(md_content)

    html = re.sub(
        r'(<img[^>]+>)\s*</p>\s*<p><em>([^<]+)</em>',
        r'<figure>\1<figcaption>\2</figcaption></figure>',
        html
    )

    return html


def process_template(content, partials):
    """Process a template, replacing partial includes with their content."""
    pattern = r'\{\{>\s*(\w+)\s*\}\}'

    def replace_partial(match):
        partial_name = match.group(1)
        if partial_name in partials:
            return partials[partial_name]
        else:
            print(f"  Warning: Partial '{partial_name}' not found")
            return match.group(0)

    return re.sub(pattern, replace_partial, content)


def process_page_with_layout(page_content, layouts, partials, issue_metadata=None, depth=0):
    """Process a page file with front-matter and apply layout."""
    metadata, content = parse_front_matter(page_content)

    layout_name = metadata.get('layout', 'base')
    if layout_name not in layouts:
        print(f"  Warning: Layout '{layout_name}' not found, using content as-is")
        return process_template(page_content, partials)

    layout = layouts[layout_name]

    # Calculate path prefix based on depth
    prefix = '../' * depth if depth > 0 else ''

    # Replace placeholders
    result = layout.replace('{{title}}', metadata.get('title', 'Go Semi & Beyond'))
    result = result.replace('{{body_class}}', metadata.get('body_class', ''))
    result = result.replace('{{content}}', content)
    result = result.replace('{{path_prefix}}', prefix)

    result = process_template(result, partials)

    # Replace dynamic content placeholders
    if issue_metadata:
        lighter_side_image = issue_metadata.get('lighter_side_image', '')
        lighter_side_alt = issue_metadata.get('lighter_side_alt', 'On the Lighter Side')
        if lighter_side_image:
            lighter_side_html = f'<img src="{BASE_PATH}/images/{lighter_side_image}" alt="{lighter_side_alt}" style="width: 100%; border-radius: 8px;">'
        else:
            lighter_side_html = '<p style="color: var(--COLOR_TEXT_SECONDARY); font-style: italic;">Coming soon...</p>'
        result = result.replace('{{lighter_side_content}}', lighter_side_html)

        # Podcast spotlight data
        podcast_title = issue_metadata.get('podcast_title', 'Advantest Talks Semi')
        podcast_excerpt = issue_metadata.get('podcast_excerpt', 'Listen to the latest episode of Advantest Talks Semi.')
        podcast_slug = issue_metadata.get('podcast_slug', 'podcast-spotlight')
        issue_slug = issue_metadata.get('issue_slug', CURRENT_ISSUE_SLUG)
        result = result.replace('{{podcast_title}}', podcast_title)
        result = result.replace('{{podcast_excerpt}}', podcast_excerpt)
        result = result.replace('{{podcast_url}}', f'{BASE_PATH}/issues/{issue_slug}/{podcast_slug}/')

    result = result.replace('{{lighter_side_content}}', '')
    result = result.replace('{{podcast_title}}', 'Advantest Talks Semi')
    result = result.replace('{{podcast_excerpt}}', '')
    result = result.replace('{{podcast_url}}', '#')
    result = result.replace('{{subscribe_url}}', CC_SUBSCRIBE_URL)
    result = result.replace('{{current_issue}}', CURRENT_ISSUE_SLUG)
    result = result.replace('{{base_path}}', BASE_PATH)

    return result


def load_issues_data():
    """Load all issues and articles data."""
    issues_file = CONTENT_DIR / 'issues.json'
    archive_dir = CONTENT_DIR / 'archive'
    issues_dir = CONTENT_DIR / 'issues'

    all_articles = {}
    issues = []

    # Load issues from JSON
    if issues_file.exists():
        with open(issues_file, 'r', encoding='utf-8') as f:
            issues = json.load(f)

    # Load articles from archive (historical content)
    if archive_dir.exists():
        for year_dir in sorted(archive_dir.iterdir()):
            if not year_dir.is_dir() or year_dir.name == 'images':
                continue

            year = year_dir.name

            for article_file in year_dir.glob('*.md'):
                content = article_file.read_text(encoding='utf-8')
                metadata, md_content = parse_front_matter(content)

                article_slug = metadata.get('slug', article_file.stem)
                title = metadata.get('title', article_slug.replace('-', ' ').title())

                # Clean up content
                md_content = re.sub(r'Posted\s+in\s+\[.*?\]\(.*?\)\s*\n*', '', md_content)
                md_content = re.sub(r'\s*end \.post_content\s*', '', md_content)
                md_content = re.sub(rf'^#\s*{re.escape(title)}\s*\n*', '', md_content, flags=re.MULTILINE)

                all_articles[article_slug] = {
                    'title': title,
                    'slug': article_slug,
                    'category': metadata.get('category', 'Article'),
                    'author': metadata.get('author', ''),
                    'date': metadata.get('date', ''),
                    'excerpt': metadata.get('excerpt', ''),
                    'original_url': metadata.get('original_url', ''),
                    'year': year,
                    'md_content': md_content,
                    'image_path': f'{BASE_PATH}/images/archive/',
                }

    # Load articles from content/issues/{issue-slug}/articles/ (current/new content)
    if issues_dir.exists():
        for issue_dir in issues_dir.iterdir():
            if not issue_dir.is_dir():
                continue

            issue_slug = issue_dir.name
            articles_dir = issue_dir / 'articles'

            if articles_dir.exists():
                for article_file in articles_dir.glob('*.md'):
                    content = article_file.read_text(encoding='utf-8')
                    metadata, md_content = parse_front_matter(content)

                    article_slug_name = metadata.get('slug', article_file.stem)
                    title = metadata.get('title', article_slug_name.replace('-', ' ').title())

                    all_articles[article_slug_name] = {
                        'title': title,
                        'slug': article_slug_name,
                        'category': metadata.get('category', ''),
                        'author': metadata.get('author', ''),
                        'date': metadata.get('date', ''),
                        'excerpt': metadata.get('excerpt', ''),
                        'original_url': '',
                        'year': issue_slug.split('-')[-1] if '-' in issue_slug else '',
                        'md_content': md_content,
                        'image_path': f'{BASE_PATH}/images/issues/{issue_slug}/',
                    }

    # Map articles to issues
    issue_articles = {}

    for issue in issues:
        issue_slug = issue['slug']
        issue_articles[issue_slug] = []

        for article_ref in issue.get('articles', []):
            article_slug = article_ref['slug']
            if article_slug in all_articles:
                article_data = all_articles[article_slug].copy()
                article_data['issue_slug'] = issue_slug
                article_data['issue_title'] = issue['title']
                issue_articles[issue_slug].append(article_data)
                all_articles[article_slug]['issue_slug'] = issue_slug
                all_articles[article_slug]['issue_title'] = issue['title']

    return issues, all_articles, issue_articles


def generate_article_page(article, issue_slug, issue_title, layouts, partials):
    """Generate an article page."""
    # Use article's image path or default to archive
    image_path = article.get('image_path', '/images/archive/')
    html_content = convert_markdown_to_html(article['md_content'], image_path)

    # Build header
    header_html = f'<h1>{article["title"]}</h1>'
    header_html += '<div class="article-meta">'
    meta_parts = []
    if article['category']:
        display_category = normalize_category(article['category'])
        if display_category:
            meta_parts.append(f'<span class="article-label">{display_category}</span>')
    meta_parts.append(f'<span class="article-date">{issue_title} Issue</span>')
    if article['author']:
        meta_parts.append(f'<span class="article-author">By {article["author"]}</span>')
    header_html += ' &bull; '.join(meta_parts)
    header_html += '</div>'

    back_link = f'<a href="{BASE_PATH}/issues/{issue_slug}/" class="btn-outline">&larr; Back to {issue_title} Issue</a>'
    original_link = f'<a href="{article["original_url"]}" class="btn-outline" target="_blank">View Original</a>' if article.get('original_url') else ''

    layout = layouts.get('base')
    page_html = layout.replace('{{title}}', f'{article["title"]} - Go Semi & Beyond')
    page_html = page_html.replace('{{body_class}}', '')
    page_html = page_html.replace('{{path_prefix}}', '../../../')
    page_html = page_html.replace('{{content}}', f'''
    <article class="article-page archive-article">
        <div class="article-header">
            {header_html}
        </div>
        <div class="article-body">
            {html_content}
        </div>
        <div class="article-footer" style="margin-top: 40px; padding-top: 20px; border-top: 1px solid var(--border);">
            {back_link}
            {original_link}
        </div>
    </article>
''')
    page_html = process_template(page_html, partials)
    page_html = page_html.replace('{{subscribe_url}}', CC_SUBSCRIBE_URL)
    page_html = page_html.replace('{{current_issue}}', CURRENT_ISSUE_SLUG)
    page_html = page_html.replace('{{base_path}}', BASE_PATH)

    return page_html


def generate_issue_page(issue, articles, layouts, partials):
    """Generate an issue page listing its articles."""
    issue_html = f'''
    <div class="issue-page">
        <header class="issue-header">
            <h1>{issue['title']} Issue</h1>
            <p><a href="{BASE_PATH}/issues/">&larr; Back to All Issues</a></p>
        </header>
        <div class="issue-content">
'''

    if articles:
        issue_html += '<div class="issue-articles">'
        for article in articles:
            display_category = normalize_category(article.get('category', '')) if article.get('category') else ''
            category_badge = f'<span class="article-label">{display_category}</span>' if display_category else ''
            excerpt = article.get('excerpt', '')
            excerpt = re.sub(r'^Posted\s+in\s+\S+\s*', '', excerpt).strip()
            if len(excerpt) > 200:
                excerpt = excerpt[:200] + '...'
            issue_html += f'''
            <article class="issue-article-item">
                <div class="issue-article-content">
                    {category_badge}
                    <h3><a href="{BASE_PATH}/issues/{issue['slug']}/{article['slug']}/">{article['title']}</a></h3>
                    {f'<p class="article-excerpt">{excerpt}</p>' if excerpt else ''}
                </div>
            </article>
'''
        issue_html += '</div>'
    else:
        issue_html += '<p class="no-articles">No articles available for this issue.</p>'

    # Lighter side section
    lighter_side_image = issue.get('lighter_side_image', '')
    if lighter_side_image:
        # Current issue uses /images/, archived issues use /images/archive/lighter-side/
        if issue['slug'] == CURRENT_ISSUE_SLUG:
            lighter_side_path = f'{BASE_PATH}/images/{lighter_side_image}'
        else:
            lighter_side_path = f'{BASE_PATH}/images/archive/lighter-side/{lighter_side_image}'
        issue_html += f'''
            <div class="lighter-side-section" style="margin-top: 40px; padding-top: 30px; border-top: 1px solid var(--border);">
                <h3>On the Lighter Side</h3>
                <img src="{lighter_side_path}" alt="On the Lighter Side - {issue['title']}" style="max-width: 100%; border-radius: 8px; margin-top: 15px;">
            </div>
'''

    issue_html += f'''
        </div>
    </div>

    <section class="cta-section">
        <div class="container">
            <h2>Stay Informed</h2>
            <p>Subscribe to Go Semi & Beyond for the latest semiconductor insights.</p>
            <a href="{CC_SUBSCRIBE_URL}" class="btn-primary" target="_blank">Subscribe Today</a>
        </div>
    </section>
'''

    layout = layouts.get('base')
    page_html = layout.replace('{{title}}', f'{issue["title"]} Issue - Go Semi & Beyond')
    page_html = page_html.replace('{{body_class}}', '')
    page_html = page_html.replace('{{path_prefix}}', '../../')
    page_html = page_html.replace('{{content}}', issue_html)
    page_html = process_template(page_html, partials)
    page_html = page_html.replace('{{subscribe_url}}', CC_SUBSCRIBE_URL)
    page_html = page_html.replace('{{current_issue}}', CURRENT_ISSUE_SLUG)
    page_html = page_html.replace('{{base_path}}', BASE_PATH)

    return page_html


def generate_issues_index(issues, issue_articles, layouts, partials):
    """Generate the issues index page (archive)."""
    archive_html = '''
    <div class="archive-page">
        <header class="archive-header">
            <h1>All Issues</h1>
            <p>Browse our complete archive of GO SEMI & BEYOND newsletter issues.</p>
        </header>
        <div class="archive-content">
'''

    # Group by year
    issues_by_year = {}
    for issue in issues:
        year = issue['year']
        if year not in issues_by_year:
            issues_by_year[year] = []
        issues_by_year[year].append(issue)

    month_order = ['December', 'November', 'October', 'September', 'August', 'July',
                   'June', 'May', 'April', 'March', 'February', 'January']

    for year in sorted(issues_by_year.keys(), reverse=True):
        year_issues = issues_by_year[year]
        archive_html += f'''
        <section class="archive-year">
            <h2>{year}</h2>
            <div class="issue-grid">
'''
        year_issues_sorted = sorted(year_issues, key=lambda x: month_order.index(x['month']) if x['month'] in month_order else 12)

        for issue in year_issues_sorted:
            article_count = len(issue_articles.get(issue['slug'], []))
            archive_html += f'''
                <a href="{BASE_PATH}/issues/{issue['slug']}/" class="issue-card">
                    <div class="issue-card-content">
                        <h3>{issue['title']}</h3>
                        <p class="issue-article-count">{article_count} articles</p>
                    </div>
                </a>
'''
        archive_html += '''
            </div>
        </section>
'''

    archive_html += f'''
        </div>
    </div>

    <section class="cta-section">
        <div class="container">
            <h2>Stay Informed</h2>
            <p>Subscribe to Go Semi & Beyond for the latest semiconductor insights.</p>
            <a href="{CC_SUBSCRIBE_URL}" class="btn-primary" target="_blank">Subscribe Today</a>
        </div>
    </section>
'''

    layout = layouts.get('base')
    page_html = layout.replace('{{title}}', 'All Issues - Go Semi & Beyond')
    page_html = page_html.replace('{{body_class}}', '')
    page_html = page_html.replace('{{path_prefix}}', '../')
    page_html = page_html.replace('{{content}}', archive_html)
    page_html = process_template(page_html, partials)
    page_html = page_html.replace('{{subscribe_url}}', CC_SUBSCRIBE_URL)
    page_html = page_html.replace('{{current_issue}}', CURRENT_ISSUE_SLUG)
    page_html = page_html.replace('{{base_path}}', BASE_PATH)

    return page_html


def get_current_issue_metadata():
    """Load metadata from the current issue's index.md file and articles."""
    issues_dir = CONTENT_DIR / 'issues'
    if not issues_dir.exists():
        return {}

    current_issue_dir = issues_dir / CURRENT_ISSUE_SLUG
    if not current_issue_dir.exists():
        issue_dirs = sorted([d for d in issues_dir.iterdir() if d.is_dir()], reverse=True)
        if not issue_dirs:
            return {}
        current_issue_dir = issue_dirs[0]

    index_file = current_issue_dir / 'index.md'
    if not index_file.exists():
        return {}

    content = index_file.read_text(encoding='utf-8')
    metadata, _ = parse_front_matter(content)
    metadata['issue_slug'] = current_issue_dir.name

    # Load podcast spotlight data from articles
    articles_dir = current_issue_dir / 'articles'
    if articles_dir.exists():
        podcast_file = articles_dir / 'podcast-spotlight.md'
        if podcast_file.exists():
            podcast_content = podcast_file.read_text(encoding='utf-8')
            podcast_metadata, _ = parse_front_matter(podcast_content)
            metadata['podcast_title'] = podcast_metadata.get('title', 'Advantest Talks Semi')
            metadata['podcast_excerpt'] = podcast_metadata.get('excerpt', '')
            metadata['podcast_slug'] = 'podcast-spotlight'

    return metadata


def copy_static_assets():
    """Copy static asset directories to output directory."""
    print("\nCopying static assets:")
    for dir_name in STATIC_DIRS:
        src_path = STATIC_MOCKUP_DIR / dir_name
        dest_path = OUTPUT_DIR / dir_name
        if src_path.exists():
            if dest_path.exists():
                shutil.rmtree(dest_path)
            shutil.copytree(src_path, dest_path)
            print(f"  {dir_name}/ -> docs/{dir_name}/")

    # Copy archive images
    archive_images_src = CONTENT_DIR / 'archive' / 'images'
    if archive_images_src.exists():
        archive_images_dest = OUTPUT_DIR / 'images' / 'archive'
        if archive_images_dest.exists():
            shutil.rmtree(archive_images_dest)
        shutil.copytree(archive_images_src, archive_images_dest)
        print(f"  archive/images/ -> docs/images/archive/")

    # Copy issue images (from content/issues/{slug}/media or images)
    issues_dir = CONTENT_DIR / 'issues'
    if issues_dir.exists():
        for issue_dir in issues_dir.iterdir():
            if not issue_dir.is_dir():
                continue
            issue_slug = issue_dir.name

            # Try media/ first, then images/
            for img_dir_name in ['media', 'images']:
                img_src = issue_dir / img_dir_name
                if img_src.exists():
                    img_dest = OUTPUT_DIR / 'images' / 'issues' / issue_slug
                    img_dest.mkdir(parents=True, exist_ok=True)
                    for img_file in img_src.iterdir():
                        if img_file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg']:
                            shutil.copy2(img_file, img_dest / img_file.name)
                    print(f"  issues/{issue_slug}/{img_dir_name}/ -> docs/images/issues/{issue_slug}/")


def build_templates():
    """Build all templates to the output directory."""
    print("\n" + "=" * 50)
    print("Building Go Semi and Beyond templates...")
    print("=" * 50)

    # Clean and create output directory
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Copy static assets
    copy_static_assets()

    # Load partials and layouts
    print("\nLoading partials:")
    partials = load_partials()

    print("\nLoading layouts:")
    layouts = load_layouts()

    # Load current issue metadata
    print("\nLoading current issue metadata:")
    issue_metadata = get_current_issue_metadata()
    if issue_metadata:
        print(f"  Current issue: {issue_metadata.get('title', 'Unknown')}")

    templates_processed = 0

    # Load all issues and articles
    print("\nLoading issues and articles:")
    issues, all_articles, issue_articles = load_issues_data()
    print(f"  Loaded {len(issues)} issues")
    print(f"  Loaded {len(all_articles)} articles")

    # Generate issue pages and article pages
    print("\nGenerating issue and article pages:")
    for issue in issues:
        issue_slug = issue['slug']
        articles = issue_articles.get(issue_slug, [])

        # Generate issue page
        page_html = generate_issue_page(issue, articles, layouts, partials)
        write_page(f'issues/{issue_slug}', page_html)
        print(f"  /issues/{issue_slug}/ ({len(articles)} articles)")
        templates_processed += 1

        # Generate article pages for this issue
        for article in articles:
            page_html = generate_article_page(article, issue_slug, issue['title'], layouts, partials)
            write_page(f'issues/{issue_slug}/{article["slug"]}', page_html)
            templates_processed += 1

    # Generate issues index
    page_html = generate_issues_index(issues, issue_articles, layouts, partials)
    write_page('issues', page_html)
    print(f"  /issues/ (archive index)")
    templates_processed += 1

    # Process static pages from src/pages/
    print("\nProcessing static pages:")
    if PAGES_DIR.exists():
        for page_file in PAGES_DIR.glob('*.html'):
            content = page_file.read_text(encoding='utf-8')
            page_name = page_file.stem

            # Determine depth for path prefix
            if page_name == 'index':
                depth = 0
                output_file = OUTPUT_DIR / 'index.html'
            else:
                depth = 1
                output_file = None  # Use write_page

            processed = process_page_with_layout(content, layouts, partials, issue_metadata, depth)

            if page_name == 'index':
                output_file.write_text(processed, encoding='utf-8')
                print(f"  / (homepage)")
            else:
                write_page(page_name, processed)
                print(f"  /{page_name}/")

            templates_processed += 1

    print(f"\nBuild complete! Processed {templates_processed} pages.")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 50 + "\n")
    return templates_processed


def get_file_mtimes():
    """Get modification times for all source files."""
    mtimes = {}

    for f in SRC_DIR.rglob('*.html'):
        mtimes[str(f)] = f.stat().st_mtime

    if CONTENT_DIR.exists():
        for f in CONTENT_DIR.rglob('*.md'):
            mtimes[str(f)] = f.stat().st_mtime
        for f in CONTENT_DIR.rglob('*.json'):
            mtimes[str(f)] = f.stat().st_mtime

    for ext in ['css', 'js']:
        for f in STATIC_MOCKUP_DIR.rglob(f'*.{ext}'):
            mtimes[str(f)] = f.stat().st_mtime

    return mtimes


def watch_and_build():
    """Watch for file changes and rebuild automatically."""
    print("Watching for changes... (Ctrl+C to stop)")

    last_mtimes = get_file_mtimes()
    build_templates()

    try:
        while True:
            time.sleep(1)
            current_mtimes = get_file_mtimes()

            changed = False
            for filepath, mtime in current_mtimes.items():
                if filepath not in last_mtimes or last_mtimes[filepath] != mtime:
                    print(f"\nChange detected: {Path(filepath).name}")
                    changed = True
                    break

            if not changed:
                for filepath in current_mtimes:
                    if filepath not in last_mtimes:
                        print(f"\nNew file detected: {Path(filepath).name}")
                        changed = True
                        break

            if changed:
                build_templates()
                last_mtimes = current_mtimes

    except KeyboardInterrupt:
        print("\nWatch stopped.")


def main():
    parser = argparse.ArgumentParser(description='Build Go Semi and Beyond templates')
    parser.add_argument('--watch', '-w', action='store_true',
                        help='Watch for changes and rebuild automatically')
    args = parser.parse_args()

    if args.watch:
        watch_and_build()
    else:
        build_templates()


if __name__ == '__main__':
    main()
