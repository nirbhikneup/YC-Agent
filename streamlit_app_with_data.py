import streamlit as st
import pandas as pd
import os
import glob
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="YC Company Data Explorer",
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
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FF6B35;
    }
</style>
""", unsafe_allow_html=True)

# Sample data embedded in the app
SAMPLE_DATA = {
    'name': [
        'OpenAI', 'Stripe', 'Airbnb', 'Dropbox', 'Coinbase', 
        'DoorDash', 'Instacart', 'GitLab', 'Reddit', 'Twitch',
        'Zoom', 'Slack', 'Notion', 'Figma', 'Canva',
        'Discord', 'Spotify', 'Netflix', 'Uber', 'Lyft'
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
        'https://www.ycombinator.com/companies/lyft'
    ],
    'batch': [
        'Summer 2024', 'Summer 2024', 'Summer 2024', 'Summer 2024', 'Summer 2024',
        'Summer 2024', 'Summer 2024', 'Summer 2024', 'Summer 2024', 'Summer 2024',
        'Summer 2023', 'Summer 2023', 'Summer 2023', 'Summer 2023', 'Summer 2023',
        'Summer 2023', 'Summer 2023', 'Summer 2023', 'Summer 2023', 'Summer 2023'
    ],
    'emails': [
        'contact@openai.com', 'hello@stripe.com;support@stripe.com', 'press@airbnb.com', '', 'hello@coinbase.com',
        '', 'support@instacart.com', 'contact@gitlab.com;support@gitlab.com', '', 'press@twitch.tv',
        'support@zoom.us', 'hello@slack.com', 'contact@notion.so', 'hello@figma.com', 'support@canva.com',
        'hello@discord.com', 'press@spotify.com', 'press@netflix.com', 'hello@uber.com', 'support@lyft.com'
    ],
    'email_count': [1, 2, 1, 0, 1, 0, 1, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
}

def load_data():
    """Load CSV data from the scraper results or use sample data"""
    csv_files = glob.glob("yc_companies_*.csv")
    
    if csv_files:
        # Load the most recent file
        latest_file = max(csv_files, key=os.path.getctime)
        try:
            df = pd.read_csv(latest_file)
            return df, latest_file, False
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None, None, False
    else:
        # Use sample data
        df = pd.DataFrame(SAMPLE_DATA)
        return df, "Sample Data (YC Companies)", True

def create_metrics(df):
    """Create key metrics display"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Companies",
            value=len(df),
            delta=None
        )
    
    with col2:
        companies_with_emails = len(df[df['email_count'] > 0])
        st.metric(
            label="Companies with Emails",
            value=companies_with_emails,
            delta=f"{companies_with_emails/len(df)*100:.1f}%"
        )
    
    with col3:
        total_emails = df['email_count'].sum()
        st.metric(
            label="Total Emails Found",
            value=total_emails,
            delta=None
        )
    
    with col4:
        avg_emails = df['email_count'].mean()
        st.metric(
            label="Avg Emails per Company",
            value=f"{avg_emails:.1f}",
            delta=None
        )

def filter_data(df):
    """Create filtering interface"""
    st.sidebar.header("🔍 Filter Data")
    
    # Batch filter
    batches = df['batch'].unique()
    selected_batches = st.sidebar.multiselect(
        "Select Batches:",
        options=batches,
        default=batches
    )
    
    # Email count filter
    min_emails = st.sidebar.slider(
        "Minimum Email Count:",
        min_value=0,
        max_value=int(df['email_count'].max()),
        value=0
    )
    
    # Company name search
    search_term = st.sidebar.text_input(
        "Search Company Names:",
        placeholder="Enter company name..."
    )
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_batches:
        filtered_df = filtered_df[filtered_df['batch'].isin(selected_batches)]
    
    filtered_df = filtered_df[filtered_df['email_count'] >= min_emails]
    
    if search_term:
        filtered_df = filtered_df[
            filtered_df['name'].str.contains(search_term, case=False, na=False)
        ]
    
    return filtered_df

def main():
    # Header
    st.markdown('<h1 class="main-header">🚀 YC Company Data Explorer</h1>', unsafe_allow_html=True)
    
    # Load data
    data = load_data()
    if data is None:
        st.stop()
    
    df, filename, is_sample = data
    
    # Display file info
    if is_sample:
        st.info(f"📁 **Data Source:** {filename} | **Note:** This is sample data. Upload your own CSV file or run the scraper to get real data.")
    else:
        st.info(f"📁 **Data Source:** {filename} | **Last Updated:** {datetime.fromtimestamp(os.path.getctime(filename)).strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔍 Explore Data", "📧 Email Analysis", "💾 Download"])
    
    with tab1:
        st.header("📊 Data Overview")
        create_metrics(df)
        
        # Simple charts without plotly
        st.header("📈 Data Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Email Count Distribution")
            email_counts = df['email_count'].value_counts().sort_index()
            st.bar_chart(email_counts)
        
        with col2:
            st.subheader("Companies with vs without Emails")
            email_status = df['email_count'].apply(lambda x: 'With Emails' if x > 0 else 'No Emails')
            status_counts = email_status.value_counts()
            st.bar_chart(status_counts)
    
    with tab2:
        st.header("🔍 Explore Companies")
        
        # Filter data
        filtered_df = filter_data(df)
        
        # Display filtered results
        st.write(f"**Showing {len(filtered_df)} of {len(df)} companies**")
        
        # Display options
        col1, col2 = st.columns([3, 1])
        with col1:
            show_columns = st.multiselect(
                "Select columns to display:",
                options=df.columns.tolist(),
                default=['name', 'batch', 'email_count', 'emails']
            )
        
        with col2:
            rows_per_page = st.selectbox("Rows per page:", [10, 25, 50, 100], index=1)
        
        # Pagination
        total_pages = (len(filtered_df) - 1) // rows_per_page + 1
        if total_pages > 1:
            page = st.selectbox("Page:", range(1, total_pages + 1))
            start_idx = (page - 1) * rows_per_page
            end_idx = start_idx + rows_per_page
            display_df = filtered_df.iloc[start_idx:end_idx]
        else:
            display_df = filtered_df
        
        # Display table
        st.dataframe(
            display_df[show_columns],
            use_container_width=True,
            height=400
        )
    
    with tab3:
        st.header("📧 Email Analysis")
        
        # Companies with emails
        companies_with_emails = df[df['email_count'] > 0]
        
        if len(companies_with_emails) > 0:
            st.subheader("Companies with Email Addresses")
            
            # Top companies by email count
            top_companies = companies_with_emails.nlargest(10, 'email_count')
            st.subheader("Top 10 Companies by Email Count")
            st.dataframe(top_companies[['name', 'email_count', 'emails']], use_container_width=True)
            
            # Email addresses list
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
                
                # Download emails
                csv_emails = emails_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Email List",
                    data=csv_emails,
                    file_name=f"yc_emails_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        else:
            st.warning("No companies with email addresses found.")
    
    with tab4:
        st.header("💾 Download Data")
        
        # Filter data for download
        download_df = filter_data(df)
        
        st.subheader("Download Filtered Data")
        st.write(f"**{len(download_df)} companies** will be included in the download")
        
        # Download options
        col1, col2 = st.columns(2)
        
        with col1:
            download_format = st.selectbox(
                "Download Format:",
                ["CSV", "JSON"]
            )
        
        with col2:
            include_columns = st.multiselect(
                "Include Columns:",
                options=df.columns.tolist(),
                default=df.columns.tolist()
            )
        
        # Prepare data for download
        download_data = download_df[include_columns]
        
        if download_format == "CSV":
            csv_data = download_data.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=f"yc_companies_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        elif download_format == "JSON":
            json_data = download_data.to_json(orient='records', indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"yc_companies_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        # Quick download buttons
        st.subheader("Quick Downloads")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📧 Companies with Emails Only"):
                companies_with_emails = df[df['email_count'] > 0]
                csv_data = companies_with_emails.to_csv(index=False)
                st.download_button(
                    label="Download",
                    data=csv_data,
                    file_name=f"yc_companies_with_emails_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📊 Summary Statistics"):
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
                    mime="text/csv"
                )
        
        with col3:
            if st.button("🔗 Company Links Only"):
                links_df = df[['name', 'link', 'batch']]
                csv_data = links_df.to_csv(index=False)
                st.download_button(
                    label="Download",
                    data=csv_data,
                    file_name=f"yc_company_links_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()
