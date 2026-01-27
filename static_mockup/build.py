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


def process_page_with_layout(page_content, layouts, partials):
    """Process a page file with front-matter and apply layout."""
    # Parse front-matter
    metadata, content = parse_front_matter(page_content)

    # Get the layout
    layout_name = metadata.get('layout', 'base')
    if layout_name not in layouts:
        print(f"  Warning: Layout '{layout_name}' not found, using content as-is")
        return process_template(page_content, partials)

    layout = layouts[layout_name]

    # Replace {{title}} and {{content}} in layout
    result = layout.replace('{{title}}', metadata.get('title', 'Go Semi & Beyond'))
    result = result.replace('{{content}}', content)

    # Process partials
    result = process_template(result, partials)

    return result


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

    templates_processed = 0

    # Process pages from src/pages/ (new layout-based system)
    if PAGES_DIR.exists():
        print("\nProcessing pages (with layouts):")
        for page_file in PAGES_DIR.glob('*.html'):
            content = page_file.read_text(encoding='utf-8')
            processed = process_page_with_layout(content, layouts, partials)

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
