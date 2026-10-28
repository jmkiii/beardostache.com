#!/usr/bin/env python3
"""Verify beardostache.com site integrity.

Checks:
- All homepage article links resolve to existing files
- Every article has tracking ID knoxyknoxer-20
- Every article has Amazon affiliate link with knoxyknoxer-20
- Every article has rivalry note
- Every article has valid HTML structure
- Flags articles with NO Reddit quotes (need real research)
- Verifies Reddit citations are properly formatted
- Reports which articles need real research
"""
import os, re, glob, sys

LIVE_SITE = os.path.dirname(os.path.abspath(__file__))
ARTICLES_DIR = os.path.join(LIVE_SITE, "articles")

errors = []
warnings = []

def check_file(path, label):
    if not os.path.isfile(path):
        errors.append(f"{label}: MISSING FILE {path}")
        return False
    return True

# ── 1. Check homepage links ──
print("=== Checking homepage links ===")
index_path = os.path.join(LIVE_SITE, "index.html")
check_file(index_path, "Homepage")

with open(index_path, 'r', encoding='utf-8') as f:
    index_html = f.read()

homepage_links = re.findall(r'href="articles/([^"]+)"', index_html)
unique_links = sorted(set(homepage_links))
print(f"Homepage links to articles: {len(unique_links)} unique")

broken = 0
for link in unique_links:
    full_path = os.path.join(ARTICLES_DIR, link)
    if not os.path.isfile(full_path):
        broken += 1
        errors.append(f"Homepage links to MISSING article: articles/{link}")
        print(f"  BROKEN: articles/{link}")

if broken == 0:
    print("  All homepage links resolve OK")
else:
    print(f"  {broken} BROKEN links FAIL")

# ── 2. Check each article ──
print("\n=== Checking articles ===")
article_files = sorted(glob.glob(os.path.join(ARTICLES_DIR, "*.html")))
article_count = len(article_files)
print(f"Total articles: {article_count}")

articles_needing_research = []
articles_with_real_quotes = 0

for filepath in article_files:
    fname = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    article_issues = []

    # Tracking ID
    if 'knoxyknoxer-20' not in content:
        article_issues.append("Missing tracking ID knoxyknoxer-20")
    elif 'meta name="amazon-tracking-id"' not in content:
        article_issues.append("Tracking ID present but not in meta tag")

    # Amazon affiliate link
    amazon_links = re.findall(r'href="(https://www\.amazon\.com[^"]*tag=knoxyknoxer-20[^"]*)"', content)
    if not amazon_links:
        article_issues.append("No Amazon affiliate link with knoxyknoxer-20")
    else:
        print(f"  {fname}: {len(amazon_links)} affiliate link(s)")

    # Rivalry note
    if 'rivalry-note' not in content:
        article_issues.append("No rivalry note")

    # Reddit quote
    has_reddit_quote = 'reddit-quote' in content
    if not has_reddit_quote:
        article_issues.append("No Reddit quote - needs real research")
        articles_needing_research.append(fname)
        print(f"  {fname}: NO REDDIT QUOTE (needs real research)")
    else:
        # Verify citation format
        user_refs = re.findall(r'reddit\.com/user/([^/"]+)/', content)
        sub_refs = re.findall(r'reddit\.com/r/([^/"]+)/', content)
        if user_refs and sub_refs:
            articles_with_real_quotes += 1
            print(f"  {fname}: Reddit quote OK (users: {user_refs[:2]}, subreddits: {sub_refs[:2]})")
        else:
            article_issues.append("Reddit quote block present but missing user/subreddit links")
            articles_needing_research.append(fname)

    # Required HTML structure
    for tag in ['<!DOCTYPE html>', '<title>', '<h1>', '<meta name="amazon-tracking-id"']:
        if tag not in content:
            article_issues.append(f"Missing {tag}")

    # Product box
    if 'product-box' not in content:
        article_issues.append("No product-box div")

    # Template variables
    for placeholder in ['{product}', '{niche}', '{months}', '{user}', '{random}', 'TODO', 'XXX']:
        if placeholder in content:
            article_issues.append(f"Unresolved template variable: {placeholder}")

    # Clickbait check
    title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    if title_match:
        title = title_match.group(1).strip()
        bad_words = ['best', 'top 10', 'ultimate', 'shocking', 'miracle', 'game-changer']
        for bw in bad_words:
            if bw.lower() in title.lower():
                article_issues.append(f"Title contains clickbait word: {bw}")

    if article_issues:
        for issue in article_issues:
            errors.append(f"{fname}: {issue}")
            print(f"  {fname}: {issue}")

print(f"\n=== Summary ===")
print(f"Articles checked: {article_count}")
print(f"Articles with real Reddit citations: {articles_with_real_quotes}")
print(f"Articles needing real research: {len(articles_needing_research)}")
print(f"Total errors: {len(errors)}")

if errors:
    print("\n--- ERRORS / WARNINGS ---")
    for e in errors:
        print(f"  {e}")

if articles_needing_research:
    print(f"\nArticles that need real Reddit research before publishing:")
    for a in articles_needing_research:
        print(f"  - {a}")

if not errors:
    print("\nAll checks passed OK")

sys.exit(1 if errors else 0)