import json
import requests
import os
from datetime import datetime

# Configuration
POSTS_FILE = 'data/posts.json'
API_URL = "https://www.binance.com/bapi/composite/v4/friendly/pgc/feed/news/list?strategy=10"
HEADERS = {
    "lang": "vi",
    "clienttype": "web"
}

def fetch_latest_news():
    print(f"Fetching news from {API_URL}...")
    try:
        response = requests.get(API_URL, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        if data['code'] == "000000":
            return data['data']['vos'][:3] # Get the 3 latest
        else:
            print(f"Error from API: {data['message']}")
            return []
    except Exception as e:
        print(f"Failed to fetch news: {e}")
        return []

def format_article(vo):
    # Try to get translated data if available
    translated = vo.get('translatedData', {})
    title = translated.get('title') or vo.get('title')
    description = translated.get('subTitle') or vo.get('subTitle')
    
    # ID/Slug from title
    slug = title.lower().replace(' ', '-').replace('/', '-').replace(':', '')
    # Clean up non-alphanumeric chars for the ID
    import re
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    
    # Category based on source or content tags
    category = "TIN TỨC THỊ TRƯỜNG"
    
    # Image
    image = vo.get('coverMeta', {}).get('url') or "https://images.unsplash.com/photo-1621761191319-c6fb62004040?auto=format&fit=crop&q=80&w=800"
    
    # Date
    publish_time = vo.get('date', 0)
    if publish_time:
        date_str = datetime.fromtimestamp(publish_time).strftime('%d/%m/%Y')
    else:
        date_str = datetime.now().strftime('%d/%m/%Y')
        
    # Content (formatted with some basic HTML)
    content = f"{description} <br><br> <h2>Nội Dung Tóm Lược</h2> {description} <br><br> Bạn có thể xem chi tiết bài đăng gốc tại Binance Square để nắm bắt thêm thông tin chuyên sâu. #SHINTRADING"
    
    return {
        "id": slug,
        "category": category,
        "title": title,
        "description": description,
        "image": image,
        "date": date_str,
        "content": content,
        "original_id": vo.get('id') # To prevent duplicates
    }

def update_posts():
    news_items = fetch_latest_news()
    if not news_items:
        print("No new news found.")
        return

    # Load existing posts
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, 'r', encoding='utf-8') as f:
            posts = json.load(f)
    else:
        posts = []

    # Get set of existing titles to avoid duplicates (titles are a good unique enough key)
    existing_titles = {p['title'] for p in posts}
    
    new_posts_added = 0
    for item in news_items:
        formatted = format_article(item)
        if formatted['title'] not in existing_titles:
            posts.insert(0, formatted)
            new_posts_added += 1
            print(f"Added: {formatted['title']}")
        else:
            print(f"Skipped (already exists): {formatted['title']}")

    if new_posts_added > 0:
        # Basic validation: ensure posts is a list and has content
        if isinstance(posts, list) and len(posts) > 0:
            # Save back to file
            with open(POSTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(posts, f, ensure_ascii=False, indent=4)
            print(f"Successfully updated {POSTS_FILE} with {new_posts_added} new posts.")
        else:
            print("Error: posts data is invalid or empty, skipping write.")
    else:
        print("No new unique posts found.")

if __name__ == "__main__":
    update_posts()
