#!/usr/bin/env python3
"""
Template build script for Go Semi and Beyond static site.

Usage:
    python build.py          # Build once
    python build.py --watch  # Watch for changes and rebuild automatically

Template syntax:
    {{> partial_name }}  - Include a partial from src/partials/partial_name.html
    {{title}}            - Page title (set in front-matter)
    {{content}}          - Page content (in layouts)

Page front-matter (at top of page files):
    ---
    title: Page Title Here
    layout: base
    ---

    <page content here>

Content Management:
    Markdown content for issues goes in content/issues/<issue-slug>/
    Each issue has an index.md with metadata and articles in articles/
"""

import os
import re
import sys
import time
import shutil
import argparse
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
OUTPUT_DIR = Path(__file__).parent.parent / 'docs'  # Output to /docs for GitHub Pages

# Static asset directories to copy
STATIC_DIRS = ['css', 'js', 'images']

# Files/directories to ignore
IGNORE_PATTERNS = ['partials', 'layouts', 'pages']

# Category display name mappings
CATEGORY_MAPPING = {
    'Upcoming Events': 'Events',
}


def normalize_category(category):
    """Normalize category names for display."""
    return CATEGORY_MAPPING.get(category, category)


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
    """Parse front-matter from page content.

    Front-matter format:
    ---
    title: Page Title
    layout: base
    ---

    Returns (metadata_dict, content_without_front_matter)
    """
    metadata = {
        'title': 'Go Semi & Beyond',
        'layout': 'base'
    }

    # Check for front-matter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            # Parse the front-matter
            front_matter = parts[1].strip()
            for line in front_matter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip().strip('"\'')
            # Return content without front-matter
            return metadata, parts[2].strip()

    return metadata, content


def clean_markdown(content):
    """Clean up pandoc-generated markdown artifacts."""
    # Remove {.mark} class markers
    content = re.sub(r'\{\.mark\}', '', content)
    # Remove width/height attributes from images
    content = re.sub(r'\{width="[^"]*"\s*height="[^"]*"\}', '', content)
    content = re.sub(r'\{width="[^"]*"\}', '', content)
    content = re.sub(r'\{height="[^"]*"\}', '', content)
    # Clean up escaped characters
    content = content.replace('\\#', '#')
    content = content.replace('\\[', '[')
    content = content.replace('\\]', ']')
    # Remove "AI-generated content may be incorrect" from image alt text
    content = re.sub(r'AI-generated content may be incorrect\.?', '', content)
    # Clean up superscript notation (e.g., cm^2^)
    content = re.sub(r'\^(\d+)\^', r'<sup>\1</sup>', content)
    return content


def convert_markdown_to_html(md_content, base_image_path='images/'):
    """Convert markdown content to HTML."""
    if not MARKDOWN_AVAILABLE:
        return f"<pre>{md_content}</pre>"

    # Clean up the markdown first
    md_content = clean_markdown(md_content)

    # Fix image paths - convert absolute paths to relative
    def fix_image_path(match):
        alt_text = match.group(1).strip()
        img_path = match.group(2)
        # Extract just the filename from the path
        filename = Path(img_path).name
        # Return cleaned markdown image
        return f'![{alt_text}]({base_image_path}{filename})'

    md_content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', fix_image_path, md_content)

    # Convert to HTML
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'])
    html = md.convert(md_content)

    # Add figure captions for images followed by italic text
    html = re.sub(
        r'(<img[^>]+>)\s*</p>\s*<p><em>([^<]+)</em>',
        r'<figure>\1<figcaption>\2</figcaption></figure>',
        html
    )

    return html


def fix_relative_paths(html, prefix, exclude_patterns=None):
    """Fix relative paths in HTML by adding a prefix for nested pages.

    Args:
        html: The HTML content to process
        prefix: The path prefix to add (e.g., '../')
        exclude_patterns: List of patterns to exclude from path fixing
    """
    if exclude_patterns is None:
        exclude_patterns = []

    def should_fix_path(path):
        # Don't fix absolute URLs, anchors, or already-prefixed paths
        if path.startswith(('http://', 'https://', '//', '#', 'mailto:', '../')):
            return False
        # Don't fix if matches any exclude pattern
        for pattern in exclude_patterns:
            if re.match(pattern, path):
                return False
        return True

    def fix_src(match):
        path = match.group(1)
        if should_fix_path(path):
            return f'src="{prefix}{path}"'
        return match.group(0)

    def fix_href(match):
        path = match.group(1)
        if should_fix_path(path):
            return f'href="{prefix}{path}"'
        return match.group(0)

    # Fix src attributes (images, scripts)
    html = re.sub(r'src="([^"]+)"', fix_src, html)
    # Fix href attributes (css, links)
    html = re.sub(r'href="([^"]+)"', fix_href, html)
    return html


def process_template(content, partials):
    """Process a template, replacing partial includes with their content."""
    # Pattern matches {{> partial_name }} with optional whitespace
    pattern = r'\{\{>\s*(\w+)\s*\}\}'

    def replace_partial(match):
        partial_name = match.group(1)
        if partial_name in partials:
            return partials[partial_name]
        else:
            print(f"  Warning: Partial '{partial_name}' not found")
            return match.group(0)  # Return original if not found

    return re.sub(pattern, replace_partial, content)


def process_page_with_layout(page_content, layouts, partials, issue_metadata=None):
    """Process a page file with front-matter and apply layout."""
    # Parse front-matter
    metadata, content = parse_front_matter(page_content)

    # Get the layout
    layout_name = metadata.get('layout', 'base')
    if layout_name not in layouts:
        print(f"  Warning: Layout '{layout_name}' not found, using content as-is")
        return process_template(page_content, partials)

    layout = layouts[layout_name]

    # Replace {{title}}, {{body_class}}, and {{content}} in layout
    result = layout.replace('{{title}}', metadata.get('title', 'Go Semi & Beyond'))
    result = result.replace('{{body_class}}', metadata.get('body_class', ''))
    result = result.replace('{{content}}', content)

    # Process partials
    result = process_template(result, partials)

    # Replace dynamic content placeholders from current issue
    if issue_metadata:
        # Lighter side content
        lighter_side_image = issue_metadata.get('lighter_side_image', '')
        lighter_side_alt = issue_metadata.get('lighter_side_alt', 'On the Lighter Side')
        if lighter_side_image:
            lighter_side_html = f'<img src="images/{lighter_side_image}" alt="{lighter_side_alt}" style="width: 100%; border-radius: 8px;">'
        else:
            lighter_side_html = '<p style="color: var(--COLOR_TEXT_SECONDARY); font-style: italic;">Coming soon...</p>'
        result = result.replace('{{lighter_side_content}}', lighter_side_html)

    # Clean up any remaining placeholders
    result = result.replace('{{lighter_side_content}}', '')

    return result


def process_archive_content(layouts, partials):
    """Process archived article content organized by issues."""
    import json

    archive_dir = CONTENT_DIR / 'archive'
    issues_file = CONTENT_DIR / 'issues.json'

    if not archive_dir.exists():
        return 0

    processed = 0
    all_articles = {}  # slug -> article data
    print("\nProcessing archive content:")

    # Copy archive images to output
    archive_images_src = archive_dir / 'images'
    if archive_images_src.exists():
        archive_images_dest = OUTPUT_DIR / 'images' / 'archive'
        if archive_images_dest.exists():
            shutil.rmtree(archive_images_dest)
        shutil.copytree(archive_images_src, archive_images_dest)
        image_count = len(list(archive_images_src.iterdir()))
        print(f"  Copied {image_count} archive images")

    # Create archive output directory
    archive_output_dir = OUTPUT_DIR / 'archive'
    archive_output_dir.mkdir(parents=True, exist_ok=True)

    # Process each year directory to build article index
    for year_dir in sorted(archive_dir.iterdir()):
        if not year_dir.is_dir() or year_dir.name == 'images':
            continue

        year = year_dir.name

        for article_file in year_dir.glob('*.md'):
            content = article_file.read_text(encoding='utf-8')
            metadata, md_content = parse_front_matter(content)

            article_slug = metadata.get('slug', article_file.stem)
            title = metadata.get('title', article_slug.replace('-', ' ').title())

            # Clean up the content
            md_content = re.sub(r'Posted\s+in\s+\[.*?\]\(.*?\)\s*\n*', '', md_content)
            md_content = re.sub(r'\s*end \.post_content\s*', '', md_content)
            md_content = re.sub(rf'^#\s*{re.escape(title)}\s*\n*', '', md_content, flags=re.MULTILINE)

            # Store article data
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
                'file_path': str(article_file)
            }

    print(f"  Loaded {len(all_articles)} articles")

    # Load issue mapping
    issues = []
    if issues_file.exists():
        with open(issues_file, 'r', encoding='utf-8') as f:
            issues = json.load(f)
        print(f"  Loaded {len(issues)} issues from issues.json")

    # Build issue -> articles mapping
    issue_articles = {}  # issue_slug -> list of article data
    assigned_slugs = set()

    for issue in issues:
        issue_slug = issue['slug']
        issue_articles[issue_slug] = []

        for article_ref in issue.get('articles', []):
            article_slug = article_ref['slug']
            if article_slug in all_articles:
                issue_articles[issue_slug].append(all_articles[article_slug])
                assigned_slugs.add(article_slug)

    # Articles not assigned to any issue go into "uncategorized"
    unassigned = [a for slug, a in all_articles.items() if slug not in assigned_slugs]
    if unassigned:
        print(f"  {len(unassigned)} articles not assigned to issues")

    # Generate individual article pages
    for article_slug, article in all_articles.items():
        # Determine which issue this article belongs to
        article_issue = None
        for issue in issues:
            for article_ref in issue.get('articles', []):
                if article_ref['slug'] == article_slug:
                    article_issue = issue
                    break
            if article_issue:
                break

        # Convert markdown to HTML
        base_image_path = '../images/archive/'
        html_content = convert_markdown_to_html(article['md_content'], base_image_path)

        # Build article header
        header_html = f'<h1>{article["title"]}</h1>'
        header_html += '<div class="article-meta">'
        meta_parts = []
        if article['category']:
            display_category = normalize_category(article['category'])
            meta_parts.append(f'<span class="article-label">{display_category}</span>')
        if article_issue:
            meta_parts.append(f'<span class="article-date">{article_issue["title"]} Issue</span>')
        else:
            meta_parts.append(f'<span class="article-date">{article["year"]}</span>')
        if article['author']:
            meta_parts.append(f'<span class="article-author">By {article["author"]}</span>')
        header_html += ' &bull; '.join(meta_parts)
        header_html += '</div>'

        # Back link - to issue page if assigned, otherwise to archive
        if article_issue:
            back_link = f'<a href="{article_issue["slug"]}.html" class="btn-outline">&larr; Back to {article_issue["title"]} Issue</a>'
        else:
            back_link = '<a href="index.html" class="btn-outline">&larr; Back to Archive</a>'

        original_link = f'<a href="{article["original_url"]}" class="btn-outline" target="_blank">View Original</a>' if article['original_url'] else ''

        # Get layout
        layout = layouts.get('base')

        # Create full page
        page_html = layout.replace('{{title}}', f'{article["title"]} - Go Semi & Beyond Archive')
        page_html = page_html.replace('{{body_class}}', '')
        page_html = page_html.replace('{{content}}', f'''
    <article class="article-page archive-article">
        <div class="article-header">
            {header_html}
        </div>
        <div class="article-body">
            {html_content}
        </div>
        <footer class="article-footer" style="margin-top: 40px; padding-top: 20px; border-top: 1px solid var(--border);">
            {back_link}
            {original_link}
        </footer>
    </article>
''')
        page_html = process_template(page_html, partials)

        # Fix relative paths for nested archive pages
        page_html = fix_relative_paths(page_html, '../')

        # Write output
        output_file = archive_output_dir / f'{article_slug}.html'
        output_file.write_text(page_html, encoding='utf-8')
        processed += 1

    # Generate issue pages
    for issue in issues:
        issue_slug = issue['slug']
        articles = issue_articles.get(issue_slug, [])

        generate_issue_page(issue, articles, layouts, partials, archive_output_dir)
        print(f"  Generated issue page: {issue_slug}.html ({len(articles)} articles)")

    # Generate archive index (list of issues)
    generate_archive_index_page(issues, issue_articles, unassigned, layouts, partials)

    return processed


def generate_issue_page(issue, articles, layouts, partials, output_dir):
    """Generate a page for a single issue listing its articles."""
    issue_html = f'''
    <div class="issue-page">
        <header class="issue-header">
            <h1>{issue['title']} Issue</h1>
            <p><a href="../archive.html">&larr; Back to All Issues</a></p>
        </header>
        <div class="issue-content">
'''

    if articles:
        issue_html += '<div class="issue-articles">'
        for article in articles:
            display_category = normalize_category(article.get('category', '')) if article.get('category') else ''
            category_badge = f'<span class="article-label">{display_category}</span>' if display_category else ''
            # Clean up excerpt - remove "Posted in" text
            excerpt = article.get('excerpt', '')
            excerpt = re.sub(r'^Posted\s+in\s+\S+\s*', '', excerpt).strip()
            if len(excerpt) > 200:
                excerpt = excerpt[:200] + '...'
            issue_html += f'''
            <article class="issue-article-item">
                <div class="issue-article-content">
                    {category_badge}
                    <h3><a href="{article['slug']}.html">{article['title']}</a></h3>
                    {f'<p class="article-excerpt">{excerpt}</p>' if excerpt else ''}
                </div>
            </article>
'''
        issue_html += '</div>'
    else:
        issue_html += '<p class="no-articles">No articles available for this issue.</p>'

    # Add "On the Lighter Side" section if image exists
    lighter_side_image = issue.get('lighter_side_image', '')
    if lighter_side_image:
        issue_html += f'''
            <div class="lighter-side-section" style="margin-top: 40px; padding-top: 30px; border-top: 1px solid var(--border);">
                <h3>On the Lighter Side</h3>
                <img src="../images/archive/lighter-side/{lighter_side_image}" alt="On the Lighter Side - {issue['title']}" style="max-width: 100%; border-radius: 8px; margin-top: 15px;">
            </div>
'''

    issue_html += '''
        </div>
    </div>

    <section class="cta-section">
        <div class="container">
            <h2>Stay Informed</h2>
            <p>Subscribe to Go Semi & Beyond for the latest semiconductor insights.</p>
            <a href="https://visitor.r20.constantcontact.com/manage/optin?v=001y_Bo5goCBKQ5mpCMPMk9NZ99QMnLrLllc1SVvjz3oBDPSK7NuaD2lmbp7Qd60Oy3ftqVE4iZfLT8xvaduZ92LDuKgDRcJgGp19iRFGA-2EqbiZuQnFXcLv5m5oWB7xioLSQR2RO7XNixpn3YPSNXUJ4X2lHntVromrWTUzGfYQ4%3D" class="btn-primary" target="_blank">Subscribe Today</a>
        </div>
    </section>
'''

    # Get layout and build page
    layout = layouts.get('base')
    page_html = layout.replace('{{title}}', f'{issue["title"]} Issue - Go Semi & Beyond Archive')
    page_html = page_html.replace('{{body_class}}', '')
    page_html = page_html.replace('{{content}}', issue_html)
    page_html = process_template(page_html, partials)

    # Fix relative paths - exclude article links (long slugs with multiple hyphens)
    # Article slugs have 2+ hyphens, nav pages like current-issue.html have just 1
    page_html = fix_relative_paths(page_html, '../', exclude_patterns=[r'^[a-z0-9]+(-[a-z0-9]+){2,}\.html$'])

    # Write output
    output_file = output_dir / f'{issue["slug"]}.html'
    output_file.write_text(page_html, encoding='utf-8')


def generate_archive_index_page(issues, issue_articles, unassigned, layouts, partials):
    """Generate the archive index page listing all issues."""
    archive_html = '''
    <div class="archive-page">
        <header class="archive-header">
            <h1>Past Issues</h1>
            <p>Browse our complete archive of GO SEMI & BEYOND newsletter issues.</p>
        </header>
        <div class="archive-content">
'''

    # Group issues by year
    issues_by_year = {}
    for issue in issues:
        year = issue['year']
        if year not in issues_by_year:
            issues_by_year[year] = []
        issues_by_year[year].append(issue)

    # Sort years descending
    for year in sorted(issues_by_year.keys(), reverse=True):
        year_issues = issues_by_year[year]
        archive_html += f'''
        <section class="archive-year">
            <h2>{year}</h2>
            <div class="issue-grid">
'''
        # Sort issues by month (reverse chronological)
        month_order = ['December', 'November', 'October', 'September', 'August', 'July',
                       'June', 'May', 'April', 'March', 'February', 'January']
        year_issues_sorted = sorted(year_issues, key=lambda x: month_order.index(x['month']) if x['month'] in month_order else 12)

        for issue in year_issues_sorted:
            article_count = len(issue_articles.get(issue['slug'], []))
            archive_html += f'''
                <a href="archive/{issue['slug']}.html" class="issue-card">
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

    archive_html += '''
        </div>
    </div>

    <section class="cta-section">
        <div class="container">
            <h2>Stay Informed</h2>
            <p>Subscribe to Go Semi & Beyond for the latest semiconductor insights.</p>
            <a href="https://visitor.r20.constantcontact.com/manage/optin?v=001y_Bo5goCBKQ5mpCMPMk9NZ99QMnLrLllc1SVvjz3oBDPSK7NuaD2lmbp7Qd60Oy3ftqVE4iZfLT8xvaduZ92LDuKgDRcJgGp19iRFGA-2EqbiZuQnFXcLv5m5oWB7xioLSQR2RO7XNixpn3YPSNXUJ4X2lHntVromrWTUzGfYQ4%3D" class="btn-primary" target="_blank">Subscribe Today</a>
        </div>
    </section>
'''

    # Get layout and build page
    layout = layouts.get('base')
    page_html = layout.replace('{{title}}', 'Past Issues - Go Semi & Beyond')
    page_html = page_html.replace('{{body_class}}', '')
    page_html = page_html.replace('{{content}}', archive_html)
    page_html = process_template(page_html, partials)

    # Write output
    output_file = OUTPUT_DIR / 'archive.html'
    output_file.write_text(page_html, encoding='utf-8')
    print(f"  Generated archive index: archive.html")


def process_markdown_content(layouts, partials):
    """Process markdown content from content/issues/ directory."""
    if not CONTENT_DIR.exists():
        return 0

    issues_dir = CONTENT_DIR / 'issues'
    if not issues_dir.exists():
        return 0

    processed = 0
    print("\nProcessing markdown content:")

    for issue_dir in issues_dir.iterdir():
        if not issue_dir.is_dir():
            continue

        issue_slug = issue_dir.name
        print(f"  Processing issue: {issue_slug}")

        # Copy issue images to output
        media_dir = issue_dir / 'media'
        if media_dir.exists():
            output_images_dir = OUTPUT_DIR / 'images' / 'issues' / issue_slug
            output_images_dir.mkdir(parents=True, exist_ok=True)
            for img_file in media_dir.iterdir():
                if img_file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.emf']:
                    shutil.copy2(img_file, output_images_dir / img_file.name)
            print(f"    Copied images to images/issues/{issue_slug}/")

        # Process individual article markdown files
        articles_dir = issue_dir / 'articles'
        if articles_dir.exists():
            for article_file in articles_dir.glob('*.md'):
                content = article_file.read_text(encoding='utf-8')
                metadata, md_content = parse_front_matter(content)

                # Get article slug from metadata or filename
                article_slug = metadata.get('slug', article_file.stem)

                # Convert markdown to HTML
                base_image_path = f'images/issues/{issue_slug}/'
                html_content = convert_markdown_to_html(md_content, base_image_path)

                # Get metadata values
                title = metadata.get('title', article_slug.replace('-', ' ').title())
                category = metadata.get('category', 'Article')
                author = metadata.get('author', '')
                date = metadata.get('date', '')
                excerpt = metadata.get('excerpt', '')

                # Build article header with metadata
                header_html = f'<h1>{title}</h1>'
                if category or date or author:
                    header_html += '<div class="article-meta">'
                    meta_parts = []
                    if category:
                        meta_parts.append(f'<span class="article-label">{category}</span>')
                    if date:
                        meta_parts.append(f'<span class="article-date">{date}</span>')
                    if author:
                        meta_parts.append(f'<span class="article-author">By {author}</span>')
                    header_html += ' &bull; '.join(meta_parts)
                    header_html += '</div>'

                # Wrap in article layout
                article_layout = layouts.get('article', layouts.get('base'))

                # Create full page
                page_html = article_layout.replace('{{title}}', title)
                page_html = page_html.replace('{{content}}', f'''
    <article class="article-full">
        <header class="article-header">
            {header_html}
        </header>
        <div class="article-body">
            {html_content}
        </div>
        <footer class="article-footer">
            <a href="current-issue.html" class="btn-outline">&larr; Back to Current Issue</a>
        </footer>
    </article>
''')
                page_html = process_template(page_html, partials)

                # Write output - use article- prefix for article pages
                output_file = OUTPUT_DIR / f'article-{article_slug}.html'
                output_file.write_text(page_html, encoding='utf-8')
                print(f"    Generated: article-{article_slug}.html")
                processed += 1

        # Process the main issue markdown if it exists (for full issue view)
        issue_md = issue_dir / 'issue.md'
        if issue_md.exists():
            content = issue_md.read_text(encoding='utf-8')
            metadata, md_content = parse_front_matter(content)

            # Convert markdown to HTML
            base_image_path = f'images/issues/{issue_slug}/'
            html_content = convert_markdown_to_html(md_content, base_image_path)

            # Wrap in article layout
            article_layout = layouts.get('article', layouts.get('base'))
            title = metadata.get('title', f'{issue_slug} Issue')

            # Create full page
            page_html = article_layout.replace('{{title}}', title)
            page_html = page_html.replace('{{content}}', f'''
    <article class="article-full">
        <header class="article-header">
            <h1>{title}</h1>
        </header>
        <div class="article-body">
            {html_content}
        </div>
    </article>
''')
            page_html = process_template(page_html, partials)

            # Write output
            output_file = OUTPUT_DIR / f'{issue_slug}-issue-content.html'
            output_file.write_text(page_html, encoding='utf-8')
            print(f"    Generated: {issue_slug}-issue-content.html")
            processed += 1

    return processed


def get_current_issue_metadata():
    """Load metadata from the current issue's index.md file."""
    issues_dir = CONTENT_DIR / 'issues'
    if not issues_dir.exists():
        return {}

    # Find the most recent issue (by directory name or date in metadata)
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

    return metadata


def copy_static_assets():
    """Copy static asset directories (css, js, images) to output directory."""
    print("\nCopying static assets:")
    for dir_name in STATIC_DIRS:
        src_path = STATIC_MOCKUP_DIR / dir_name
        dest_path = OUTPUT_DIR / dir_name
        if src_path.exists():
            if dest_path.exists():
                shutil.rmtree(dest_path)
            shutil.copytree(src_path, dest_path)
            print(f"  {dir_name}/ -> docs/{dir_name}/")


def build_templates():
    """Build all templates from src/ to the output directory."""
    print("\n" + "=" * 50)
    print("Building Go Semi and Beyond templates...")
    print("=" * 50)

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Copy static assets
    copy_static_assets()

    # Load partials
    print("\nLoading partials:")
    partials = load_partials()

    if not partials:
        print("  No partials found in", PARTIALS_DIR)

    # Load layouts
    print("\nLoading layouts:")
    layouts = load_layouts()

    if not layouts:
        print("  No layouts found in", LAYOUTS_DIR)

    # Load current issue metadata for dynamic content
    print("\nLoading current issue metadata:")
    issue_metadata = get_current_issue_metadata()
    if issue_metadata:
        print(f"  Current issue: {issue_metadata.get('title', 'Unknown')}")
        if issue_metadata.get('lighter_side_image'):
            print(f"  Lighter side image: {issue_metadata.get('lighter_side_image')}")
    else:
        print("  No current issue found")

    templates_processed = 0

    # Process pages from src/pages/ (new layout-based system)
    if PAGES_DIR.exists():
        print("\nProcessing pages (with layouts):")
        for page_file in PAGES_DIR.glob('*.html'):
            content = page_file.read_text(encoding='utf-8')
            processed = process_page_with_layout(content, layouts, partials, issue_metadata)

            output_file = OUTPUT_DIR / page_file.name
            output_file.write_text(processed, encoding='utf-8')

            print(f"  pages/{page_file.name} -> docs/{page_file.name}")
            templates_processed += 1

    # Process legacy templates from src/ root (backward compatibility)
    print("\nProcessing templates (legacy):")
    for template_file in SRC_DIR.glob('*.html'):
        # Skip if in ignore patterns
        if any(pattern in str(template_file) for pattern in IGNORE_PATTERNS):
            continue

        # Read template
        content = template_file.read_text(encoding='utf-8')

        # Check if it has front-matter (new style)
        if content.startswith('---'):
            processed = process_page_with_layout(content, layouts, partials)
        else:
            # Legacy: just process partials
            processed = process_template(content, partials)

        # Write output
        output_file = OUTPUT_DIR / template_file.name
        output_file.write_text(processed, encoding='utf-8')

        print(f"  {template_file.name} -> docs/{template_file.name}")
        templates_processed += 1

    # Process markdown content
    md_processed = process_markdown_content(layouts, partials)
    templates_processed += md_processed

    # Process archive content
    archive_processed = process_archive_content(layouts, partials)
    templates_processed += archive_processed

    print(f"\nBuild complete! Processed {templates_processed} template(s).")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 50 + "\n")
    return templates_processed


def get_file_mtimes():
    """Get modification times for all source files."""
    mtimes = {}

    # Check all HTML files in src/
    for f in SRC_DIR.rglob('*.html'):
        mtimes[str(f)] = f.stat().st_mtime

    # Check markdown files in content/
    if CONTENT_DIR.exists():
        for f in CONTENT_DIR.rglob('*.md'):
            mtimes[str(f)] = f.stat().st_mtime

    # Also check CSS and JS
    for ext in ['css', 'js']:
        for f in STATIC_MOCKUP_DIR.rglob(f'*.{ext}'):
            mtimes[str(f)] = f.stat().st_mtime

    return mtimes


def watch_and_build():
    """Watch for file changes and rebuild automatically."""
    print("Watching for changes... (Ctrl+C to stop)")

    last_mtimes = get_file_mtimes()
    build_templates()  # Initial build

    try:
        while True:
            time.sleep(1)
            current_mtimes = get_file_mtimes()

            # Check for changes
            changed = False
            for filepath, mtime in current_mtimes.items():
                if filepath not in last_mtimes or last_mtimes[filepath] != mtime:
                    print(f"\nChange detected: {Path(filepath).name}")
                    changed = True
                    break

            # Check for new files
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
