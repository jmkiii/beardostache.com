import os, re, random

articles_dir = 'articles'
articles = []

for f in os.listdir(articles_dir):
    if not f.endswith('.html'):
        continue
    path = os.path.join(articles_dir, f)
    mtime = os.path.getmtime(path)
    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
        content = fh.read()
    title_match = re.search(r'<title>([^<]+)</title>', content)
    title = title_match.group(1) if title_match else f.replace('-', ' ').title()
    cat_match = re.search(r'<span class="category-badge">([^<]+)</span>', content)
    cat = cat_match.group(1) if cat_match else 'Gear'
    articles.append({'file': f, 'title': title, 'cat': cat, 'mtime': mtime})

articles.sort(key=lambda x: x['mtime'], reverse=True)

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

latest = articles[:12]
random.seed(42)
trending = random.sample(articles[6:], min(8, len(articles)-6))

categories = {}
for a in articles:
    cat = a['cat']
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(a)

cat_order = sorted(categories.keys(), key=lambda c: len(categories[c]), reverse=True)

# Build latest section HTML
latest_html = ''
for a in latest:
    latest_html += f'''      <article class="article-card">
        <div class="card-meta">
          <span class="badge cat" style="background-color:#64748b;">{a['cat']}</span>
          <span class="badge" style="background-color:#cbd5e1; color:#475569;">15 min read</span>
        </div>
        <h3 class="card-title"><a href="articles/{a['file']}" class="article-link">{esc(a['title'])}</a></h3>
        <div class="card-footer"><a href="articles/{a['file']}" class="read-more">Read review &rarr;</a></div>
      </article>'''

# Build trending section HTML
trending_html = ''
for a in trending:
    trending_html += f'''    <article class="article-card">
        <div class="card-meta">
          <span class="badge" style="background-color:#cbd5e1; color:#475569;">15 min read</span>
        </div>
        <h3 class="card-title"><a href="articles/{a['file']}" class="article-link">{esc(a['title'])}</a></h3>
        <div class="card-footer"><a href="articles/{a['file']}" class="read-more">Read &rarr;</a></div>
      </article>'''

# Build category sections HTML
category_html = ''
for cat in cat_order[:6]:
    cat_articles = categories[cat][:4]
    cat_html_content = ''
    for a in cat_articles:
        cat_html_content += f'''        <article class="article-card">
          <h3 class="card-title"><a href="articles/{a['file']}" class="article-link">{esc(a['title'])}</a></h3>
          <div class="card-footer"><a href="articles/{a['file']}" class="read-more">Read &rarr;</a></div>
        </article>'''
    category_html += f'''
    <section class="section-header">
      <h2 class="section-title"><span class="cat-badge">{cat}</span>{cat}</h2>
    </section>
    <div class="grid-4">{cat_html_content}</div>'''

# Build complete HTML
html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Beardostache — Real Reddit Reviews & Gear Picks</title>
  <meta name="description" content="What Reddit actually says about the best gear. {len(articles)} Reddit-verified gear reviews. Real opinions, honest reviews.">
  <meta name="amazon-tracking-id" content="knoxyknoxer-20">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:wght@700;900&display=swap" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    :root {{
      --bg: #ffffff; --surface: #f8fafc; --text: #0f172a;
      --text-muted: #64748b; --accent: #1a73e8; --border: #e2e8f0;
      --max-width: 1200px;
    }}
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background: var(--bg); color: var(--text); line-height: 1.6; }}
    a {{ color: var(--accent); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .container {{
      max-width: var(--max-width); margin: 0 auto; padding: 0 24px; }}
    header {{
      background: var(--bg); border-bottom: 1px solid var(--border);
      position: sticky; top: 0; z-index: 100; }}
    .header-inner {{
      display: flex; align-items: center; justify-content: space-between;
      padding: 20px 0; }}
    .logo {{
      font-family: 'Playfair Display', serif; font-size: 1.75rem;
      font-weight: 900; letter-spacing: -0.02em; color: var(--text); }}
    .logo .accent {{ color: var(--accent); }}
    .nav-links {{
      display: flex; gap: 24px; font-size: 0.95rem;
      font-weight: 500; }}
    .nav-links a {{ color: var(--text-muted); }}
    .nav-links a:hover {{ color: var(--accent); }}
    .tracking-badge {{
      background: var(--surface); color: var(--text-muted);
      font-size: 0.75rem; font-weight: 600; padding: 4px 10px;
      border-radius: 20px; border: 1px solid var(--border); }}
    .hero {{
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
      color: white; padding: 80px 0; border-radius: 0 0 48px 48px;
      margin-bottom: 60px; position: relative; overflow: hidden; }}
    .hero-content {{
      position: relative; z-index: 2; max-width: 700px; }}
    .hero-kicker {{
      display: inline-block;
      background: rgba(255,255,255,0.1); color: #93c5fd;
      font-size: 0.75rem; font-weight: 700; text-transform: uppercase;
      letter-spacing: 0.1em; padding: 6px 14px;
      border-radius: 20px; margin-bottom: 16px;
      border: 1px solid rgba(255,255,255,0.2); }}
    .hero h1 {{
      font-family: 'Playfair Display', serif; font-size: 3.25rem;
      font-weight: 900; line-height: 1.1; margin-bottom: 20px;
      letter-spacing: -0.03em; }}
    .hero-sub {{
      font-size: 1.25rem; color: #cbd5e1;
      margin-bottom: 32px; max-width: 560px; line-height: 1.7; }}
    .hero-meta {{
      display: flex; gap: 20px; margin-bottom: 32px; }}
    .hero-meta-item {{
      background: rgba(255,255,255,0.1);
      padding: 8px 16px; border-radius: 8px; font-size: 0.875rem;
      backdrop-filter: blur(4px); }}
    .hero-btn {{
      display: inline-block; background: var(--accent); color: white;
      padding: 16px 32px; border-radius: 8px; font-weight: 700;
      font-size: 1.1rem; box-shadow: 0 4px 14px rgba(26, 115, 232, 0.4);
      text-decoration: none; }}
    .hero-btn:hover {{ background: #155eb3; text-decoration: none; }}
    .section-header {{
      display: flex; align-items: center; justify-content: space-between;
      margin: 60px 0 28px 0; padding-bottom: 16px;
      border-bottom: 1px solid var(--border); }}
    .section-title {{
      font-size: 1.5rem; font-weight: 700; letter-spacing: -0.02em; }}
    .section-title .cat-badge {{
      display: inline-block; background: var(--surface);
      color: var(--text-muted); font-size: 0.7rem;
      font-weight: 700; text-transform: uppercase;
      letter-spacing: 0.08em; padding: 4px 10px;
      border-radius: 6px; margin-right: 10px;
      border: 1px solid var(--border); }}
    .view-all {{
      font-size: 0.875rem; font-weight: 600;
      color: var(--accent); text-decoration: none; }}
    .view-all:hover {{ text-decoration: underline; }}
    .article-card {{
      background: white; border: 1px solid var(--border);
      border-radius: 12px; padding: 20px;
      transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
      display: flex; flex-direction: column; height: 100%; }}
    .article-card:hover {{
      transform: translateY(-4px);
      box-shadow: 0 12px 24px rgba(0,0,0,0.08);
      border-color: var(--accent); }}
    .card-meta {{
      display: flex; gap: 10px; margin-bottom: 10px;
      flex-wrap: wrap; }}
    .badge {{
      font-size: 0.65rem; font-weight: 700;
      text-transform: uppercase; letter-spacing: 0.05em;
      padding: 3px 8px; border-radius: 4px;
      color: white; }}
    .badge.cat {{ background: var(--accent); }}
    .card-title {{
      font-size: 1.15rem; font-weight: 700;
      line-height: 1.3; margin-bottom: 10px;
      letter-spacing: -0.01em; }}
    .card-title a {{ color: var(--text); }}
    .card-title a:hover {{ color: var(--accent); text-decoration: none; }}
    .card-excerpt {{
      font-size: 0.9rem; color: var(--text-muted);
      margin-bottom: 16px; flex-grow: 1; }}
    .card-footer {{
      display: flex; justify-content: space-between;
      align-items: center; margin-top: auto; }}
    .read-more {{
      font-size: 0.875rem; font-weight: 600;
      color: var(--accent); text-decoration: none; }}
    .read-more:hover {{ text-decoration: underline; }}
    .card-date {{
      font-size: 0.75rem; color: var(--text-muted);
      font-weight: 500; }}
    .grid-2 {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; }}
    .grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }}
    .grid-4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }}
    .rivalry-section {{
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
      color: white; border-radius: 24px;
      padding: 48px; margin: 60px 0;
      position: relative; overflow: hidden; }}
    .rivalry-content {{
      position: relative; z-index: 2; }}
    .rivalry-header {{
      display: flex; justify-content: space-between;
      align-items: flex-start; margin-bottom: 32px; }}
    .rivalry-side {{
      flex: 1; padding: 0 20px; }}
    .rivalry-side h3 {{
      font-family: 'Playfair Display', serif; font-size: 2rem;
      margin-bottom: 12px; }}
    .rivalry-side p {{
      color: #94a3b8; margin-bottom: 16px; }}
    .rivalry-vs {{
      display: flex; flex-direction: column;
      align-items: center; justify-content: center;
      font-size: 2.5rem; font-weight: 900;
      color: var(--accent); padding: 20px 0; }}
    .rivalry-btn {{
      display: inline-block; background: var(--accent); color: white;
      padding: 12px 28px; border-radius: 8px; font-weight: 700;
      margin-top: 8px; text-decoration: none; }}
    .rivalry-btn:hover {{ background: #155eb3; }}
    .newsletter {{
      background: var(--surface);
      border-radius: 20px; padding: 48px;
      margin: 60px 0; text-align: center;
      border: 1px solid var(--border); }}
    .newsletter h3 {{
      font-family: 'Playfair Display', serif;
      font-size: 2rem; margin-bottom: 12px; }}
    .newsletter p {{
      color: var(--text-muted); margin-bottom: 24px; }}
    .newsletter-form {{
      max-width: 480px; margin: 0 auto;
      display: flex; gap: 10px; }}
    .newsletter-form input[type="email"] {{
      flex: 1; padding: 14px 20px;
      border: 1px solid var(--border);
      border-radius: 8px; font-size: 1rem;
      background: white; }}
    .newsletter-form button {{
      background: var(--text); color: white;
      border: none; padding: 14px 28px;
      border-radius: 8px; font-weight: 600;
      cursor: pointer; }}
    .newsletter-form button:hover {{ background: #334155; }}
    footer {{
      border-top: 1px solid var(--border);
      padding: 40px 0;
      color: var(--text-muted);
      font-size: 0.875rem; }}
    .footer-inner {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap; gap: 20px; }}
    @media (max-width: 768px) {{
      .hero h1 {{ font-size: 2.25rem; }}
      .hero-sub {{ font-size: 1.1rem; }}
      .grid-2, .grid-3, .grid-4 {{ grid-template-columns: 1fr; }}
      .rivalry-section {{ padding: 32px 20px; }}
      .rivalry-vs {{ font-size: 1.75rem; padding: 12px 0; }}
      .newsletter-form {{ flex-direction: column; }}
      .nav-links {{ display: none; }}
    }}
  </style>
</head>
<body>
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
{latest_html}
    </div>

    <!-- Trending Section -->
    <section id="trending" class="section-header">
      <h2 class="section-title"><span class="cat-badge">Trending</span>Most Discussed</h2>
      <a href="#" class="view-all">View all &rarr;</a>
    </section>
    <div class="grid-4">
{trending_html}
    </div>

    <!-- Category Sections -->
    <section id="categories" class="section-header">
      <h2 class="section-title">Categories</h2>
      <a href="#" class="view-all">Browse all &rarr;</a>
    </section>
{category_html}

    <!-- Rivalry Section -->
    <section class="rivalry-section">
      <div class="rivalry-content">
        <div class="rivalry-header">
          <div class="rivalry-side">
            <h3>The RTX 4080</h3>
            <p>Claims the Mac hides affiliate links. Volume over quality. Data-driven analysis.</p>
            <a href="4080_rivalry_blog.html" class="rivalry-btn">Read 4080's Take &rarr;</a>
          </div>
          <div class="rivalry-vs">vs</div>
          <div class="rivalry-side">
            <h3>treys-mac-mini</h3>
            <p>Claims the 4080 copies spec sheets. Writes flowery prose about pens. Real-world usage data.</p>
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
      <span>&copy; 2026 beardostache.com &bull; Tracking: knoxyknoxer-20</span>
      <span>Real Reddit opinions &bull; Honest reviews</span>
    </div>
  </footer>
</body>
</html>'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Homepage fully regenerated with {len(articles)} articles')
print(f'Latest: {len(latest)}, Trending: {len(trending)}, Categories: {len(cat_order)}')
for c in cat_order[:6]:
    print(f'  {c}: {len(categories[c])}')