import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import sys
import re


async def scrape_yc(batch):
    url = "https://www.ycombinator.com/companies"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=250)
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
                companies.append(
                    {
                        "name": name,
                        "link": "https://www.ycombinator.com" + href,
                        "batch": batch,
                    }
                )

    # Deduplicate
    seen = set()
    unique_companies = []
    for c in companies:
        if c["link"] not in seen:
            seen.add(c["link"])
            unique_companies.append(c)

    return pd.DataFrame(unique_companies)


async def scrape_company_emails(company_url, browser):
    """Scrape emails from a company's YC page"""
    try:
        page = await browser.new_page()
        await page.goto(company_url, timeout=30000)
        await asyncio.sleep(2)

        content = await page.content()
        await page.close()

        soup = BeautifulSoup(content, "html.parser")

        # Look for email patterns in the page content
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        emails = re.findall(email_pattern, content)

        # Also look for contact links and other email indicators
        contact_links = soup.find_all("a", href=lambda x: x and "mailto:" in x)
        for link in contact_links:
            email = link["href"].replace("mailto:", "")
            if email not in emails:
                emails.append(email)

        return list(set(emails))  # Remove duplicates
    except Exception as e:
        print(f"Error scraping emails from {company_url}: {e}")
        return []


async def scrape_yc_with_emails(batch):
    """Main function to scrape YC companies and their emails"""
    print(f"Starting YC scraper for batch: {batch}")

    # First, get the list of companies
    companies_df = await scrape_yc(batch)
    print(f"Found {len(companies_df)} companies")

    if len(companies_df) == 0:
        print("No companies found. Exiting.")
        return pd.DataFrame()

    # Now scrape emails for each company
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=100)

        companies_with_emails = []
        for idx, row in companies_df.iterrows():
            print(f"Scraping emails for {row['name']} ({idx + 1}/{len(companies_df)})")
            emails = await scrape_company_emails(row["link"], browser)

            company_data = {
                "name": row["name"],
                "link": row["link"],
                "batch": row["batch"],
                "emails": ", ".join(emails) if emails else "",
                "email_count": len(emails),
            }
            companies_with_emails.append(company_data)

            # Small delay to be respectful
            await asyncio.sleep(1)

        await browser.close()

    return pd.DataFrame(companies_with_emails)


def get_year_input():
    """Get year input from user"""
    while True:
        try:
            year = input("Enter the year for YC batch (e.g., 2024, 2023): ").strip()
            if not year:
                print("Please enter a valid year.")
                continue

            # Convert to batch format
            if year.isdigit():
                batch = f"Summer {year}"
                return batch
            else:
                print("Please enter a valid year (e.g., 2024).")
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)


if __name__ == "__main__":
    # Get batch from command line argument or prompt user
    if len(sys.argv) > 1:
        batch = sys.argv[1]
    else:
        batch = get_year_input()

    print(f"Scraping YC companies for batch: {batch}")

    # Run the scraper
    df = asyncio.run(scrape_yc_with_emails(batch))

    if len(df) > 0:
        print(f"\nScraped {len(df)} companies with emails")
        print(f"Companies with emails: {len(df[df['email_count'] > 0])}")
        print("\nSample results:")
        print(df[["name", "email_count", "emails"]].head())

        # Save to CSV
        filename = f"yc_companies_{batch.replace(' ', '_')}.csv"
        df.to_csv(filename, index=False)
        print(f"\nSaved to {filename}")

        # Save to SQLite
        engine = create_engine("sqlite:///yc_agent.db")
        df.to_sql("yc_companies", engine, if_exists="replace", index=False)
        print("Saved to yc_agent.db (table: yc_companies)")
    else:
        print("No data to save.")
