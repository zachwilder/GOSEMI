#!/usr/bin/env python3
"""
Scraper for Go Semi & Beyond issue structure.
Fetches issue pages and maps articles to their issues.

Usage:
    python scrape_issues.py
"""

import re
import json
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

BASE_URL = "https://www.gosemiandbeyond.com"
PAST_ISSUES_URL = f"{BASE_URL}/full-width/"
OUTPUT_DIR = Path(__file__).parent.parent / "content"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}


def fetch_issue_list():
    """Fetch list of all issues from the past issues page."""
    print("Fetching past issues page...")
    response = requests.get(PAST_ISSUES_URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    issues = []
    # Find all links to issue pages
    for link in soup.find_all('a', href=True):
        href = link.get('href', '')
        text = link.get_text().strip()

        # Match issue links like "June 2024", "March 2023", etc.
        if re.search(r'-issue/?$', href) or re.search(r'(january|february|march|april|may|june|july|august|september|october|november|december)-\d{4}/?$', href, re.IGNORECASE):
            # Extract month and year from text or URL
            match = re.search(r'(january|february|march|april|may|june|july|august|september|october|november|december)\s*(\d{4})', text, re.IGNORECASE)
            if not match:
                match = re.search(r'(january|february|march|april|may|june|july|august|september|october|november|december)-(\d{4})', href, re.IGNORECASE)

            if match:
                month = match.group(1).capitalize()
                year = match.group(2)

                # Make URL absolute
                if not href.startswith('http'):
                    href = urljoin(BASE_URL, href)

                issue = {
                    'title': f"{month} {year}",
                    'month': month,
                    'year': year,
                    'url': href,
                    'slug': f"{month.lower()}-{year}"
                }

                # Avoid duplicates
                if not any(i['slug'] == issue['slug'] for i in issues):
                    issues.append(issue)
                    print(f"  Found: {issue['title']}")

    return sorted(issues, key=lambda x: (x['year'], x['month']), reverse=True)


def fetch_issue_articles(issue_url):
    """Fetch article links from an issue page."""
    print(f"  Fetching articles from {issue_url}")

    try:
        response = requests.get(issue_url, headers=HEADERS, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')

        articles = []
        content = soup.find('article') or soup.find('div', class_='entry-content') or soup.find('main')

        if content:
            for link in content.find_all('a', href=True):
                href = link.get('href', '')
                text = link.get_text().strip()

                # Skip non-article links
                skip_patterns = ['/category/', '/tag/', '/full-width/', '-issue/', '/go-poll/',
                                '/about', '/current-issue', '/subscribe', 'mailto:',
                                'twitter.com', 'linkedin.com', 'facebook.com', 'wikipedia.org']
                if any(skip in href.lower() for skip in skip_patterns):
                    continue

                # Must be a gosemiandbeyond.com link
                if 'gosemiandbeyond.com' in href:
                    # Extract slug from URL
                    parsed = urlparse(href)
                    path = parsed.path.strip('/')

                    # Skip if path contains year/month structure or is empty
                    if not path or '/' in path:
                        continue

                    # Skip if it's just a homepage or issue page
                    if path in ['', 'home', 'current-issue', 'full-width', 'about-2', 'go-poll']:
                        continue

                    # Skip issue pages (month-year pattern)
                    if re.match(r'^(january|february|march|april|may|june|july|august|september|october|november|december)-\d{4}', path, re.IGNORECASE):
                        continue

                    articles.append({
                        'url': href.rstrip('/'),
                        'slug': path,
                        'text': text[:100] if text else ''
                    })

        # Deduplicate
        seen = set()
        unique_articles = []
        for article in articles:
            if article['slug'] not in seen:
                seen.add(article['slug'])
                unique_articles.append(article)

        return unique_articles

    except Exception as e:
        print(f"    Error: {e}")
        return []


def slugify(text):
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = text.strip('-')
    return text[:80]


def main():
    # Fetch issue list
    issues = fetch_issue_list()
    print(f"\nFound {len(issues)} issues")

    # Fetch articles for each issue
    print("\nFetching articles for each issue:")
    for issue in issues:
        articles = fetch_issue_articles(issue['url'])
        issue['articles'] = articles
        print(f"    {issue['title']}: {len(articles)} articles")

    # Save issue mapping
    output_file = OUTPUT_DIR / 'issues.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(issues, f, indent=2)

    print(f"\nSaved issue mapping to {output_file}")

    # Print summary
    print("\n" + "=" * 50)
    print("Issue Summary:")
    for issue in issues:
        print(f"  {issue['title']}: {len(issue.get('articles', []))} articles")


if __name__ == '__main__':
    main()
