import requests
import pandas as pd
import re
import sqlite3

HN_SEARCH_URL = "https://hn.algolia.com/api/v1/search"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Function to extract emails from text using regex
def extract_emails(text):
    if not text:
        return []
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    return re.findall(pattern, text)

def fetch_comments(item_id):
    """Recursively fetch comments for a post and extract all text."""
    res = requests.get(HN_ITEM_URL.format(item_id)).json()
    texts = []
    if res and "kids" in res:
        for kid in res["kids"]:
            comment = requests.get(HN_ITEM_URL.format(kid)).json()
            if comment and "text" in comment:
                texts.append(comment["text"])
                # recursive fetch for nested replies
                if "kids" in comment:
                    texts.extend(fetch_comments(comment["id"]))
    return texts

def scrape_hn_posts(batch="Summer 2024"):
    query = "YC Summer 2024"
    url = f"{HN_SEARCH_URL}?query={query}&tags=story"
    res = requests.get(url).json()

    posts = []
    for hit in res["hits"]:
        post_id = hit["objectID"]
        hn_link = f"https://news.ycombinator.com/item?id={post_id}"

        # Fetch comments
        print(f"Fetching comments for: {hit['title']}")
        comments = fetch_comments(post_id)
        all_text = " ".join(comments)
        emails = list(set(extract_emails(all_text)))

        posts.append({
            "title": hit.get("title"),
            "url": hit.get("url"),
            "author": hit.get("author"),
            "hn_link": hn_link,
            "emails": ", ".join(emails)
        })

    df = pd.DataFrame(posts)
    return df

if __name__ == "__main__":
    batch = "Summer 2024"
    df = scrape_hn_posts(batch)
    print(f"Scraped {len(df)} HN posts for {batch}")
    print(df.head())

    if not df.empty:
        df.to_csv("hn_posts.csv", index=False)
        conn = sqlite3.connect("yc_agent.db")
        df.to_sql("hn_posts", conn, if_exists="replace", index=False)
        conn.close()
        print("HN posts with emails saved to yc_agent.db (table: hn_posts)")
    else:
        print("No HN posts found – nothing to save.")

