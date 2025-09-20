# 🚀 YC Company Data Explorer - Deployment Guide

## ✅ What We've Built

A complete YC company data exploration system with:

1. **🔧 YC Scraper** (`scraper/yc_scraper.py`)
   - Headless web scraping with Playwright
   - Email extraction from company pages
   - Year-based batch filtering
   - CSV and SQLite output

2. **📊 Streamlit Dashboard** (`streamlit_app.py`)
   - Interactive data exploration
   - Advanced filtering and search
   - Beautiful visualizations with Plotly
   - Multiple download formats (CSV, Excel, JSON)
   - Email analysis and extraction

## 🎯 Quick Deploy to Streamlit Community Cloud

### Step 1: Your Code is Ready! ✅
- ✅ All files committed to GitHub
- ✅ Streamlit app created and tested
- ✅ Requirements file ready
- ✅ Sample data included

### Step 2: Deploy to Streamlit (2 minutes)

1. **Go to Streamlit Community Cloud:**
   - Visit: https://share.streamlit.io
   - Sign in with your GitHub account

2. **Deploy your app:**
   - Click "New app"
   - Repository: `nirbhikneup/YC-Agent`
   - Branch: `main`
   - Main file path: `streamlit_app.py`
   - Click "Deploy"

3. **Your app will be live at:**
   - `https://yc-agent.streamlit.app` (or similar URL)

## 🎨 App Features

### 📊 Overview Tab
- **Key Metrics**: Total companies, email counts, success rates
- **Visualizations**: Interactive charts showing data distribution
- **Quick Stats**: At-a-glance insights

### 🔍 Explore Data Tab
- **Advanced Filtering**: By batch, email count, company name
- **Search**: Real-time company name search
- **Pagination**: Handle large datasets efficiently
- **Custom Views**: Choose which columns to display

### 📧 Email Analysis Tab
- **Email Extraction**: All found email addresses
- **Company Mapping**: See which emails belong to which companies
- **Top Performers**: Companies with most emails
- **Download**: Email-only CSV export

### 💾 Download Tab
- **Multiple Formats**: CSV, Excel, JSON
- **Filtered Downloads**: Apply filters before downloading
- **Quick Downloads**: Pre-configured exports
- **Custom Selection**: Choose specific columns

## 🔄 Workflow

### For New Data:
1. **Run the scraper:**
   ```bash
   python scraper/yc_scraper.py "Summer 2024"
   ```

2. **Upload CSV to Streamlit:**
   - The app automatically finds the latest CSV file
   - Or manually upload via the Streamlit interface

3. **Explore and download:**
   - Use the interactive dashboard
   - Filter and analyze your data
   - Download results in your preferred format

## 🎯 Use Cases

### 📈 Business Development
- Find companies with contact information
- Filter by specific YC batches
- Export email lists for outreach

### 📊 Market Research
- Analyze YC company trends
- Track email availability by batch
- Generate reports and summaries

### 🔍 Data Analysis
- Visualize company distributions
- Identify patterns in email collection
- Export data for further analysis

## 🛠️ Local Development

```bash
# Install dependencies
pip install -r requirements-streamlit.txt

# Run the app
streamlit run streamlit_app.py

# Open browser to http://localhost:8501
```

## 📁 File Structure

```
yc_agent/
├── streamlit_app.py              # 🎨 Main Streamlit app
├── requirements-streamlit.txt    # 📦 Dependencies
├── yc_companies_*.csv           # 📊 Data files
├── scraper/
│   └── yc_scraper.py            # 🔧 Web scraper
├── README-Streamlit.md          # 📖 App documentation
└── DEPLOYMENT-GUIDE.md          # 🚀 This file
```

## 🎉 Success Metrics

Your deployed app will have:
- ✅ **Beautiful UI**: Modern, responsive design
- ✅ **Fast Performance**: Optimized for large datasets
- ✅ **Interactive Features**: Real-time filtering and search
- ✅ **Multiple Exports**: CSV, Excel, JSON downloads
- ✅ **Visual Analytics**: Charts and graphs
- ✅ **Email Focus**: Dedicated email analysis tools

## 🔗 Next Steps

1. **Deploy to Streamlit** (2 minutes)
2. **Test with real data** (run the scraper)
3. **Share with your team**
4. **Customize as needed**

## 🆘 Support

- **Streamlit Docs**: https://docs.streamlit.io
- **Community**: https://discuss.streamlit.io
- **GitHub Issues**: Create an issue in your repo

---

**🎯 Ready to deploy? Go to https://share.streamlit.io and deploy your YC Data Explorer! 🚀**
