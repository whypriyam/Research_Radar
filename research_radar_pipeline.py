from dotenv import load_dotenv
load_dotenv()
import os


from telegram_sender import send_telegram
from digest_builder import build_digest
from test_arxiv import fetch_arxiv_papers
from test_github import fetch_github_repos
from test_news import fetch_news
from email_sender import send_email


print("Starting ResearchRadar pipeline...\n")

# 1. Fetch data
papers_raw = fetch_arxiv_papers()
repos = fetch_github_repos()
news = fetch_news()

print(f"Fetched {len(papers_raw)} papers")
print(f"Fetched {len(repos)} repos")
print(f"Fetched {len(news)} news articles\n")


# 2. Convert ArXiv format → builder format
papers = []
for p in papers_raw:
    papers.append({
        "title": p.get("title"),
        "summary": p.get("abstract"),   # 🔥 FIX HERE
        "link": p.get("link"),
        "authors": p.get("authors")
    })


# 3. Safety fallback (avoid crash)
if not papers:
    papers = [{"title": "No data", "summary": "No papers found", "link": "", "authors": ""}]

if not repos:
    repos = [{"name": "No repos", "stars": 0, "url": "", "description": ""}]

if not news:
    news = [{"title": "No news"}]


# 4. Build DOCX
docx_file = build_digest(papers, repos, news, 0)

print("\nDOCX generated:", docx_file)
send_telegram(docx_file)
from email_sender import send_email

send_email(docx_file, ["samarth.00071@gmail.com"])
print("📧 Email sent successfully")
