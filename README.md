# YC Company Scraper

A powerful web scraper that extracts Y Combinator company information and email addresses for any given year/batch.

## Live Demo

- Explore the AI-enhanced dashboard: https://yc-agent-findjobs.streamlit.app/

## Features

- 🤖 **AI Insights**: Streamlit dashboard uses Meta LLaMA 3 80B on Hugging Face for contextual answers about the dataset
- 🚀 **Backend Operation**: Runs completely in headless mode without showing browser windows
- 📧 **Email Extraction**: Automatically finds and extracts email addresses from company pages
- 📊 **Data Export**: Saves results to both CSV and SQLite database
- 🎯 **Year-based Filtering**: Scrape companies from specific YC batches
- ⚡ **Fast & Efficient**: Uses Playwright for reliable web scraping

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd yc_agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
playwright install
```

## Usage

### Command Line Interface

```bash
# Interactive mode - prompts for year
python scraper/yc_scraper.py

# Direct mode - specify batch
python scraper/yc_scraper.py "Summer 2024"
```

### Web API (Coming Soon)

The scraper will be available as a web service with a simple interface to:
- Select year/batch
- Start scraping process
- Download results as CSV
- View progress in real-time

## Output

The scraper generates:
- **CSV file**: `yc_companies_Summer_2024.csv` with company details and emails
- **SQLite database**: `yc_agent.db` with table `yc_companies`

## Data Structure

Each company record includes:
- `name`: Company name
- `link`: YC company page URL
- `batch`: YC batch (e.g., "Summer 2024")
- `emails`: Comma-separated list of found emails
- `email_count`: Number of emails found

## Example Results

```
Scraped 440 companies with emails
Companies with emails: 91
```

## Deployment

This project is configured for deployment on Vercel with:
- FastAPI backend
- Automatic dependency installation
- Headless browser support

### Streamlit AI Experience

The live Streamlit deployment shares the same Hugging Face configuration used locally. Set the following environment variables when deploying:

- `HUGGINGFACE_API_TOKEN`: Required. A token with access to the Meta LLaMA 3 80B Instruct model.
- `HUGGINGFACE_MODEL_ID` (optional): Override the default `meta-llama/Meta-Llama-3-80B-Instruct` model.

You can also customise the system prompt and sampling parameters by setting `LLM_SYSTEM_PROMPT`, `LLM_TEMPERATURE`, `LLM_TOP_P`, and `LLM_MAX_TOKENS`.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details