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

# Build latest section (12 newest)
latest = articles[:12]
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

# Build trending section (8 random)
random.seed(42)
trending = random.sample(articles[6:], min(8, len(articles)-6))
trending_html = ''
for a in trending:
    trending_html += f'''    <article class="article-card">
        <div class="card-meta">
          <span class="badge" style="background-color:#cbd5e1; color:#475569;">15 min read</span>
        </div>
        <h3 class="card-title"><a href="articles/{a['file']}" class="article-link">{esc(a['title'])}</a></h3>
        <div class="card-footer"><a href="articles/{a['file']}" class="read-more">Read &rarr;</a></div>
      </article>'''

# Build category sections
categories = {}
for a in articles:
    cat = a['cat']
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(a)

cat_order = sorted(categories.keys(), key=lambda c: len(categories[c]), reverse=True)

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

# Read current index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace latest section
latest_pattern = r'<section class="section-header" id="latest">.*?</div>\s*\n'
latest_replacement = f'''    <section class="section-header" id="latest">
      <h2 class="section-title">Latest Reviews</h2>
      <a href="#" class="view-all">View all {len(articles)} &rarr;</a>
    </section>
    <div class="grid-3">{latest_html}</div>'''
html = re.sub(latest_pattern, latest_replacement, html, flags=re.DOTALL)

# Replace trending section
trending_pattern = r'<section id="trending".*?</div>\s*\n'
trending_replacement = f'''    <section id="trending" class="section-header">
      <h2 class="section-title"><span class="cat-badge">Trending</span>Most Discussed</h2>
      <a href="#" class="view-all">View all &rarr;</a>
    </section>
    <div class="grid-4">{trending_html}</div>'''
html = re.sub(trending_pattern, trending_replacement, html, flags=re.DOTALL)

# Replace category sections - find category section start and replace until rivalry section
cat_start = html.find('<section class="section-header">', html.find('Trending'))
if cat_start == -1:
    cat_start = html.find('<!-- Category grids will go here -->')
rivalry_start = html.find('<section class="rivalry-section"')

if cat_start >= 0 and rivalry_start > cat_start:
    html = html[:cat_start] + category_html + '\n' + html[rivalry_start:]
else:
    print("WARNING: Could not find category section boundaries, appending at end of main")
    # Insert before </main>
    main_end = html.rfind('</main>')
    if main_end >= 0:
        html = html[:main_end] + category_html + '\n' + html[main_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Homepage regenerated with {len(articles)} articles')
print(f'Latest: {len(latest)}, Trending: {len(trending)}, Categories: {len(cat_order)}')
for c in cat_order[:6]:
    print(f'  {c}: {len(categories[c])}')