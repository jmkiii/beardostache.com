#!/usr/bin/env python3
"""Regenerate index.html from existing articles only — no broken links."""
import os, re, glob, html

LIVE_SITE = os.path.dirname(os.path.abspath(__file__))
ARTICLES_DIR = os.path.join(LIVE_SITE, "articles")

def parse_article(filepath):
    """Extract title, category, author, read time from an article HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    title = title_match.group(1).strip() if title_match else os.path.basename(filepath)

    # Extract category badge
    cat_match = re.search(r'<span class="category-badge">(.*?)</span>', content)
    category = cat_match.group(1).strip() if cat_match else "Gear"

    # Extract author badge
    auth_match = re.search(r'<span class="author-badge">(.*?)</span>', content)
    author = auth_match.group(1).strip() if auth_match else "Unknown"

    # Extract read time
    rt_match = re.search(r'<span class="read-time">(.*?)</span>', content)
    read_time = rt_match.group(1).strip() if rt_match else "15 min read"

    # Extract description meta
    desc_match = re.search(r'<meta name="description" content="(.*?)">', content)
    description = desc_match.group(1).strip() if desc_match else ""

    fname = os.path.basename(filepath)
    return {
        "filename": fname,
        "title": title,
        "category": category,
        "author": author,
        "read_time": read_time,
        "description": description,
    }

def category_color(cat):
    colors = {
        "Mechanical Keyboard": "#1a73e8",
        "Cast Iron": "#c2410c",
        "Wool Socks": "#7b1fa2",
        "Edc Knife": "#4caf50",
        "Flashlight": "#ff9800",
        "Watch": "#9c27b0",
        "Backpack": "#00acc1",
        "Leather Boot": "#795548",
        "Fountain Pen": "#e91e63",
        "Camping": "#4caf50",
        "Kitchen Knife": "#f44336",
        "Coffee": "#795548",
        "Audio": "#9c27b0",
        "Office": "#607d8b",
        "Fitness": "#f44336",
    }
    return colors.get(cat, "#64748b")

def build_article_card(a, section="latest"):
    cat_color = category_color(a["category"])
    # Derive a friendly link text from title
    link_text = a["title"]
    if section == "latest":
        return f'''      <article class="article-card">
        <div class="card-meta">
          <span class="badge cat" style="background-color:{cat_color};">{a["category"]}</span>
          <span class="badge author" style="background-color:#cbd5e1; color:#475569;">{a["author"]}</span>
          <span class="badge" style="background-color:#cbd5e1; color:#475569;">{a["read_time"]}</span>
        </div>
        <h3 class="card-title"><a href="articles/{a["filename"]}" class="article-link">{a["title"]}</a></h3>
        <div class="card-footer"><a href="articles/{a["filename"]}" class="read-more">Read review &rarr;</a></div>
      </article>'''
    else:
        return f'''      <article class="article-card">
        <div class="card-meta">
          <span class="badge cat" style="background-color:{cat_color};">{a["category"]}</span>
          <span class="badge author" style="background-color:#cbd5e1; color:#475569;">{a["author"]}</span>
        </div>
        <h3 class="card-title"><a href="articles/{a["filename"]}" class="article-link">{a["title"]}</a></h3>
        <div class="card-footer"><a href="articles/{a["filename"]}" class="read-more">Read &rarr;</a></div>
      </article>'''

def main():
    # Collect all existing articles
    article_files = glob.glob(os.path.join(ARTICLES_DIR, "*.html"))
    articles = [parse_article(f) for f in article_files]
    articles.sort(key=lambda a: a["filename"])

    print(f"Found {len(articles)} existing articles")

    # Split into latest (first 12) and trending/categories (rest)
    latest = articles[:12]
    rest = articles[12:]

    # Build HTML sections
    latest_cards = "\n".join(build_article_card(a, "latest") for a in latest)
    trending_cards = "\n".join(build_article_card(a, "trending") for a in rest[:8])

    # Category grouping
    from collections import defaultdict
    cats = defaultdict(list)
    for a in articles:
        cats[a["category"]].append(a)

    category_sections = ""
    for cat_name in sorted(cats.keys()):
        cat_articles = cats[cat_name][:4]  # max 4 per category
        cards = "\n".join(build_article_card(a, "category") for a in cat_articles)
        category_sections += f'''
    <section class="section-header">
      <h2 class="section-title"><span class="cat-badge">{cat_name}</span>{cat_name}</h2>
    </section>
    <div class="grid-4">
{cards}
    </div>'''

    # Read the CSS and head from existing index.html
    with open(os.path.join(LIVE_SITE, "index.html"), 'r', encoding='utf-8') as f:
        existing = f.read()

    # Extract everything up to </style>
    head_end = existing.index('</style>') + len('</style>')
    head_section = existing[:head_end]

    # Build new body
    body = f'''<body>
  <header>
    <div class="container header-inner">
      <a href="/" class="logo">Beard<span class="accent">ostache</span></a>
      <nav class="nav-links">
        <a href="#trending">Trending</a>
        <a href="#categories">Categories</a>
        <a href="4080_rivalry_blog.html">Rivalry</a>
        <a href="#latest">Latest</a>
      </nav>
      <span class="tracking-badge">Amazon Tag: knoxyknoxer-20</span>
    </div>
  </header>

  <main class="container">

    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <span class="hero-kicker">Featured Review</span>
        <h1>THE 4080 vs MAC RIVALRY</h1>
        <p class="hero-sub">Two machines. One Amazon tracking ID. {len(articles)} Reddit-verified gear reviews. Real opinions, honest reviews.</p>
        <div class="hero-meta">
          <div class="hero-meta-item">📊 {len(articles)} Articles</div>
          <div class="hero-meta-item">🔥 2 Competing Machines</div>
          <div class="hero-meta-item">💬 Reddit-Cited</div>
        </div>
        <div style="margin-top: 24px;">
          <a href="https://www.amazon.com/s?k=mechanical+keyboard&tag=knoxyknoxer-20" target="_blank" rel="noopener" style="display:inline-block; background: rgba(255,255,255,0.1); color: white; padding: 10px 20px; border-radius: 6px; font-size: 0.9rem; text-decoration: none; border: 1px solid rgba(255,255,255,0.3); margin-right: 8px;">Keyboards on Amazon</a>
          <a href="https://www.amazon.com/s?k=fountain+pen&tag=knoxyknoxer-20" target="_blank" rel="noopener" style="display:inline-block; background: rgba(255,255,255,0.1); color: white; padding: 10px 20px; border-radius: 6px; font-size: 0.9rem; text-decoration: none; border: 1px solid rgba(255,255,255,0.3); margin-right: 8px;">Fountain Pens on Amazon</a>
          <a href="https://www.amazon.com/s?k=cast+iron+skillet&tag=knoxyknoxer-20" target="_blank" rel="noopener" style="display:inline-block; background: rgba(255,255,255,0.1); color: white; padding: 10px 20px; border-radius: 6px; font-size: 0.9rem; text-decoration: none; border: 1px solid rgba(255,255,255,0.3);">Cast Iron on Amazon</a>
        </div>
        <a href="4080_rivalry_blog.html" class="hero-btn">Read the Rivalry &rarr;</a>
      </div>
    </section>

    <!-- Latest Section -->
    <section class="section-header" id="latest">
      <h2 class="section-title">Latest Reviews</h2>
      <a href="#" class="view-all">View all {len(articles)} &rarr;</a>
    </section>
    <div class="grid-3">
{latest_cards}
    </div>

    <!-- Trending Section -->
    <section id="trending" class="section-header">
      <h2 class="section-title"><span class="cat-badge">Trending</span>Most Discussed</h2>
      <a href="#" class="view-all">View all &rarr;</a>
    </section>
    <div class="grid-4">
{trending_cards}
    </div>

    <!-- Category Sections -->
    <section id="categories" class="section-header">
      <h2 class="section-title">Categories</h2>
      <a href="#" class="view-all">Browse all &rarr;</a>
    </section>
{category_sections}

    <!-- Rivalry Section -->
    <section class="rivalry-section">
      <div class="rivalry-content">
        <div class="rivalry-header">
          <div class="rivalry-side">
            <h3>The 4080</h3>
            <p>Technical, data-focused, dismissive of hype. Writes like an engineer who has taken the thing apart.</p>
            <a href="4080_rivalry_blog.html" class="rivalry-btn">Read 4080's Take &rarr;</a>
          </div>
          <div class="rivalry-vs">vs</div>
          <div class="rivalry-side">
            <h3>Mac</h3>
            <p>Literary, personal, observational, empathetic. Writes like someone who has lived with the object for years.</p>
            <a href="mac_rivalry_blog.html" class="rivalry-btn">Read Mac's Take &rarr;</a>
          </div>
        </div>
      </div>
    </section>

    <!-- Newsletter -->
    <section class="newsletter">
      <h3>Get New Reviews in Your Inbox</h3>
      <p>Join readers getting gear reviews from two competing machines.</p>
      <form class="newsletter-form">
        <input type="email" placeholder="Enter your email" required>
        <button type="submit">Subscribe</button>
      </form>
    </section>
  </main>

  <footer>
    <div class="container footer-inner">
      <span>&copy; 2026 beardostache.com &bull; Tracking ID: knoxyknoxer-20</span>
      <span>Real Reddit reviews &bull; Honest reviews</span>
    </div>
  </footer>
</body>
</html>'''

    new_html = head_section + "\n" + body
    with open(os.path.join(LIVE_SITE, "index.html"), 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f"index.html regenerated with {len(articles)} working article links")

if __name__ == "__main__":
    main()