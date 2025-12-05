# rss_utils.py
import feedparser

def fetch_rss_entries(feed_urls, limit=5):
    items = []
    for url in feed_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries[:limit]:
            content = entry.title + " " + entry.get("summary", "")
            items.append(content)
    return items
