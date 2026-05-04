import requests
import xml.etree.ElementTree as ET

ARXIV_URL = (
    'https://export.arxiv.org/api/query'
    '?search_query=cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL'
    '&max_results=20'
    '&sortBy=submittedDate'
    '&sortOrder=descending'
)

NS = {'atom': 'http://www.w3.org/2005/Atom'}

def fetch_arxiv_papers():
    print('Fetching ArXiv papers...')
    response = requests.get(ARXIV_URL, timeout=30)
    if response.status_code != 200:
        print(f'Error: ArXiv returned status {response.status_code}')
        return []
    
    root = ET.fromstring(response.content)
    papers = []
    for entry in root.findall('atom:entry', NS):
        raw_id = entry.find('atom:id', NS).text.strip()
        title = entry.find('atom:title', NS).text.strip().replace('\n', ' ')
        abstract = entry.find('atom:summary', NS).text.strip().replace('\n', ' ')
        link = raw_id.replace('http://arxiv.org/abs/', 'https://arxiv.org/abs/')
        paper_id = raw_id.split('/')[-1]
        author_elements = entry.findall('atom:author/atom:name', NS)
        authors = ', '.join([a.text for a in author_elements[:3]])
        
        papers.append({
            'paper_id': paper_id,
            'title': title,
            'abstract': abstract,
            'link': link,
            'authors': authors,
        })
    return papers

if __name__ == '__main__':
    papers = fetch_arxiv_papers()
    for p in papers[:3]:
        print(f"Title: {p['title'][:80]}")
        print(f"Link: {p['link']}")
        print('---')