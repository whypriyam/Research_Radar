"""
main.py — ResearchRadar Master Pipeline
Run this file to execute the full weekly digest generation.
"""
import os
from dotenv import load_dotenv

# Load .env before anything else
load_dotenv()

# Import Bedant's data fetchers
from test_arxiv  import fetch_arxiv_papers
from test_github import fetch_github_repos
from test_news   import fetch_news

# Import your (Sarthak's) AI modules
from groq_summarizer import summarize_all_papers, get_top_pick
from memory          import filter_new_papers, update_memory

# Import Samarth's delivery modules
from digest_builder  import build_digest
from telegram_sender import send_telegram
from email_sender    import send_email


def run_weekly_digest():
    print('=' * 50)
    print('🦞 ResearchRadar — Weekly Digest Starting')
    print('=' * 50)

    # ── STEP 1: Fetch raw data from all 3 sources ──────
    print('\n📡 STEP 1: Fetching data...')
    arxiv_papers = fetch_arxiv_papers()
    github_repos  = fetch_github_repos()
    news_articles = fetch_news()

    # ── STEP 2: Filter out already-seen papers ──────────
    print('\n💾 STEP 2: Applying memory filter...')
    new_papers = filter_new_papers(arxiv_papers)

    if not new_papers:
        print('No new papers found this week. Skipping digest.')
        return

    # Limit to 10 papers max to keep Groq usage reasonable
    new_papers = new_papers[:10]
# ── STEP 3: Summarize with Groq AI ──────────────────
    print(f'\n🧠 STEP 3: Summarizing {len(new_papers)} papers with Groq...')
    papers_with_summaries = summarize_all_papers(new_papers)

    # ── STEP 4: Pick the top paper ──────────────────────
    print('\n⭐ STEP 4: Selecting Top Pick...')
    top_idx = get_top_pick(papers_with_summaries)
    print(f'  Top Pick: {papers_with_summaries[top_idx]["title"][:60]}')

    # ── STEP 5: Build the DOCX digest ───────────────────
    print('\n📄 STEP 5: Building DOCX digest...')
    docx_path = build_digest(papers_with_summaries, github_repos, news_articles, top_idx)
    print(f'  Saved: {docx_path}')

    # ── STEP 6: Deliver to all channels ─────────────────
    print('\n📬 STEP 6: Delivering...')
    send_telegram(docx_path)

    recipients = os.environ.get('EMAIL_RECIPIENTS', '').split(',')
    if recipients and recipients[0]:
        send_email(docx_path, recipients)

    # ── STEP 7: Update memory ────────────────────────────
    print('\n💾 STEP 7: Updating memory...')
    update_memory(papers_with_summaries)

    print('\n✅ ResearchRadar digest complete!')
    print(f'   Papers summarized: {len(papers_with_summaries)}')
    print(f'   GitHub repos:      {len(github_repos)}')
    print(f'   DOCX saved to:     {docx_path}')


if __name__ == '__main__':
    run_weekly_digest()
