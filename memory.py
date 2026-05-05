import json
import os
from datetime import datetime, timedelta

# The file where we store seen paper IDs
MEMORY_FILE = 'seen_papers.json'


def load_memory():
    """Loads the memory file. Returns a dict mapping paper_id to the date seen."""
    if not os.path.exists(MEMORY_FILE):
        return {}  # empty memory on first run
    with open(MEMORY_FILE, 'r') as f:
        return json.load(f)


def save_memory(memory_dict):
    """Saves the memory dict to the JSON file."""
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory_dict, f, indent=2)


def filter_new_papers(papers):
    """
    Given a list of papers, removes any we have already seen in the past 14 days.
    Returns only the NEW papers.
    """
    memory = load_memory()
    two_weeks_ago = (datetime.now() - timedelta(days=14)).isoformat()
    new_papers = []

    for paper in papers:
        pid = paper['paper_id']
        if pid not in memory or memory[pid] < two_weeks_ago:
            new_papers.append(paper)

    print(f'Memory filter: {len(papers)} total → {len(new_papers)} new papers')
    return new_papers


def update_memory(papers):
    """Marks all these papers as seen today."""
    memory = load_memory()
    today = datetime.now().isoformat()
    for paper in papers:
        memory[paper['paper_id']] = today
    save_memory(memory)
    print(f'Memory updated with {len(papers)} new paper IDs.')
