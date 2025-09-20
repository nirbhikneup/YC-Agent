import pandas as pd
import sqlite3
from rapidfuzz import fuzz, process
import sys
batch = sys.argv[1] if len(sys.argv) > 1 else "Summer 2024"


DB_PATH = "yc_agent.db"

def load_tables():
    conn = sqlite3.connect(DB_PATH)
    yc = pd.read_sql("SELECT name, link FROM yc_companies", conn)
    hn = pd.read_sql("SELECT title, hn_link, emails FROM hn_posts", conn)
    conn.close()
    return yc, hn

def match_companies(yc, hn, threshold=60):
    contacts = []
    for _, row in yc.iterrows():
        company_name = row["name"].split()[0]  # take first word as base
        matches = process.extract(
            company_name, hn["title"], scorer=fuzz.partial_ratio, limit=1
        )
        if matches and matches[0][1] >= threshold:
            matched_title = matches[0][0]
            hn_row = hn[hn["title"] == matched_title].iloc[0]
            contacts.append({
                "company_name": row["name"],
                "yc_link": row["link"],
                "hn_link": hn_row["hn_link"],
                "emails": hn_row["emails"]
            })
    return pd.DataFrame(contacts)

if __name__ == "__main__":
    yc, hn = load_tables()
    df = match_companies(yc, hn, threshold=60)
    print(f"Found {len(df)} matches")
    print(df.head())
    df.to_csv("contacts.csv", index=False)
    conn = sqlite3.connect("yc_agent.db")
    df.to_sql("contacts", conn, if_exists="replace", index=False)
    conn.close()

    print("Saved contacts.csv")
