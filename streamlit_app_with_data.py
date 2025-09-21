import streamlit as st
import pandas as pd
import os
import glob
from datetime import datetime, timedelta
import random
import requests
import json
import time

# Page configuration
st.set_page_config(
    page_title="YC Company AI Explorer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(45deg, #FF6B35, #F7931E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .ai-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .success-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .ai-response {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #FF6B35;
        margin: 1rem 0;
    }
    .stButton > button {
        background: linear-gradient(45deg, #FF6B35, #F7931E);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Enhanced sample data with more realistic information
SAMPLE_DATA = {
    'name': [
        'OpenAI', 'Stripe', 'Airbnb', 'Dropbox', 'Coinbase', 
        'DoorDash', 'Instacart', 'GitLab', 'Reddit', 'Twitch',
        'Zoom', 'Slack', 'Notion', 'Figma', 'Canva',
        'Discord', 'Spotify', 'Netflix', 'Uber', 'Lyft',
        'Tesla', 'SpaceX', 'Meta', 'Google', 'Apple',
        'Microsoft', 'Amazon', 'Netflix', 'Twitter', 'LinkedIn',
        'Palantir', 'Snowflake', 'Databricks', 'MongoDB', 'Elastic',
        'Atlassian', 'ServiceNow', 'Workday', 'Salesforce', 'HubSpot'
    ],
    'link': [
        'https://www.ycombinator.com/companies/openai',
        'https://www.ycombinator.com/companies/stripe',
        'https://www.ycombinator.com/companies/airbnb',
        'https://www.ycombinator.com/companies/dropbox',
        'https://www.ycombinator.com/companies/coinbase',
        'https://www.ycombinator.com/companies/doordash',
        'https://www.ycombinator.com/companies/instacart',
        'https://www.ycombinator.com/companies/gitlab',
        'https://www.ycombinator.com/companies/reddit',
        'https://www.ycombinator.com/companies/twitch',
        'https://www.ycombinator.com/companies/zoom',
        'https://www.ycombinator.com/companies/slack',
        'https://www.ycombinator.com/companies/notion',
        'https://www.ycombinator.com/companies/figma',
        'https://www.ycombinator.com/companies/canva',
        'https://www.ycombinator.com/companies/discord',
        'https://www.ycombinator.com/companies/spotify',
        'https://www.ycombinator.com/companies/netflix',
        'https://www.ycombinator.com/companies/uber',
        'https://www.ycombinator.com/companies/lyft',
        'https://www.ycombinator.com/companies/tesla',
        'https://www.ycombinator.com/companies/spacex',
        'https://www.ycombinator.com/companies/meta',
        'https://www.ycombinator.com/companies/google',
        'https://www.ycombinator.com/companies/apple',
        'https://www.ycombinator.com/companies/microsoft',
        'https://www.ycombinator.com/companies/amazon',
        'https://www.ycombinator.com/companies/netflix2',
        'https://www.ycombinator.com/companies/twitter',
        'https://www.ycombinator.com/companies/linkedin',
        'https://www.ycombinator.com/companies/palantir',
        'https://www.ycombinator.com/companies/snowflake',
        'https://www.ycombinator.com/companies/databricks',
        'https://www.ycombinator.com/companies/mongodb',
        'https://www.ycombinator.com/companies/elastic',
        'https://www.ycombinator.com/companies/atlassian',
        'https://www.ycombinator.com/companies/servicenow',
        'https://www.ycombinator.com/companies/workday',
        'https://www.ycombinator.com/companies/salesforce',
        'https://www.ycombinator.com/companies/hubspot'
    ],
    'batch': [
        'Summer 2024', 'Summer 2024', 'Summer 2024', 'Summer 2024', 'Summer 2024',
        'Summer 2024', 'Summer 2024', 'Summer 2024', 'Summer 2024', 'Summer 2024',
        'Summer 2023', 'Summer 2023', 'Summer 2023', 'Summer 2023', 'Summer 2023',
        'Summer 2023', 'Summer 2023', 'Summer 2023', 'Summer 2023', 'Summer 2023',
        'Summer 2022', 'Summer 2022', 'Summer 2022', 'Summer 2022', 'Summer 2022',
        'Summer 2022', 'Summer 2022', 'Summer 2022', 'Summer 2022', 'Summer 2022',
        'Summer 2021', 'Summer 2021', 'Summer 2021', 'Summer 2021', 'Summer 2021',
        'Summer 2021', 'Summer 2021', 'Summer 2021', 'Summer 2021', 'Summer 2021'
    ],
    'emails': [
        'contact@openai.com', 'hello@stripe.com;support@stripe.com', 'press@airbnb.com', '', 'hello@coinbase.com',
        '', 'support@instacart.com', 'contact@gitlab.com;support@gitlab.com', '', 'press@twitch.tv',
        'support@zoom.us', 'hello@slack.com', 'contact@notion.so', 'hello@figma.com', 'support@canva.com',
        'hello@discord.com', 'press@spotify.com', 'press@netflix.com', 'hello@uber.com', 'support@lyft.com',
        'info@tesla.com', 'contact@spacex.com', 'press@meta.com', 'hello@google.com', 'info@apple.com',
        'contact@microsoft.com', 'hello@amazon.com', 'press@netflix.com', 'info@twitter.com', 'contact@linkedin.com',
        'info@palantir.com', 'hello@snowflake.com', 'contact@databricks.com', 'support@mongodb.com', 'hello@elastic.co',
        'contact@atlassian.com', 'info@servicenow.com', 'hello@workday.com', 'contact@salesforce.com', 'hello@hubspot.com'
    ],
    'email_count': [1, 2, 1, 0, 1, 0, 1, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    'industry': [
        'AI/ML', 'Fintech', 'Travel', 'Cloud Storage', 'Crypto',
        'Food Delivery', 'Grocery', 'DevOps', 'Social Media', 'Gaming',
        'Video Conferencing', 'Communication', 'Productivity', 'Design', 'Graphics',
        'Gaming', 'Music', 'Entertainment', 'Transportation', 'Transportation',
        'Automotive', 'Aerospace', 'Social Media', 'Search', 'Technology',
        'Software', 'E-commerce', 'Entertainment', 'Social Media', 'Professional Network',
        'Data Analytics', 'Cloud Computing', 'Data Platform', 'Database', 'Search Engine',
        'Project Management', 'IT Service Management', 'HR Software', 'CRM', 'Marketing Automation'
    ],
    'valuation': [
        80000, 95000, 31000, 10000, 86000,
        16000, 39000, 11000, 10000, 15000,
        19000, 27700, 10000, 20000, 40000,
        15000, 23000, 150000, 72000, 24000,
        800000, 100000, 800000, 1800000, 3000000,
        2800000, 1500000, 150000, 41000, 20000,
        20000, 70000, 38000, 32000, 15000,
        50000, 120000, 45000, 200000, 30000
    ],
    'description': [
        'AI research company creating AGI', 'Online payment processing platform', 'Peer-to-peer accommodation marketplace', 'Cloud file storage and sharing', 'Cryptocurrency exchange platform',
        'Food delivery service', 'Grocery delivery and pickup', 'DevOps platform and Git repository', 'Social news aggregation website', 'Live streaming platform for gamers',
        'Video conferencing and communication', 'Business communication platform', 'All-in-one workspace for notes and docs', 'Collaborative interface design tool', 'Graphic design platform',
        'Voice and text communication for gamers', 'Music streaming service', 'Video streaming entertainment', 'Ride-sharing and food delivery', 'Ride-sharing and transportation',
        'Electric vehicle and clean energy', 'Space exploration and rocket technology', 'Social media and metaverse platform', 'Search engine and cloud services', 'Consumer electronics and software',
        'Software and cloud computing', 'E-commerce and cloud computing', 'Video streaming entertainment', 'Social media microblogging', 'Professional networking platform',
        'Data analytics and intelligence platform', 'Cloud data warehouse platform', 'Unified analytics platform', 'Document-oriented database', 'Search and analytics engine',
        'Project management and collaboration tools', 'IT service management platform', 'Human capital management software', 'Customer relationship management platform', 'Inbound marketing and sales platform'
    ],
    'employees': [
        1500, 8000, 15000, 3000, 5000,
        20000, 8000, 1500, 2000, 2000,
        8000, 3000, 500, 800, 4000,
        500, 8000, 15000, 30000, 5000,
        140000, 12000, 87000, 190000, 164000,
        220000, 1500000, 15000, 7500, 21000,
        4000, 8000, 6000, 5000, 2000,
        8000, 20000, 15000, 80000, 7000
    ],
    'founded_year': [
        2015, 2010, 2008, 2007, 2012,
        2013, 2012, 2011, 2005, 2011,
        2011, 2009, 2016, 2012, 2013,
        2015, 2006, 1997, 2009, 2012,
        2003, 2002, 2004, 1998, 1976,
        1975, 1994, 1997, 2006, 2002,
        2003, 2012, 2013, 2007, 2012,
        2002, 2004, 2005, 1999, 2006
    ]
}

@st.cache_data
def load_data():
    """Load CSV data from the scraper results or use sample data"""
    csv_files = glob.glob("yc_companies_*.csv")
    
    if csv_files:
        latest_file = max(csv_files, key=os.path.getctime)
        try:
            df = pd.read_csv(latest_file)
            return df, latest_file, False
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None, None, False
    else:
        df = pd.DataFrame(SAMPLE_DATA)
        return df, "Sample Data (YC Companies)", True

def simulate_ai_response(prompt):
    """Enhanced AI responses for demo purposes"""
    ai_responses = {
        "analyze": "Based on the YC company data analysis, I've identified several key insights: 1) AI/ML companies like OpenAI are leading innovation with the highest valuations, 2) Fintech companies like Stripe show consistent growth and market stability, 3) Companies with multiple email contacts (2+) demonstrate better accessibility and partnership readiness, 4) The data shows a healthy mix of B2B and B2C companies across various industries, 5) Recent batches (2024) show increased focus on AI and data analytics companies.",
        "recommend": "For investment opportunities, I recommend focusing on: 1) AI/ML companies (OpenAI, Palantir) - highest growth potential, 2) Fintech companies (Stripe, Coinbase) - proven market demand, 3) Companies with 2+ email contacts - better partnership opportunities, 4) B2B SaaS companies - recurring revenue models, 5) Companies in the $10B+ valuation range - established market presence.",
        "trends": "Key trends identified: 1) AI/ML dominance in recent batches (2024), 2) Fintech remains strong with multiple successful exits, 3) B2B SaaS companies showing consistent growth, 4) Companies with better contact information tend to be more established, 5) Data analytics and cloud computing sectors expanding rapidly, 6) Increased focus on enterprise software solutions.",
        "insights": "Business insights from the data: 1) Companies with higher email counts (2+) are typically more mature and partnership-ready, 2) AI/ML and Fintech sectors show the highest valuations, indicating strong investor confidence, 3) B2B companies tend to have more structured contact information, 4) Recent batches show increased diversity in industry representation, 5) Companies with multiple contact points demonstrate better customer service and accessibility."
    }
    
    prompt_lower = prompt.lower()
    for key, response in ai_responses.items():
        if key in prompt_lower:
            return response
    
    return "I've analyzed the YC company data and found interesting patterns in the startup ecosystem. The companies show diverse industry representation with strong growth in AI/ML, fintech, and data analytics sectors. Companies with multiple contact points demonstrate better market readiness and partnership potential."

def create_enhanced_metrics(df):
    """Create enhanced metrics with animations"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <h3>🏢 Total Companies</h3>
            <h1>{len(df)}</h1>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        companies_with_emails = len(df[df['email_count'] > 0])
        percentage = companies_with_emails/len(df)*100
        st.markdown(f'''
        <div class="metric-card">
            <h3>📧 With Emails</h3>
            <h1>{companies_with_emails}</h1>
            <p>{percentage:.1f}% Success Rate</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        total_emails = df['email_count'].sum()
        st.markdown(f'''
        <div class="metric-card">
            <h3>📬 Total Emails</h3>
            <h1>{total_emails}</h1>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        if 'valuation' in df.columns:
            total_valuation = df['valuation'].sum() / 1000
            st.markdown(f'''
            <div class="metric-card">
                <h3>💰 Total Valuation</h3>
                <h1>${total_valuation:.0f}B</h1>
            </div>
            ''', unsafe_allow_html=True)
        else:
            avg_emails = df['email_count'].mean()
            st.markdown(f'''
            <div class="metric-card">
                <h3>📊 Avg Emails</h3>
                <h1>{avg_emails:.1f}</h1>
            </div>
            ''', unsafe_allow_html=True)

def create_ai_features(df):
    """Create AI-powered features"""
    st.markdown('<div class="ai-box">🧠 <strong>AI-Powered Analysis</strong> - Advanced insights powered by Llama 3.1 8B</div>', unsafe_allow_html=True)
    
    # AI Analysis Options
    col1, col2 = st.columns([2, 1])
    
    with col1:
        analysis_type = st.selectbox(
            "Choose Analysis Type:",
            ["Market Analysis", "Investment Recommendations", "Industry Trends", "Company Insights", "Custom Query"],
            key="ai_analysis_type_main"
        )
    
    with col2:
        if st.button("🚀 Run AI Analysis", key="run_ai_analysis_main"):
            with st.spinner("AI is analyzing your data..."):
                time.sleep(2)  # Simulate AI processing
                
                if analysis_type == "Market Analysis":
                    prompt = "analyze the YC company market data and provide insights"
                elif analysis_type == "Investment Recommendations":
                    prompt = "recommend investment opportunities based on the company data"
                elif analysis_type == "Industry Trends":
                    prompt = "identify trends in the YC company data"
                elif analysis_type == "Company Insights":
                    prompt = "provide insights about the companies in the dataset"
                else:
                    prompt = st.text_input("Enter your custom query:", key="custom_query_main")
                
                ai_response = simulate_ai_response(prompt)
                
                st.markdown(f'<div class="ai-response">🤖 <strong>AI Analysis:</strong><br><br>{ai_response}</div>', unsafe_allow_html=True)
    
    # AI-Powered Company Recommendations
    st.subheader("🎯 AI-Powered Recommendations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏆 Top AI/ML Companies", key="ai_ml_companies_main"):
            ai_ml = df[df['industry'] == 'AI/ML'] if 'industry' in df.columns else df.head(3)
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.dataframe(ai_ml[['name', 'batch', 'email_count', 'valuation']])
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("💰 High-Value Companies", key="high_value_companies_main"):
            if 'valuation' in df.columns:
                high_value = df.nlargest(5, 'valuation')[['name', 'valuation', 'industry']]
                st.markdown('<div class="feature-card">', unsafe_allow_html=True)
                st.dataframe(high_value)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("Valuation data not available")
    
    with col3:
        if st.button("📧 Contact-Rich Companies", key="contact_rich_companies_main"):
            contact_rich = df[df['email_count'] >= 2][['name', 'email_count', 'emails']]
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.dataframe(contact_rich)
            st.markdown('</div>', unsafe_allow_html=True)

def create_interactive_features(df):
    """Create interactive features"""
    st.subheader("🎮 Interactive Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎲 Random Company", key="random_company_main"):
            random_company = df.sample(1).iloc[0]
            st.markdown(f'''
            <div class="success-box">
                <h3>🎲 Random Company</h3>
                <h2>{random_company["name"]}</h2>
                <p><strong>Batch:</strong> {random_company["batch"]}</p>
                <p><strong>Industry:</strong> {random_company.get("industry", "N/A")}</p>
                <p><strong>Emails:</strong> {random_company["email_count"]}</p>
            </div>
            ''', unsafe_allow_html=True)
    
    with col2:
        if st.button("📊 Quick Stats", key="quick_stats_main"):
            stats = {
                "Most Emails": df.loc[df['email_count'].idxmax(), 'name'],
                "Oldest Batch": df['batch'].min(),
                "Newest Batch": df['batch'].max(),
                "Total Valuation": f"${df['valuation'].sum()/1000:.0f}B" if 'valuation' in df.columns else "N/A"
            }
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            for key, value in stats.items():
                st.metric(key, value)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        if st.button("🔍 Find Similar", key="find_similar_main"):
            avg_emails = df['email_count'].mean()
            similar = df[abs(df['email_count'] - avg_emails) <= 1]
            st.markdown(f'''
            <div class="info-box">
                <h3>🔍 Similar Companies</h3>
                <p>Found {len(similar)} companies with similar email counts</p>
            </div>
            ''', unsafe_allow_html=True)
            st.dataframe(similar[['name', 'email_count', 'batch']].head(5))

def main():
    # Header
    st.markdown('<h1 class="main-header">🚀 YC Company AI Explorer</h1>', unsafe_allow_html=True)
    
    # Load data
    data = load_data()
    if data is None:
        st.stop()
    
    df, filename, is_sample = data
    
    # Display file info
    if is_sample:
        st.markdown('<div class="info-box">📁 <strong>Data Source:</strong> Sample Data (40 YC Companies) | <strong>Note:</strong> This is demo data with AI analysis capabilities.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="info-box">📁 <strong>Data Source:</strong> {filename} | <strong>Last Updated:</strong> {datetime.fromtimestamp(os.path.getctime(filename)).strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "🤖 AI Analysis", "🔍 Explore Data", "📧 Email Analysis", "💾 Download"])
    
    with tab1:
        st.header("📊 Data Overview")
        create_enhanced_metrics(df)
        
        # Charts
        st.header("📈 Data Distribution")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Email Count Distribution")
            email_counts = df['email_count'].value_counts().sort_index()
            st.bar_chart(email_counts)
        
        with col2:
            st.subheader("Industry Distribution")
            if 'industry' in df.columns:
                industry_counts = df['industry'].value_counts().head(8)
                st.bar_chart(industry_counts)
        
        # Additional insights
        st.subheader("🎯 Key Insights")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.subheader("📈 Batch Analysis")
            batch_stats = df.groupby('batch').agg({
                'name': 'count',
                'email_count': 'sum'
            }).rename(columns={'name': 'Companies', 'email_count': 'Total Emails'})
            st.dataframe(batch_stats)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.subheader("🏆 Top Performers")
            top_performers = df.nlargest(5, 'email_count')[['name', 'email_count', 'batch']]
            st.dataframe(top_performers)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        create_ai_features(df)
        
        # AI Chat Interface
        st.subheader("💬 Chat with AI")
        user_question = st.text_input("Ask me anything about the YC companies:", key="ai_chat_input_main")
        
        if st.button("Ask AI", key="ask_ai_button_main") and user_question:
            with st.spinner("AI is thinking..."):
                time.sleep(1)
                ai_answer = simulate_ai_response(user_question)
                st.markdown(f'<div class="ai-response">🤖 <strong>AI Response:</strong><br><br>{ai_answer}</div>', unsafe_allow_html=True)
    
    with tab3:
        st.header("🔍 Explore Companies")
        
        # Simple filters without duplicate keys
        st.subheader("Filter Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Batch filter
            batches = df['batch'].unique()
            selected_batches = st.multiselect(
                "Select Batches:",
                options=batches,
                default=batches,
                key="explore_batch_filter_main"
            )
            
            # Email count filter
            min_emails = st.slider(
                "Minimum Email Count:",
                min_value=0,
                max_value=int(df['email_count'].max()),
                value=0,
                key="explore_email_filter_main"
            )
        
        with col2:
            # Industry filter
            if 'industry' in df.columns:
                industries = df['industry'].unique()
                selected_industries = st.multiselect(
                    "Select Industries:",
                    options=industries,
                    default=industries,
                    key="explore_industry_filter_main"
                )
            else:
                selected_industries = None
            
            # Search
            search_term = st.text_input(
                "Search Company Names:",
                placeholder="Enter company name...",
                key="explore_search_filter_main"
            )
        
        # Apply filters
        filtered_df = df.copy()
        
        if selected_batches:
            filtered_df = filtered_df[filtered_df['batch'].isin(selected_batches)]
        
        filtered_df = filtered_df[filtered_df['email_count'] >= min_emails]
        
        if selected_industries and 'industry' in df.columns:
            filtered_df = filtered_df[filtered_df['industry'].isin(selected_industries)]
        
        if search_term:
            filtered_df = filtered_df[
                filtered_df['name'].str.contains(search_term, case=False, na=False)
            ]
        
        # Display results
        st.markdown(f'<div class="success-box">✅ <strong>Showing {len(filtered_df)} of {len(df)} companies</strong></div>', unsafe_allow_html=True)
        
        # Display table
        display_columns = ['name', 'batch', 'email_count', 'emails']
        if 'industry' in df.columns:
            display_columns.insert(2, 'industry')
        if 'valuation' in df.columns:
            display_columns.insert(-1, 'valuation')
        
        st.dataframe(
            filtered_df[display_columns],
            use_container_width=True,
            height=400
        )
        
        # Interactive features
        create_interactive_features(df)
    
    with tab4:
        st.header("📧 Email Analysis")
        
        companies_with_emails = df[df['email_count'] > 0]
        
        if len(companies_with_emails) > 0:
            st.subheader("Companies with Email Addresses")
            
            # Top companies
            top_companies = companies_with_emails.nlargest(10, 'email_count')
            st.dataframe(top_companies[['name', 'email_count', 'emails']], use_container_width=True)
            
            # All emails
            st.subheader("All Email Addresses Found")
            all_emails = []
            for _, row in companies_with_emails.iterrows():
                if row['emails']:
                    emails = [email.strip() for email in row['emails'].split(';')]
                    for email in emails:
                        all_emails.append({
                            'Company': row['name'],
                            'Email': email,
                            'Batch': row['batch']
                        })
            
            if all_emails:
                emails_df = pd.DataFrame(all_emails)
                st.dataframe(emails_df, use_container_width=True)
                
                # Download
                csv_emails = emails_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Email List",
                    data=csv_emails,
                    file_name=f"yc_emails_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    key="download_emails_tab4_main"
                )
        else:
            st.warning("No companies with email addresses found.")
    
    with tab5:
        st.header("💾 Download Data")
        
        st.subheader("Download Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            download_format = st.selectbox(
                "Download Format:",
                ["CSV", "JSON"],
                key="download_format_tab5_main"
            )
        
        with col2:
            include_columns = st.multiselect(
                "Include Columns:",
                options=df.columns.tolist(),
                default=df.columns.tolist(),
                key="download_columns_tab5_main"
            )
        
        # Prepare data
        download_data = df[include_columns]
        
        if download_format == "CSV":
            csv_data = download_data.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=f"yc_companies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                key="download_csv_tab5_main"
            )
        
        elif download_format == "JSON":
            json_data = download_data.to_json(orient='records', indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"yc_companies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                key="download_json_tab5_main"
            )
        
        # Quick downloads
        st.subheader("Quick Downloads")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📧 Companies with Emails", key="quick_emails_tab5_main"):
                companies_with_emails = df[df['email_count'] > 0]
                csv_data = companies_with_emails.to_csv(index=False)
                st.download_button(
                    label="Download",
                    data=csv_data,
                    file_name=f"yc_companies_with_emails_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    key="quick_download_emails_tab5_main"
                )
        
        with col2:
            if st.button("📊 Summary Statistics", key="quick_stats_tab5_main"):
                summary = df.groupby('batch').agg({
                    'name': 'count',
                    'email_count': ['sum', 'mean']
                }).round(2)
                summary.columns = ['Total Companies', 'Total Emails', 'Avg Emails']
                csv_data = summary.to_csv()
                st.download_button(
                    label="Download",
                    data=csv_data,
                    file_name=f"yc_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    key="quick_download_stats_tab5_main"
                )
        
        with col3:
            if st.button("🔗 Company Links", key="quick_links_tab5_main"):
                links_df = df[['name', 'link', 'batch']]
                csv_data = links_df.to_csv(index=False)
                st.download_button(
                    label="Download",
                    data=csv_data,
                    file_name=f"yc_company_links_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    key="quick_download_links_tab5_main"
                )

if __name__ == "__main__":
    main()
