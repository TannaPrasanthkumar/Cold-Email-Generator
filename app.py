import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
import os
import time
import json

from model import Model
from portfolio import Portfolio
from utils import clean_text

# Set default user agent
if not os.environ.get("USER_AGENT"):
    os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def safe_format_text(text):
    """Safely handle text that might contain curly braces by escaping them."""
    if isinstance(text, str):
        return text.replace("{", "{{").replace("}", "}}")
    return text

def show_job_details(job):
    """Display job details in an organized way"""
    with st.expander("📋 View Job Details", expanded=False):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 🎯 Role")
            st.write(job.get('role', 'Not specified'))
            
            st.markdown("### ⏳ Experience Required")
            st.write(job.get('experience', 'Not specified'))
        
        with col2:
            st.markdown("### 🔧 Required Skills")
            skills = job.get('skills', [])
            if skills:
                for skill in skills:
                    st.write(f"- {skill}")
            else:
                st.write("No specific skills listed")
        
        st.markdown("### 📝 Job Description")
        st.write(job.get('description', 'No description available'))

def create_streamlit_app(llm, portfolio, clean_text):
    # Set up the sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Settings")
        st.markdown("---")
        
        # Add portfolio status
        st.markdown("### 📊 Portfolio Status")
        if portfolio.collection.count():
            st.success("Portfolio loaded successfully!")
            st.info(f"Total entries: {portfolio.collection.count()}")
        else:
            st.warning("Portfolio not loaded yet")
        
        # Add some helpful tips
        st.markdown("### 💡 Tips")
        st.markdown("""
        - Make sure the job URL is accessible
        - Check if the URL contains full job description
        - Wait for the email generation to complete
        - Review the job details before using the email
        """)
        
        # Add contact/about section
        st.markdown("### 📬 Contact")
        st.markdown("For issues or suggestions, please contact:")
        st.markdown("📧 tannaprasanthkumar76@gmail.com")

    # Main content
    st.title("📧 Cold Mail Generator")
    st.markdown("""
    <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
        <h4 style='color: #262730; margin-bottom: 15px; font-size: 1.2em;'>Welcome to the Cold Mail Generator! 👋</h4>
        <p style='color: #424242; margin-bottom: 15px;'>This tool helps you create personalized cold emails for job applications by:</p>
        <ul style='color: #424242; margin-left: 20px;'>
            <li style='margin-bottom: 8px;'>📊 Analyzing job postings automatically</li>
            <li style='margin-bottom: 8px;'>🎯 Matching your portfolio with job requirements</li>
            <li style='margin-bottom: 8px;'>✉️ Generating professional cold emails</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for input
    col1, col2 = st.columns([2, 1])
    
    with col1:
        url_input = st.text_input(
            "🔗 Enter Job Posting URL:",
            value="https://jobs.nike.com/job/R-33460",
            help="Paste the complete URL of the job posting you're interested in"
        )
    
    with col2:
        submit_button = st.button("Generate Email 📨", type="primary")
        
    # Progress tracking
    if submit_button:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Update progress: Starting
            progress_bar.progress(10)
            status_text.text("Starting process...")
            time.sleep(0.5)
            
            # Load and process URL
            status_text.text("Loading job posting...")
            loader = WebBaseLoader(
                [url_input],
                header_template={"User-Agent": os.environ["USER_AGENT"]}
            )
            raw_data = loader.load()
            progress_bar.progress(30)
            
            if not raw_data:
                st.error("❌ No data could be loaded from the URL.")
                return
            
            # Clean and process text
            status_text.text("Processing job details...")
            data = clean_text(raw_data[0].page_content)
            progress_bar.progress(50)
            
            # Load portfolio
            status_text.text("Loading portfolio data...")
            portfolio.load_portfolio()
            progress_bar.progress(70)
            
            # Extract jobs
            status_text.text("Analyzing job requirements...")
            jobs = llm.extract_jobs(data)
            progress_bar.progress(90)
            
            if not jobs:
                st.warning("⚠️ No job information could be extracted from the provided URL.")
                return
            
            # Process each job
            status_text.text("Generating email...")
            progress_bar.progress(95)
            
            # Create tabs for multiple jobs if present
            if len(jobs) > 1:
                tabs = st.tabs([f"Job {i+1}" for i in range(len(jobs))])
            else:
                tabs = [st.container()]
            
            for i, (job, tab) in enumerate(zip(jobs, tabs)):
                with tab:
                    # Show job details
                    show_job_details(job)
                    
                    # Get matching portfolio links
                    skills = job.get('skills', [])
                    if not skills:
                        st.warning("⚠️ No skills were extracted from the job posting.")
                        continue
                    
                    links = portfolio.query_links(skills)
                    
                    # Generate and display email
                    try:
                        email = llm.write_mail(job, links)
                        safe_email = safe_format_text(email)
                        
                        st.markdown("### 📨 Generated Email")
                        st.code(safe_email, language='markdown')
                        
                        # Add copy and download buttons
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            if st.button("📋 Copy Email", key=f"copy_{i}"):
                                st.toast("📋 Email copied to clipboard!")
                        with col2:
                            if st.button("💾 Download Email", key=f"download_{i}"):
                                st.download_button(
                                    label="💾 Download",
                                    data=safe_email,
                                    file_name="cold_email.txt",
                                    mime="text/plain",
                                    key=f"download_button_{i}"
                                )
                                
                    except Exception as e:
                        st.error(f"❌ Error generating email: {str(e)}")
                        st.exception(e)
                        continue
            
            # Complete progress
            progress_bar.progress(100)
            status_text.text("✅ Process completed successfully!")
            time.sleep(1)
            status_text.empty()
            progress_bar.empty()

        except Exception as e:
            st.error(f"❌ An Error Occurred: {str(e)}")
            st.exception(e)
            st.info("🔄 Please check the URL and try again.")

if __name__ == "__main__":
    # Configure the Streamlit page
    st.set_page_config(
        layout="wide",
        page_title="Cold Email Generator",
        page_icon="📧",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.example.com/help',
            'Report a bug': "https://www.example.com/bug",
            'About': "# Cold Email Generator\nThis app helps you generate personalized cold emails for job applications."
        }
    )
    
    # Add custom CSS
    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;
        }
        .stProgress>div>div {
            background-color: #00ff00;
        }
        .css-1v0mbdj {
            margin-top: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize components
    try:
        chain = Model()
        portfolio = Portfolio()
        create_streamlit_app(chain, portfolio, clean_text)
        
    except Exception as e:
        st.error(f"❌ Failed to initialize application: {str(e)}")
        st.exception(e)