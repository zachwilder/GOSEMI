#!/usr/bin/env python3
"""
Simple template build script for Go Semi and Beyond static mockup.

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
"""

import os
import re
import sys
import time
import shutil
import argparse
from pathlib import Path

# Configuration
SRC_DIR = Path(__file__).parent / 'src'
PARTIALS_DIR = SRC_DIR / 'partials'
LAYOUTS_DIR = SRC_DIR / 'layouts'
PAGES_DIR = SRC_DIR / 'pages'
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
                    metadata[key.strip()] = value.strip()
            # Return content without front-matter
            return metadata, parts[2].strip()

    return metadata, content


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
