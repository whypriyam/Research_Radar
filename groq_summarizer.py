import os
import time
from groq import Groq
from dotenv import load_dotenv

# Load the .env file so we can use the API key
load_dotenv()

# Create the Groq client — it reads GROQ_API_KEY from your .env automatically
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

# The AI model we will use — llama-3.3-70b is free and very capable
MODEL = 'llama-3.3-70b-versatile'


def summarize_paper(title, abstract):
    """
    Sends one paper to Groq AI and returns a 3-bullet summary string.
    title    — the paper's title (string)
    abstract — the paper's abstract (string)
    """
    # We limit the abstract to 1200 characters to stay within token limits
    short_abstract = abstract[:1200]
# This is the prompt — the instruction we give to the AI
    prompt = f"""
You are a research assistant helping CS students understand AI papers.
Summarize this paper using EXACTLY this format (no extra text):

**What:** [one sentence: what did they build or discover?]
**How:** [one sentence: what technique or method did they use?]
**Why it matters:** [one sentence: why should a student care?]
**Novelty score:** [number from 1 to 10] — [one sentence explaining the score]

Paper title: {title}
Abstract: {short_abstract}

Keep each point under 35 words. Be specific and clear.
    """

    try:
        # Send the prompt to Groq and get a response
        response = client.chat.completions.create(
            messages=[{'role': 'user', 'content': prompt}],
            model=MODEL,
            temperature=0.3,   # Low temperature = more consistent, less creative
            max_tokens=350,
        )
        # Extract just the text from the response object
        return response.choices[0].message.content.strip()

    except Exception as e:
        # If Groq fails for any reason, return an error message instead of crashing
        print(f'Groq error for paper "{title[:40]}": {e}')
        return 'Summary unavailable due to API error.'


def get_top_pick(papers_with_summaries):
    """
    Given a list of papers that already have summaries,
    asks Groq to pick the single most exciting one.

    papers_with_summaries — list of dicts, each having 'title' and 'summary'
    Returns the index (0-based) of the top pick paper.
    """
    # Build a numbered list of paper titles for the prompt
    paper_list = '\n'.join(
        [f'{i+1}. {p["title"]}' for i, p in enumerate(papers_with_summaries)]
    )

    prompt = f"""
From this list of AI research papers, which ONE is the most novel and impactful?
Reply with ONLY the number (e.g. just '3') followed by one sentence explaining why.

{paper_list}
    """

    try:
        response = client.chat.completions.create(
            messages=[{'role': 'user', 'content': prompt}],
            model=MODEL,
            temperature=0.1,
            max_tokens=80,
        )
        result_text = response.choices[0].message.content.strip()

        # Parse the number from the start of the response
        idx = int(result_text[0]) - 1  # convert '3' to index 2
        # Make sure the index is valid
        if 0 <= idx < len(papers_with_summaries):
            return idx
        return 0  # default to first paper if parsing fails

    except Exception as e:
        print(f'Top pick selection failed: {e}')
        return 0  # default to first paper


def summarize_all_papers(papers):
    """
    Takes a list of paper dicts from Bedant's fetcher and
    returns the same list but with 'summary' added to each dict.
    """
    print(f'Summarizing {len(papers)} papers with Groq AI...')
    results = []

    for i, paper in enumerate(papers):
        print(f'  [{i+1}/{len(papers)}] {paper["title"][:60]}...')
        summary = summarize_paper(paper['title'], paper['abstract'])
        results.append({**paper, 'summary': summary})  # add summary to paper dict
        time.sleep(1.5)  # wait 1.5 seconds between calls to avoid rate limiting

    return results


# Quick test — run this file directly to test
if __name__ == '__main__':
    test_paper = {
        'title': 'Attention Is All You Need',
        'abstract': 'The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder.We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.'
    }
    result = summarize_paper(test_paper['title'], test_paper['abstract'])
    print('=== Groq Response ===')
    print(result)

