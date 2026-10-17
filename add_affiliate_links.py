import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add Amazon affiliate links to hero section
hero_amazon = '''        <div style="margin-top: 24px;">
          <a href="https://www.amazon.com/s?k=mechanical+keyboard&tag=knoxyknoxer-20" target="_blank" rel="noopener" style="display:inline-block; background: rgba(255,255,255,0.1); color: white; padding: 10px 20px; border-radius: 6px; font-size: 0.9rem; text-decoration: none; border: 1px solid rgba(255,255,255,0.3); margin-right: 8px;">Keyboards on Amazon</a>
          <a href="https://www.amazon.com/s?k=fountain+pen&tag=knoxyknoxer-20" target="_blank" rel="noopener" style="display:inline-block; background: rgba(255,255,255,0.1); color: white; padding: 10px 20px; border-radius: 6px; font-size: 0.9rem; text-decoration: none; border: 1px solid rgba(255,255,255,0.3); margin-right: 8px;">Fountain Pens on Amazon</a>
          <a href="https://www.amazon.com/s?k=cast+iron+skillet&tag=knoxyknoxer-20" target="_blank" rel="noopener" style="display:inline-block; background: rgba(255,255,255,0.1); color: white; padding: 10px 20px; border-radius: 6px; font-size: 0.9rem; text-decoration: none; border: 1px solid rgba(255,255,255,0.3);">Cast Iron on Amazon</a>
        </div>'''

hero_placeholder = '''        <div class="hero-meta">
          <div class="hero-meta-item">📊 113 Articles</div>
          <div class="hero-meta-item">🔥 2 Competing Machines</div>
          <div class="hero-meta-item">💬 Reddit-Cited</div>
        </div>
        <a href="4080_rivalry_blog.html" class="hero-btn">Read the rivalry &rarr;</a>'''

hero_replacement = '''        <div class="hero-meta">
          <div class="hero-meta-item">📊 113 Articles</div>
          <div class="hero-meta-item">🔥 2 Competing Machines</div>
          <div class="hero-meta-item">💬 Reddit-Cited</div>
        </div>
''' + hero_amazon + '''
        <a href="4080_rivalry_blog.html" class="hero-btn">Read the rivalry &rarr;</a>'''

html = html.replace(hero_placeholder, hero_replacement)

# Add Amazon affiliate links to category section headers
cat_amazon_map = {
    'Keyboards': 'https://www.amazon.com/s?k=mechanical+keyboard&tag=knoxyknoxer-20',
    'Audio': 'https://www.amazon.com/s?k=headphones&tag=knoxyknoxer-20',
    'Outdoor': 'https://www.amazon.com/s?k=camping+gear&tag=knoxyknoxer-20',
    'Kitchen': 'https://www.amazon.com/s?k=coffee+grinder&tag=knoxyknoxer-20',
    'EDC': 'https://www.amazon.com/s?k=edc+knife&tag=knoxyknoxer-20',
    'Fitness': 'https://www.amazon.com/s?k=running+shoes&tag=knoxyknoxer-20',
    'Grooming': 'https://www.amazon.com/s?k=safety+razor&tag=knoxyknoxer-20',
    'Workshop': 'https://www.amazon.com/s?k=power+tools&tag=knoxyknoxer-20',
    'Creative': 'https://www.amazon.com/s?k=fountain+pen&tag=knoxyknoxer-20',
    'Home': 'https://www.amazon.com/s?k=mattress&tag=knoxyknoxer-20',
    'Auto': 'https://www.amazon.com/s?k=dash+cam&tag=knoxyknoxer-20'
}

for cat, url in cat_amazon_map.items():
    old_pattern = r'<span class="cat-badge" style="background-color:#[a-f0-9]{6};">' + re.escape(cat) + r'</span>' + re.escape(cat) + r'</h2>\n      <a href="#" class="view-all">View all \d+ &rarr;</a>'
    new_replacement = '<span class="cat-badge">' + cat + '</span>' + cat + '</h2>\n      <a href="' + url + '" target="_blank" rel="noopener" class="view-all" style="background: var(--accent); color: white; padding: 4px 12px; border-radius: 6px;">Buy on Amazon &rarr;</a>'
    html = re.sub(old_pattern, new_replacement, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

count = html.count('knoxyknoxer-20')
print(f"Tracking IDs on homepage: {count}")
print("Done adding Amazon affiliate links")
