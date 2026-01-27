#!/usr/bin/env python3
"""
Scrape "On the Lighter Side" images from WordPress issue pages.

This script:
1. Reads issues.json to get all issue URLs
2. Fetches each issue page
3. Extracts the "On the Lighter Side" image URL
4. Downloads the image to content/archive/images/lighter-side/
5. Updates issues.json with the lighter_side_image field
"""

import json
import os
import re
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: BeautifulSoup not installed. Run: pip install beautifulsoup4")
    exit(1)

# Configuration
SCRIPT_DIR = Path(__file__).parent
CONTENT_DIR = SCRIPT_DIR.parent / 'content'
ISSUES_FILE = CONTENT_DIR / 'issues.json'
IMAGES_DIR = CONTENT_DIR / 'archive' / 'images' / 'lighter-side'

# User agent to avoid blocking
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}


def fetch_page(url):
    """Fetch a page and return its HTML content."""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
        return None


def extract_lighter_side_image(html):
    """Extract the 'On the Lighter Side' image URL from the page."""
    soup = BeautifulSoup(html, 'html.parser')

    # Look for the heading - could be h2, h3, h4, or strong in a paragraph
    lighter_side_heading = None

    # Try various heading levels and text variations
    for tag in soup.find_all(['h2', 'h3', 'h4', 'p', 'strong']):
        text = tag.get_text().strip().upper()
        if 'LIGHTER SIDE' in text or 'ON THE LIGHTER' in text:
            lighter_side_heading = tag
            break

    if not lighter_side_heading:
        return None

    # Look for the image after this heading
    # Check the next few siblings
    current = lighter_side_heading
    for _ in range(5):  # Check up to 5 elements after the heading
        current = current.find_next_sibling()
        if current is None:
            break

        # Look for img tag
        img = current.find('img') if current.name != 'img' else current
        if img and img.get('src'):
            img_url = img.get('src')
            # Try to get the full-size image (remove size suffix like -300x232)
            full_url = re.sub(r'-\d+x\d+\.', '.', img_url)
            return full_url

    # Also check parent's siblings (in case heading is wrapped)
    parent = lighter_side_heading.parent
    if parent:
        current = parent
        for _ in range(5):
            current = current.find_next_sibling()
            if current is None:
                break
            img = current.find('img') if current.name != 'img' else current
            if img and img.get('src'):
                img_url = img.get('src')
                full_url = re.sub(r'-\d+x\d+\.', '.', img_url)
                return full_url

    return None


def download_image(url, filename):
    """Download an image to the lighter-side images directory."""
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    filepath = IMAGES_DIR / filename

    # Skip if already downloaded
    if filepath.exists():
        print(f"  Already downloaded: {filename}")
        return True

    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        print(f"  Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"  Error downloading {url}: {e}")
        return False


def main():
    # Load issues
    if not ISSUES_FILE.exists():
        print(f"Error: {ISSUES_FILE} not found")
        return

    with open(ISSUES_FILE, 'r', encoding='utf-8') as f:
        issues = json.load(f)

    print(f"Found {len(issues)} issues to process\n")

    updated_count = 0

    for issue in issues:
        issue_slug = issue['slug']
        issue_url = issue['url']

        print(f"Processing: {issue['title']} ({issue_url})")

        # Fetch the issue page
        html = fetch_page(issue_url)
        if not html:
            continue

        # Extract lighter side image
        img_url = extract_lighter_side_image(html)

        if img_url:
            # Generate filename from issue slug
            # Extract file extension from URL
            parsed = urlparse(img_url)
            ext = Path(parsed.path).suffix or '.jpg'
            filename = f"{issue_slug}{ext}"

            # Download the image
            if download_image(img_url, filename):
                issue['lighter_side_image'] = filename
                issue['lighter_side_url'] = img_url
                updated_count += 1
                print(f"  Found image: {img_url}")
        else:
            print(f"  No 'On the Lighter Side' image found")

        # Be nice to the server
        time.sleep(0.5)

    # Save updated issues.json
    with open(ISSUES_FILE, 'w', encoding='utf-8') as f:
        json.dump(issues, f, indent=2, ensure_ascii=False)

    print(f"\nDone! Updated {updated_count} issues with lighter side images")
    print(f"Images saved to: {IMAGES_DIR}")


if __name__ == '__main__':
    main()
