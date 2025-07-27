import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine

async def scrape_yc(batch="Summer 2024"):
    url = "https://www.ycombinator.com/companies"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=250)
        page = await browser.new_page()
        print(f"Opening {url}...")
        await page.goto(url)

        # Wait for filter panel and click batch
        await page.wait_for_selector(f"label:has-text('{batch}')")
        await page.click(f"label:has-text('{batch}')")
        print(f"Clicked filter {batch}")

        await asyncio.sleep(5)  # wait for data to load

        # Scroll to load all companies
        for _ in range(20):
            await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            await asyncio.sleep(1.5)

        content = await page.content()
        await browser.close()


    soup = BeautifulSoup(content, "html.parser")
    companies = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # Only take links that look like /companies/some-slug
        if href.startswith("/companies/") and "founders" not in href:
            name = a.get_text(strip=True)
            if name:
                companies.append({
                    "name": name,
                    "link": "https://www.ycombinator.com" + href,
                    "batch": batch
                })


    # Deduplicate
    seen = set()
    unique_companies = []
    for c in companies:
        if c["link"] not in seen:
            seen.add(c["link"])
            unique_companies.append(c)

    return pd.DataFrame(unique_companies)



if __name__ == "__main__":
    df = asyncio.run(scrape_yc("Summer 2024"))
    print(f"Scraped {len(df)} companies")
    print(df.head())
    df.to_csv("yc_companies.csv", index=False)

    # Save to SQLite
    engine = create_engine("sqlite:///yc_agent.db")
    df.to_sql("yc_companies", engine, if_exists="replace", index=False)
    print("Saved to yc_agent.db (table: yc_companies)")
