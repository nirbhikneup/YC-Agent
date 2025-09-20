# Deployment Guide

## Quick Deploy to Vercel

### Option 1: Deploy from GitHub (Recommended)

1. **Connect to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Sign up/Login with your GitHub account
   - Click "New Project"
   - Import your GitHub repository: `nirbhikneup/YC-Agent`

2. **Configure Build Settings:**
   - Framework Preset: `Other`
   - Build Command: `pip install -r requirements.txt && playwright install`
   - Output Directory: Leave empty
   - Install Command: `pip install -r requirements.txt`

3. **Environment Variables:**
   - No additional environment variables needed for basic functionality

4. **Deploy:**
   - Click "Deploy"
   - Wait for deployment to complete (usually 2-3 minutes)

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   vercel
   ```

4. **Follow the prompts:**
   - Link to existing project or create new
   - Confirm settings
   - Deploy

## Local Testing

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements.txt
playwright install

# Run the server
python main.py

# Open browser to http://localhost:8000
```

## Features After Deployment

✅ **Web Interface**: Clean, modern UI for selecting years and starting scrapes
✅ **Real-time Progress**: Live updates during scraping process
✅ **Email Extraction**: Automatically finds emails from company pages
✅ **CSV Download**: Download results as CSV files
✅ **Background Processing**: Non-blocking scraping with status updates
✅ **Error Handling**: Graceful error handling and user feedback

## API Endpoints

- `GET /` - Web interface
- `POST /scrape` - Start scraping with batch parameter
- `GET /status` - Get current scraping status
- `GET /download/{filename}` - Download CSV results
- `GET /results` - Get scraping results summary

## Usage

1. Open the deployed URL
2. Select a year from the dropdown
3. Click "Start Scraping"
4. Watch real-time progress
5. Download results when complete

## Troubleshooting

### Common Issues:

1. **Playwright not working on Vercel:**
   - Ensure `playwright install` is in build command
   - Check Vercel function timeout settings

2. **Timeout errors:**
   - Increase function timeout in `vercel.json`
   - Consider breaking large scrapes into smaller batches

3. **Memory issues:**
   - Vercel has memory limits for serverless functions
   - Consider implementing pagination for large datasets

## Performance Notes

- **Scraping Time**: ~2-5 minutes for 400+ companies
- **Memory Usage**: ~200-500MB during scraping
- **Rate Limiting**: Built-in delays to respect YC's servers
- **Concurrent Requests**: Limited to prevent overwhelming target site

## Security Considerations

- No authentication required (add if needed for production)
- CORS enabled for all origins (restrict in production)
- Input validation on batch parameter
- Error messages don't expose sensitive information
