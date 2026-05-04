import requests
import xml.etree.ElementTree as ET

NEWS_URL = 'https://news.google.com/rss/search?q=generative+AI+large+language+model&hl=en-US&gl=US&ceid=US:en'

def fetch_news():
    headers = {'User-Agent': 'ResearchRadar-Bot/1.0'}
    response = requests.get(NEWS_URL, headers=headers, timeout=30)
    if response.status_code != 200: return []
    
    root = ET.fromstring(response.content)
    articles = []
    for item in root.findall('.//item')[:10]:
        articles.append({
            'title': item.findtext('title', '').strip(),
            'link': item.findtext('link', '').strip(),
            'published': item.findtext('pubDate', '').strip()
        })
    return articles

if __name__ == '__main__':
    articles = fetch_news()
    for a in articles[:3]:
        print(f"Headline: {a['title'][:80]}")