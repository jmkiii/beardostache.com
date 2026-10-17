import os, re, datetime, random, json

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

    if 'By the RTX 4080' in content:
        author = '4080'
        author_color = '#1a73e8'
    elif 'By treys-mac-mini' in content:
        author = 'Mac'
        author_color = '#64748b'
    else:
        author = random.choice(['4080', 'Mac'])
        author_color = '#1a73e8' if author == '4080' else '#64748b'

    title_lower = title.lower()
    content_lower = content.lower()

    category = 'Gear'
    cat_color = '#64748b'

    if any(k in title_lower or k in content_lower for k in ['keyboard', 'keychron', 'mechanical', 'switch', 'keycap']):
        category = 'Keyboards'
        cat_color = '#1a73e8'
    elif any(k in title_lower or k in content_lower for k in ['headphone', 'headphones', 'iem', 'dac', 'amp', 'sennheiser', 'audeze', 'audio', 'ath-m50x', 'audeze lcd-x']):
        category = 'Audio'
        cat_color = '#7c3aed'
    elif any(k in title_lower or k in content_lower for k in ['backpack', 'tent', 'camping', 'hiking', 'sleeping', 'stove', 'headlamp', 'water filter', 'nemo', 'icebreaker', 'goruck', 'aer flight', 'minaal', 'ugq bandit', 'outdoor research', 'black diamond']):
        category = 'Outdoor'
        cat_color = '#059669'
    elif any(k in title_lower or k in content_lower for k in ['knife', 'cast iron', 'skillet', 'dutch oven', 'coffee grinder', 'espresso', 'kitchen', 'chef', 'pan', 'chemex', 'shun', 'le creuset', 'staub', 'lodge', 'finex', 'tramontina', 'wusthof', 'brew', 'coffee']):
        category = 'Kitchen'
        cat_color = '#b45309'
    elif any(k in title_lower or k in content_lower for k in ['folding knife', 'fixed blade', 'multitool', 'flashlight', 'edc', 'wallet', 'pen', 'tenacious', 'leatherman', 'spyderco', 'kershaw', 'benchmade', 'nitecore', 'olight', 'casio g-shock', 'orient kamasu', 'garmin fenix', 'streamlight']):
        category = 'EDC'
        cat_color = '#dc2626'
    elif any(k in title_lower or k in content_lower for k in ['kettlebell', 'dumbbell', 'running', 'yoga', 'massage', 'fitness', 'rogue', 'theragun', 'whoop', 'kettle', 'hoka', 'brooks', 'new balance', 'theragun']):
        category = 'Fitness'
        cat_color = '#be185d'
    elif any(k in title_lower or k in content_lower for k in ['razor', 'shaver', 'beard', 'skincare', 'sunscreen', 'grooming', 'merkur', 'electric shaver', 'biore', 'neutrogena', 'declaration']):
        category = 'Grooming'
        cat_color = '#0891b2'
    elif any(k in title_lower or k in content_lower for k in ['drill', 'saw', 'vacuum', 'compressor', 'tool chest', 'workshop', 'circular saw', 'shop vac', 'tool', 'milwaukee', 'bosch universal', 'avid power']):
        category = 'Workshop'
        cat_color = '#4f46e5'
    elif any(k in title_lower or k in content_lower for k in ['3d printer', 'fountain pen', 'notebook', 'camera', 'lens', 'film', 'tripod', 'turntable', 'creative', 'ink', 'paper', 'manfrotto', 'rega', 'cinestill', 'creality', 'anycubic', 'tomoe river', 'pilot custom heritage', 'pilot precise v5', 'lamy safari', 'parker jotter', 'uni-ball', 'twsbi eco', 'platinum preppy', 'tomoe river', 'sony 24-70', 'canon r6 ii', 'fujifilm x-t5']):
        category = 'Creative'
        cat_color = '#db2777'
    elif any(k in title_lower or k in content_lower for k in ['mattress', 'pillow', 'sheet', 'towel', 'vacuum', 'air purifier', 'robot vacuum', 'home', 'tempur-cloud', 'purple hybrid', 'brooklinen', 'coway', 'bissell', 'herman miller', 'uplift']):
        category = 'Home'
        cat_color = '#0f172a'
    elif any(k in title_lower or k in content_lower for k in ['dash cam', 'jump starter', 'tire inflator', 'auto', 'car']):
        category = 'Auto'
        cat_color = '#020617'

    word_count = len(content.split())
    read_time = max(1, round(word_count / 200))
    dt = datetime.datetime.fromtimestamp(mtime)

    articles.append({
        'file': f,
        'title': title,
        'mtime': mtime,
        'dt': dt,
        'author': author,
        'author_color': author_color,
        'category': category,
        'cat_color': cat_color,
        'read_time': read_time,
        'tracking': content.count('knoxyknoxer-20')
    })

articles.sort(key=lambda x: x['mtime'], reverse=True)

def fmt_date(dt):
    return dt.strftime('%b %d')

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

latest = articles[:6]
latest_html = ''
for a in latest:
    latest_html += f'''
    <article class="article-card">
      <div class="card-meta">
        <span class="badge cat" style="background-color:{a["cat_color"]};">{a["category"]}</span>
        <span class="badge author" style="background-color:{a["author_color"]};">{a["author"]}</span>
        <span class="badge" style="background-color:#cbd5e1; color:#475569;">{a["read_time"]} min read</span>
      </div>
      <h3 class="card-title"><a href="articles/{a["file"]}">{esc(a["title"])}</a></h3>
      <p class="card-excerpt">Newest review from the {a["category"].lower()} category.</p>
      <div class="card-footer">
        <span class="card-date">{fmt_date(a["dt"])}</span>
        <a href="articles/{a["file"]}" class="read-more">Read review &rarr;</a>
      </div>
    </article>'''

import random
random.seed(42)
trending = random.sample(articles[6:], min(8, len(articles)-6))
trending_html = ''
for a in trending:
    trending_html += f'''
    <article class="article-card">
      <div class="card-meta">
        <span class="badge cat" style="background-color:{a["cat_color"]};">{a["category"]}</span>
        <span class="badge author" style="background-color:{a["author_color"]};">{a["author"]}</span>
      </div>
      <h3 class="card-title"><a href="articles/{a["file"]}">{esc(a["title"])}</a></h3>
      <p class="card-excerpt">Community favorite with {a["tracking"]} affiliate links.</p>
      <div class="card-footer">
        <span class="card-date">{fmt_date(a["dt"])}</span>
        <a href="articles/{a["file"]}" class="read-more">Read &rarr;</a>
      </div>
    </article>'''

categories = {}
for a in articles:
    cat = a['category']
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(a)

cat_order = sorted(categories.keys(), key=lambda c: len(categories[c]), reverse=True)

category_sections_html = ''
for cat in cat_order[:6]:
    cat_articles = categories[cat][:4]
    cat_color = cat_articles[0]['cat_color']
    cat_html = ''
    for a in cat_articles:
        cat_html += f'''
        <article class="article-card">
          <div class="card-meta">
            <span class="badge author" style="background-color:{a["author_color"]};">{a["author"]}</span>
            <span class="badge" style="background-color:#cbd5e1; color:#475569;">{a["read_time"]} min</span>
          </div>
          <h3 class="card-title"><a href="articles/{a["file"]}">{esc(a["title"])}</a></h3>
          <div class="card-footer">
            <span class="card-date">{fmt_date(a["dt"])}</span>
            <a href="articles/{a["file"]}" class="read-more">Read &rarr;</a>
          </div>
        </article>'''
    category_sections_html += f'''
    <section class="section-header">
      <h2 class="section-title"><span class="cat-badge" style="background-color:{cat_color};">{cat}</span>{cat}</h2>
      <a href="#" class="view-all">View all {len(categories[cat])} &rarr;</a>
    </section>
    <div class="grid-4">{cat_html}</div>'''

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

latest_placeholder = '''    <section class="section-header">
      <h2 class="section-title">Latest Reviews</h2>
      <a href="#latest" class="view-all">View all &rarr;</a>
    </section>
    <div class="grid-3">
      <!-- Latest 6 articles will go here -->
    </div>'''

latest_replacement = f'''    <section class="section-header" id="latest">
      <h2 class="section-title">Latest Reviews</h2>
      <a href="#" class="view-all">View all {len(articles)} &rarr;</a>
    </section>
    <div class="grid-3">{latest_html}</div>'''

html = html.replace(latest_placeholder, latest_replacement)

trending_placeholder = '''    <section id="trending" class="section-header">
      <h2 class="section-title"><span class="cat-badge">Trending</span>Most Discussed</h2>
      <a href="#" class="view-all">View all &rarr;</a>
    </section>
    <div class="grid-4">
      <!-- Trending articles will go here -->
    </div>'''

trending_replacement = f'''    <section id="trending" class="section-header">
      <h2 class="section-title"><span class="cat-badge">Trending</span>Most Discussed</h2>
      <a href="#" class="view-all">View all &rarr;</a>
    </section>
    <div class="grid-4">{trending_html}</div>'''

html = html.replace(trending_placeholder, trending_replacement)

cat_placeholder = '''    <!-- Category grids will go here -->'''
html = html.replace(cat_placeholder, category_sections_html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Homepage populated with:")
print(f"  - {len(latest)} latest articles")
print(f"  - {len(trending)} trending articles")
print(f"  - {len(cat_order)} category sections")
for cat in cat_order[:6]:
    print(f"    - {cat}: {len(categories[cat])} articles")
