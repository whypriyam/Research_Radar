import requests
from datetime import datetime, timedelta

def fetch_github_repos():
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    url = 'https://api.github.com/search/repositories'
    params = {
        'q': f'topic:llm created:>{week_ago}',
        'sort': 'stars',
        'order': 'desc',
        'per_page': 10
    }
    headers = {'User-Agent': 'ResearchRadar-Bot/1.0'}
    print('Fetching GitHub trending repos...')
    response = requests.get(url, params=params, headers=headers, timeout=30)
    if response.status_code != 200:
        return []
    
    data = response.json()
    repos = []
    for repo in data.get('items', []):
        repos.append({
            'name': repo['full_name'],
            'stars': repo['stargazers_count'],
            'url': repo['html_url'],
            'description': repo.get('description', 'No description provided'),
            'language': repo.get('language', 'Unknown'),
        })
    return repos

if __name__ == '__main__':
    repos = fetch_github_repos()
    for r in repos[:3]:
        print(f"Repo: {r['name']} ({r['stars']} stars)")