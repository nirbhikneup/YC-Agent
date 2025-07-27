# YC-Agent
I built a YC agent that is an automated system to find YC companies info. Specifically, targeting the founders and their email, so we can make job application process smoother and easier.

# YC Agent – Automated YC Startup Lead Generator

YC Agent is a pipeline that automatically scrapes recent **Y Combinator batches**, finds related **Hacker News posts**, extracts founder emails from comments, and links the two together.  
It outputs a **contacts.csv** file you can use for outreach or research.

---

## Features

- **Scrape YC companies**  
  Uses Playwright to load `ycombinator.com/companies` for a given batch and extract all startup names and links.

- **Scrape Hacker News posts**  
  Uses the Algolia HN API + Firebase API to:
  - Find “Launch HN / Show HN” posts
  - Recursively collect comments
  - Extract emails using regex

- **Match YC companies to HN posts**  
  - Fuzzy string matching with RapidFuzz
  - Links company names to HN posts and emails

- **One-command automation**  
  - `run_pipeline.py` runs the entire workflow and updates:
    - `yc_agent.db` (SQLite database)
    - `contacts.csv`

---

## Tech Stack

- **Python 3.10+**
- Playwright (browser automation)
- BeautifulSoup (HTML parsing)
- Requests (API calls)
- Pandas (data processing)
- RapidFuzz (fuzzy matching)
- SQLite (local storage)

---

## Installation

Clone the repo:

```bash
git clone https://github.com/YOUR_USERNAME/YC-Agent.git
cd YC-Agent

