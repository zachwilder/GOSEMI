#!/usr/bin/env python3
"""
Scraper for Go Semi & Beyond archive content.
Fetches articles from the existing WordPress site and converts to markdown.

Usage:
    python scrape_archive.py          # Scrape all articles
    python scrape_archive.py --year 2024  # Scrape specific year
    python scrape_archive.py --test   # Test with one article
"""

import os
import re
import json
import time
import argparse
import requests
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

# Configuration
BASE_URL = "https://www.gosemiandbeyond.com"
SITEMAP_URL = f"{BASE_URL}/wp-sitemap-posts-post-1.xml"
OUTPUT_DIR = Path(__file__).parent.parent / "content" / "archive"
IMAGES_DIR = OUTPUT_DIR / "images"

# Request settings
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}
DELAY_BETWEEN_REQUESTS = 0  # No delay - scraping our own site


def fetch_sitemap():
    """Fetch and parse the sitemap to get all article URLs."""
    print("Fetching sitemap...")
    response = requests.get(SITEMAP_URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'xml')

    articles = []
    for url_tag in soup.find_all('url'):
        loc = url_tag.find('loc').text
        lastmod = url_tag.find('lastmod')
        lastmod_date = lastmod.text if lastmod else None

        # Skip non-article URLs
        if any(skip in loc for skip in ['/category/', '/tag/', '/page/', '/author/']):
            continue

        articles.append({
            'url': loc,
            'lastmod': lastmod_date
        })

    print(f"Found {len(articles)} articles in sitemap")
    return articles


def extract_year_from_date(date_str):
    """Extract year from various date formats."""
    if not date_str:
        return "unknown"

    # Try ISO format first (2024-01-15)
    match = re.search(r'(\d{4})', date_str)
    if match:
        return match.group(1)
    return "unknown"


def slugify(text):
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = text.strip('-')
    return text[:80]  # Limit length


def download_image(img_url, article_slug, img_index):
    """Download an image and return the local path."""
    try:
        response = requests.get(img_url, headers=HEADERS, timeout=30)
        if response.status_code == 200:
            # Get file extension
            ext = Path(urlparse(img_url).path).suffix or '.jpg'
            filename = f"{article_slug}-{img_index}{ext}"

            # Save image
            img_path = IMAGES_DIR / filename
            img_path.parent.mkdir(parents=True, exist_ok=True)
            img_path.write_bytes(response.content)

            return f"images/{filename}"
    except Exception as e:
        print(f"    Failed to download image: {e}")
    return None


def html_to_markdown(element):
    """Convert HTML content to markdown."""
    if element is None:
        return ""

    markdown = ""

    for child in element.children:
        if isinstance(child, str):
            markdown += child
        elif child.name == 'p':
            markdown += html_to_markdown(child) + "\n\n"
        elif child.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(child.name[1])
            markdown += '#' * level + ' ' + child.get_text().strip() + "\n\n"
        elif child.name == 'strong' or child.name == 'b':
            markdown += f"**{child.get_text()}**"
        elif child.name == 'em' or child.name == 'i':
            markdown += f"*{child.get_text()}*"
        elif child.name == 'a':
            href = child.get('href', '')
            text = child.get_text()
            markdown += f"[{text}]({href})"
        elif child.name == 'ul':
            for li in child.find_all('li', recursive=False):
                markdown += f"- {li.get_text().strip()}\n"
            markdown += "\n"
        elif child.name == 'ol':
            for i, li in enumerate(child.find_all('li', recursive=False), 1):
                markdown += f"{i}. {li.get_text().strip()}\n"
            markdown += "\n"
        elif child.name == 'blockquote':
            for line in child.get_text().strip().split('\n'):
                markdown += f"> {line}\n"
            markdown += "\n"
        elif child.name == 'img':
            # Images handled separately
            pass
        elif child.name == 'br':
            markdown += "\n"
        elif child.name == 'figure':
            markdown += html_to_markdown(child)
        elif child.name == 'figcaption':
            markdown += f"*{child.get_text().strip()}*\n\n"
        elif child.name in ['div', 'span', 'section', 'article']:
            markdown += html_to_markdown(child)
        elif hasattr(child, 'children'):
            markdown += html_to_markdown(child)

    return markdown


def scrape_article(url):
    """Scrape a single article and return structured data."""
    print(f"  Fetching: {url}")

    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        if response.status_code != 200:
            print(f"    HTTP {response.status_code}")
            return None

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract title
        title_tag = soup.find('h1', class_='entry-title') or soup.find('h1')
        title = title_tag.get_text().strip() if title_tag else "Untitled"

        # Extract date
        date_tag = soup.find('time', class_='entry-date') or soup.find('time')
        date_str = date_tag.get('datetime', '') if date_tag else ""
        if not date_str and date_tag:
            date_str = date_tag.get_text().strip()

        # Extract author
        author_tag = soup.find('span', class_='author') or soup.find('a', rel='author')
        author = author_tag.get_text().strip() if author_tag else ""

        # Extract category
        category_tag = soup.find('span', class_='cat-links') or soup.find('a', rel='category')
        category = category_tag.get_text().strip() if category_tag else ""

        # Extract main content
        content_div = (
            soup.find('div', class_='entry-content') or
            soup.find('article') or
            soup.find('main')
        )

        # Extract images
        images = []
        if content_div:
            for img in content_div.find_all('img'):
                src = img.get('src') or img.get('data-src')
                if src:
                    # Make absolute URL
                    if not src.startswith('http'):
                        src = urljoin(BASE_URL, src)
                    alt = img.get('alt', '')
                    images.append({'src': src, 'alt': alt})

        # Convert content to markdown
        content_md = html_to_markdown(content_div) if content_div else ""

        # Clean up markdown
        content_md = re.sub(r'\n{3,}', '\n\n', content_md)
        content_md = content_md.strip()

        # Extract excerpt (first paragraph)
        excerpt = ""
        if content_div:
            first_p = content_div.find('p')
            if first_p:
                excerpt = first_p.get_text().strip()[:200]

        return {
            'url': url,
            'title': title,
            'date': date_str,
            'author': author,
            'category': category,
            'excerpt': excerpt,
            'content': content_md,
            'images': images
        }

    except Exception as e:
        print(f"    Error: {e}")
        return None


def save_article_as_markdown(article, year):
    """Save an article as a markdown file."""
    slug = slugify(article['title'])
    year_dir = OUTPUT_DIR / year
    year_dir.mkdir(parents=True, exist_ok=True)

    # Download images and update references
    img_index = 1
    for img in article['images']:
        local_path = download_image(img['src'], slug, img_index)
        if local_path:
            # Update content with local path
            article['content'] = article['content'].replace(
                img['src'],
                f"../{local_path}"
            )
            # Add image to markdown if not already there
            if img['src'] not in article['content']:
                article['content'] += f"\n\n![{img['alt']}](../{local_path})\n"
            img_index += 1

    # Build front-matter
    title_escaped = article['title'].replace('"', "'")
    excerpt_escaped = article['excerpt'].replace('"', "'")

    front_matter = f"""---
title: "{title_escaped}"
slug: {slug}
date: {article['date']}
category: "{article['category']}"
author: "{article['author']}"
excerpt: "{excerpt_escaped}"
original_url: "{article['url']}"
---

"""

    # Write markdown file
    md_path = year_dir / f"{slug}.md"
    md_path.write_text(front_matter + article['content'], encoding='utf-8')
    print(f"    Saved: {md_path.name}")

    return md_path


def main():
    parser = argparse.ArgumentParser(description='Scrape Go Semi & Beyond archive')
    parser.add_argument('--year', type=str, help='Scrape specific year only')
    parser.add_argument('--test', action='store_true', help='Test with one article')
    parser.add_argument('--limit', type=int, help='Limit number of articles')
    args = parser.parse_args()

    # Create output directories
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # Fetch sitemap
    articles = fetch_sitemap()

    # Filter by year if specified
    if args.year:
        articles = [a for a in articles if args.year in (a['lastmod'] or '')]
        print(f"Filtered to {len(articles)} articles from {args.year}")

    # Limit for testing
    if args.test:
        articles = articles[:1]
    elif args.limit:
        articles = articles[:args.limit]

    # Process each article
    processed = 0
    failed = 0

    for article_info in articles:
        url = article_info['url']
        year = extract_year_from_date(article_info['lastmod'])

        print(f"\nProcessing [{processed + 1}/{len(articles)}]: {year}")

        article = scrape_article(url)
        if article:
            save_article_as_markdown(article, year)
            processed += 1
        else:
            failed += 1

        # Rate limiting
        time.sleep(DELAY_BETWEEN_REQUESTS)

    print(f"\n{'='*50}")
    print(f"Scraping complete!")
    print(f"  Processed: {processed}")
    print(f"  Failed: {failed}")
    print(f"  Output: {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
