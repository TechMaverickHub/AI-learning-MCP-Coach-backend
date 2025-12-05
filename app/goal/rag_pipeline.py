# rag_pipeline.py
from .rag_store import search_documents
from app.rss.rss_utils import fetch_rss_entries
from .llm_utils import generate_plan
from ..rss.models import RSSFeed

RSS_FEEDS = [
    "https://www.404media.co/rss/",
]

def generate_learning_suggestions(goal_text: str, days: int):
    # 1. RAG search
    rag_docs = search_documents(goal_text)

    print("RAG DOCS------------------")
    print(rag_docs)

    rss_list = RSSFeed.objects.filter(is_active=True).values_list('url', flat=True)
    print("RSS LIST==============================")
    print(rss_list)
    # 2. RSS fetch
    rss_docs = fetch_rss_entries(rss_list)
    print("RSS FEED==============================")
    print(rss_docs)

    # 3. Build context
    context = "\n\n".join(rag_docs + rss_docs)

    # 4. Build prompt
    prompt = f"""
You are an AI learning coach.

User's Goal:
{goal_text}

Timeline:
{days} days

Context from existing knowledge:
{context}

Create a detailed, step-by-step study plan the user can follow.
"""
    # 5. Generate plan
    return generate_plan(prompt)
