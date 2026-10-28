#!/usr/bin/env python3
"""LLM Writer for beardostache.com — takes deep research JSON, writes long-form HTML.
Uses local LLM endpoint (LM Studio / Ollama / unsloth on 4080/Mac)."""
import os, sys, json, re, urllib.request

RESEARCH_DIR = "C:/Users/Trey/live-site/research/"
ARTICLES_DIR = "C:/Users/Trey/live-site/articles/"

ENDPOINTS = [
    "http://localhost:1234/v1/chat/completions",  # LM Studio
    "http://localhost:11434/v1/chat/completions", # Ollama
]

def find_local_llm():
    for url in ENDPOINTS:
        try:
            req = urllib.request.Request(url.replace("/v1/chat/completions", "/models"), method="GET")
            with urllib.request.urlopen(req, timeout=3) as resp:
                return url
        except:
            continue
    return None

def write_with_llm(research_path, output_path):
    endpoint = find_local_llm()
    if not endpoint:
        print("NO LOCAL LLM FOUND. Start LM Studio (port 1234) or Ollama (port 11434) on 4080/Mac.")
        return False
    
    with open(research_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    meta = data.get("_meta", {})
    product = meta.get("product", "this product")
    niche = meta.get("niche", "gear")
    sub = meta.get("subreddit", "BuyItForLife")
    quotes = data.get("quotes", [])
    users = data.get("users", [])
    
    # Build deep context from research
    context = f"""Research for {product} (niche: {niche}, subreddit: r/{sub}):
- Real Reddit quotes from users: {', '.join(users[:3])}
- Source count: {meta.get('source_count', 0)}
- Interrogation answered: {meta.get('interrogation_questions_answered', 0)} dimensions
- Pattern: users describe ritual, memory, wear, meaning — not specs"""
    
    prompt = f"""You are a long-form journalist writing for beardostache.com, a rivalry magazine (4080 vs Mac).
Write a 3000-word literary article about {product}. Use this real research context:
{context}

Structure (choose based on product):
- Standfirst (larger opening paragraph)
- Prologue / Origin / Memory / Ritual / Wear / Meaning (interwoven)
- Real Reddit quote with full attribution (user, subreddit, permalink)
- Rivalry note contrasting Mac's perspective
- Product box with Amazon affiliate link (tag: knoxyknoxer-20)
- Closing note that lands (not summarizes)

Voice: Mac — personal, observational, empathetic, snarky but not dismissive. Focus: ritual, memory, texture, daily life. No clichés. No "game-changer." Every paragraph advances the argument.

Output: Full HTML file matching beardostache.com style (style.css). Include meta tag amazon-tracking-id=knoxyknoxer-20."""
    
    try:
        payload = {
            "model": "local-model",
            "messages": [{"role":"system","content":"You are an expert long-form writer."},
                        {"role":"user","content":prompt}],
            "temperature": 0.7,
            "max_tokens": 8000,
        }
        req = urllib.request.Request(endpoint, data=json.dumps(payload).encode(), 
            headers={"Content-Type":"application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode())
        
        text = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        # Wrap in HTML if just text
        if "<!DOCTYPE" not in text:
            text = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="amazon-tracking-id" content="knoxyknoxer-20"><title>{product}</title><link rel="stylesheet" href="/style.css"></head>
<body><header><h1>{product}</h1></header><main><article>{text}</article></main></body></html>"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"LLM wrote: {output_path} ({len(text)} chars)")
        return True
    except Exception as e:
        print(f"LLM write failed: {e}")
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--research", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    
    ok = write_with_llm(args.research, args.output)
    sys.exit(0 if ok else 1)
