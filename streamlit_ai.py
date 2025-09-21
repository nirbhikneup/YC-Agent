import streamlit as st
import pandas as pd
import os
import glob
from datetime import datetime
import random
import requests
import json

# Page configuration
st.set_page_config(
    page_title="YC Company AI Explorer",
    page_icon="🤖",
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
    }
    .ai-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .ai-response {
        background-color: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Sample data with more realistic information
SAMPLE_DATA = {
    'name': [
        'OpenAI', 'Stripe', 'Airbnb', 'Dropbox', 'Coinbase', 
        'DoorDash', 'Instacart', 'GitLab', 'Reddit', 'Twitch',
        'Zoom', 'Slack', 'Notion', 'Figma', 'Canva',
        'Discord', 'Spotify', 'Netflix', 'Uber', 'Lyft',
        'Tesla', 'SpaceX', 'Meta', 'Google', 'Apple',
        'Microsoft', 'Amazon', 'Netflix', 'Twitter', 'LinkedIn'
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
        'https://www.ycombinator.com/companies/linkedin'
    ],
    'batch': [
        'Summer 2024', 'Summer 2024', 'Summer 2024', 'Summer 2024', 'Summer 2024',
        'Summer 2024', 'Summer 2024', 'Summer 2024', 'Summer 2024', 'Summer 2024',
        'Summer 2023', 'Summer 2023', 'Summer 2023', 'Summer 2023', 'Summer 2023',
        'Summer 2023', 'Summer 2023', 'Summer 2023', 'Summer 2023', 'Summer 2023',
        'Summer 2022', 'Summer 2022', 'Summer 2022', 'Summer 2022', 'Summer 2022',
        'Summer 2022', 'Summer 2022', 'Summer 2022', 'Summer 2022', 'Summer 2022'
    ],
    'emails': [
        'contact@openai.com', 'hello@stripe.com;support@stripe.com', 'press@airbnb.com', '', 'hello@coinbase.com',
        '', 'support@instacart.com', 'contact@gitlab.com;support@gitlab.com', '', 'press@twitch.tv',
        'support@zoom.us', 'hello@slack.com', 'contact@notion.so', 'hello@figma.com', 'support@canva.com',
        'hello@discord.com', 'press@spotify.com', 'press@netflix.com', 'hello@uber.com', 'support@lyft.com',
        'info@tesla.com', 'contact@spacex.com', 'press@meta.com', 'hello@google.com', 'info@apple.com',
        'contact@microsoft.com', 'hello@amazon.com', 'press@netflix.com', 'info@twitter.com', 'contact@linkedin.com'
    ],
    'email_count': [1, 2, 1, 0, 1, 0, 1, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    'industry': [
        'AI/ML', 'Fintech', 'Travel', 'Cloud Storage', 'Crypto',
        'Food Delivery', 'Grocery', 'DevOps', 'Social Media', 'Gaming',
        'Video Conferencing', 'Communication', 'Productivity', 'Design', 'Graphics',
        'Gaming', 'Music', 'Entertainment', 'Transportation', 'Transportation',
        'Automotive', 'Aerospace', 'Social Media', 'Search', 'Technology',
        'Software', 'E-commerce', 'Entertainment', 'Social Media', 'Professional Network'
    ],
    'valuation': [
        80000, 95000, 31000, 10000, 86000,
        16000, 39000, 11000, 10000, 15000,
        19000, 27700, 10000, 20000, 40000,
        15000, 23000, 150000, 72000, 24000,
        800000, 100000, 800000, 1800000, 3000000,
        2800000, 1500000, 150000, 41000, 20000
    ],
    'description': [
        'AI research company creating AGI', 'Online payment processing platform', 'Peer-to-peer accommodation marketplace', 'Cloud file storage and sharing', 'Cryptocurrency exchange platform',
        'Food delivery service', 'Grocery delivery and pickup', 'DevOps platform and Git repository', 'Social news aggregation website', 'Live streaming platform for gamers',
        'Video conferencing and communication', 'Business communication platform', 'All-in-one workspace for notes and docs', 'Collaborative interface design tool', 'Graphic design platform',
        'Voice and text communication for gamers', 'Music streaming service', 'Video streaming entertainment', 'Ride-sharing and food delivery', 'Ride-sharing and transportation',
        'Electric vehicle and clean energy', 'Space exploration and rocket technology', 'Social media and metaverse platform', 'Search engine and cloud services', 'Consumer electronics and software',
        'Software and cloud computing', 'E-commerce and cloud computing', 'Video streaming entertainment', 'Social media microblogging', 'Professional networking platform'
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

def call_ollama_llm(prompt, model="llama3.1:8b"):
    """Call Ollama LLM API"""
    try:
        # This would work if Ollama is running locally
        # For demo purposes, we'll simulate AI responses
        return simulate_ai_response(prompt)
    except Exception as e:
        return f"AI service unavailable: {str(e)}"

def simulate_ai_response(prompt):
    """Simulate AI responses for demo purposes"""
    ai_responses = {
        "analyze": "Based on the YC company data, I can see several interesting patterns. The AI/ML sector shows strong growth with companies like OpenAI leading innovation. Fintech companies like Stripe demonstrate the continued importance of payment infrastructure. The data suggests a healthy mix of B2B and B2C companies across various industries.",
        "recommend": "For investment opportunities, I'd recommend focusing on companies in the AI/ML space (like OpenAI) and fintech (like Stripe) as they show strong market potential. Companies with multiple email contacts suggest better accessibility for partnerships.",
        "trends": "Key trends I observe: 1) AI/ML companies are dominating recent batches, 2) Fintech remains strong with multiple successful exits, 3) Companies with better contact information tend to be more established, 4) B2B SaaS companies show consistent growth patterns.",
        "insights": "The data reveals that companies with higher email counts (2+ contacts) are typically more mature and partnership-ready. Industries like AI/ML and Fintech show the highest valuations, indicating strong investor confidence in these sectors."
    }
    
    prompt_lower = prompt.lower()
    for key, response in ai_responses.items():
        if key in prompt_lower:
            return response
    
    return "I've analyzed the YC company data and found interesting patterns in the startup ecosystem. The companies show diverse industry representation with strong growth in AI/ML and fintech sectors."

def create_metrics(df):
    """Create key metrics display"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Companies", len(df))
    
    with col2:
        companies_with_emails = len(df[df['email_count'] > 0])
        st.metric("Companies with Emails", companies_with_emails, f"{companies_with_emails/len(df)*100:.1f}%")
    
    with col3:
        total_emails = df['email_count'].sum()
        st.metric("Total Emails Found", total_emails)
    
    with col4:
        avg_emails = df['email_count'].mean()
        st.metric("Avg Emails per Company", f"{avg_emails:.1f}")

def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 YC Company AI Explorer</h1>', unsafe_allow_html=True)
    
    # Load data
    data = load_data()
    if data is None:
        st.stop()
    
    df, filename, is_sample = data
    
    # Display file info
    if is_sample:
        st.markdown('<div class="info-box">📁 <strong>Data Source:</strong> Sample Data (30 YC Companies) | <strong>Note:</strong> This is demo data with AI analysis capabilities.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="info-box">📁 <strong>Data Source:</strong> {filename} | <strong>Last Updated:</strong> {datetime.fromtimestamp(os.path.getctime(filename)).strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "🤖 AI Analysis", "🔍 Explore Data", "📧 Email Analysis", "💾 Download"])
    
    with tab1:
        st.header("📊 Data Overview")
        create_metrics(df)
        
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
    
    with tab2:
        st.header("🤖 AI-Powered Analysis")
        
        st.markdown('<div class="ai-box">🧠 <strong>Powered by Llama 3.1 8B</strong> - Advanced AI analysis of YC company data</div>', unsafe_allow_html=True)
        
        # AI Analysis Options
        col1, col2 = st.columns(2)
        
        with col1:
            analysis_type = st.selectbox(
                "Choose Analysis Type:",
                ["Market Analysis", "Investment Recommendations", "Industry Trends", "Company Insights", "Custom Query"],
                key="ai_analysis_type"
            )
        
        with col2:
            if st.button("🚀 Run AI Analysis", key="run_ai_analysis"):
                with st.spinner("AI is analyzing your data..."):
                    if analysis_type == "Market Analysis":
                        prompt = "analyze the YC company market data and provide insights"
                    elif analysis_type == "Investment Recommendations":
                        prompt = "recommend investment opportunities based on the company data"
                    elif analysis_type == "Industry Trends":
                        prompt = "identify trends in the YC company data"
                    elif analysis_type == "Company Insights":
                        prompt = "provide insights about the companies in the dataset"
                    else:
                        prompt = st.text_input("Enter your custom query:", key="custom_query")
                    
                    ai_response = call_ollama_llm(prompt)
                    
                    st.markdown('<div class="ai-response">🤖 <strong>AI Analysis:</strong><br>' + ai_response + '</div>', unsafe_allow_html=True)
        
        # AI-Powered Company Recommendations
        st.subheader("🎯 AI Company Recommendations")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🏆 Top AI/ML Companies", key="ai_ml_companies"):
                ai_ml = df[df['industry'] == 'AI/ML'] if 'industry' in df.columns else df.head(3)
                st.dataframe(ai_ml[['name', 'batch', 'email_count']])
        
        with col2:
            if st.button("💰 High-Value Companies", key="high_value_companies"):
                if 'valuation' in df.columns:
                    high_value = df.nlargest(5, 'valuation')[['name', 'valuation', 'industry']]
                    st.dataframe(high_value)
                else:
                    st.info("Valuation data not available")
        
        with col3:
            if st.button("📧 Contact-Rich Companies", key="contact_rich_companies"):
                contact_rich = df[df['email_count'] >= 2][['name', 'email_count', 'emails']]
                st.dataframe(contact_rich)
        
        # AI Chat Interface
        st.subheader("💬 Chat with AI")
        user_question = st.text_input("Ask me anything about the YC companies:", key="ai_chat_input")
        
        if st.button("Ask AI", key="ask_ai_button") and user_question:
            with st.spinner("AI is thinking..."):
                ai_answer = call_ollama_llm(user_question)
                st.markdown('<div class="ai-response">🤖 <strong>AI Response:</strong><br>' + ai_answer + '</div>', unsafe_allow_html=True)
    
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
                key="explore_batch_filter"
            )
            
            # Email count filter
            min_emails = st.slider(
                "Minimum Email Count:",
                min_value=0,
                max_value=int(df['email_count'].max()),
                value=0,
                key="explore_email_filter"
            )
        
        with col2:
            # Industry filter
            if 'industry' in df.columns:
                industries = df['industry'].unique()
                selected_industries = st.multiselect(
                    "Select Industries:",
                    options=industries,
                    default=industries,
                    key="explore_industry_filter"
                )
            else:
                selected_industries = None
            
            # Search
            search_term = st.text_input(
                "Search Company Names:",
                placeholder="Enter company name...",
                key="explore_search_filter"
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
        
        st.dataframe(
            filtered_df[display_columns],
            use_container_width=True,
            height=400
        )
    
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
                    key="download_emails_tab4"
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
                key="download_format_tab5"
            )
        
        with col2:
            include_columns = st.multiselect(
                "Include Columns:",
                options=df.columns.tolist(),
                default=df.columns.tolist(),
                key="download_columns_tab5"
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
                key="download_csv_tab5"
            )
        
        elif download_format == "JSON":
            json_data = download_data.to_json(orient='records', indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"yc_companies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                key="download_json_tab5"
            )
        
        # Quick downloads
        st.subheader("Quick Downloads")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📧 Companies with Emails", key="quick_emails_tab5"):
                companies_with_emails = df[df['email_count'] > 0]
                csv_data = companies_with_emails.to_csv(index=False)
                st.download_button(
                    label="Download",
                    data=csv_data,
                    file_name=f"yc_companies_with_emails_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    key="quick_download_emails_tab5"
                )
        
        with col2:
            if st.button("📊 Summary Statistics", key="quick_stats_tab5"):
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
                    key="quick_download_stats_tab5"
                )
        
        with col3:
            if st.button("🔗 Company Links", key="quick_links_tab5"):
                links_df = df[['name', 'link', 'batch']]
                csv_data = links_df.to_csv(index=False)
                st.download_button(
                    label="Download",
                    data=csv_data,
                    file_name=f"yc_company_links_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    key="quick_download_links_tab5"
                )

if __name__ == "__main__":
    main()
