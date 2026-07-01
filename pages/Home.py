import streamlit as st
import json
import os
from PIL import Image
from utils.helpers import render_typing_animation, load_resume_bytes, get_base64_of_bin_file
from utils.github_api import fetch_github_profile

def show():
    # Load contact/bio data
    with open("data/contact.json", "r", encoding="utf-8") as f:
        contact_data = json.load(f)
        
    # Title / Top Introduction
    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 1rem;">
            <h1 style="font-size: 3rem; margin-bottom: 0;">
                Hey there! I'm <span class="text-gradient">{contact_data['full_name']}</span> 👋
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Typing animation
    roles = [
        "Data Analyst",
        "AI/ML Engineer",
        "Business Intelligence Developer",
        "Python Programmer"
    ]
    render_typing_animation(roles)
    
    # 2 Column layout for Image and Bio
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.markdown('<div class="profile-container">', unsafe_allow_html=True)
        profile_path = "assets/profile.png"
        if os.path.exists(profile_path):
            try:
                # Render profile photo in circular frame with shadow
                img_base64 = get_base64_of_bin_file(profile_path)
                st.markdown(
                    f'<img src="data:image/png;base64,{img_base64}" class="profile-img" width="220" height="220" alt="Profile">',
                    unsafe_allow_html=True
                )
            except Exception:
                st.image("https://avatars.githubusercontent.com/u/169582171?v=4", width=220)
        else:
            st.image("https://avatars.githubusercontent.com/u/169582171?v=4", width=220)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown(
            f"""
            <div class="glass-card">
                <h3>About Me</h3>
                <p style="font-size: 1.05rem; line-height: 1.6; color: var(--text-color);">
                    {contact_data['bio']}
                </p>
                <h4 style="margin-top: 1.5rem; margin-bottom: 0.5rem; color: var(--primary);">Career Objective</h4>
                <p style="font-size: 1.02rem; line-height: 1.5; color: var(--text-muted);">
                    {contact_data['objective']}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Download Resume button
        resume_data = load_resume_bytes()
        st.download_button(
            label="📄 Download Resume",
            data=resume_data,
            file_name="Nitishkumar_ML_Resume.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        
    # Separator
    st.markdown("<hr style='border-color: var(--card-border); margin: 2rem 0;'>", unsafe_allow_html=True)
    
    # Portfolio Stats Metrics
    st.markdown("<h3 style='text-align: center; margin-bottom: 1.5rem;'>Portfolio at a Glance</h3>", unsafe_allow_html=True)
    
    # Let's compute details for counters
    # Load certificates count
    try:
        with open("data/certificates.json", "r", encoding="utf-8") as f:
            certs = json.load(f)
            certs_count = len(certs)
    except Exception:
        certs_count = 5
        
    # Get public repo count from github profile api
    github_profile = fetch_github_profile()
    repos_count = github_profile.get("public_repos", 26)
    followers = github_profile.get("followers", 0)
    
    # Load visitor count
    visitor_count = st.session_state.get("visitor_count", 1)
    
    sc1, sc2, sc3, sc4 = st.columns(4, gap="medium")
    with sc1:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-val">{repos_count}</div>
                <div class="stat-lbl">GitHub Repositories</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with sc2:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-val">{certs_count}</div>
                <div class="stat-lbl">Certifications</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with sc3:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-val">{followers}</div>
                <div class="stat-lbl">GitHub Followers</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with sc4:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-val">{visitor_count}</div>
                <div class="stat-lbl">Profile Visits</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    # Quick visual highlights section
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    hc1, hc2 = st.columns(2)
    with hc1:
        st.markdown(
            """
            <div class="glass-card">
                <h4 style="color: var(--primary);"><span style="margin-right: 0.5rem;">📊</span>Data Analytics Focus</h4>
                <p style="font-size: 0.95rem; line-height: 1.5; color: var(--text-muted);">
                    Transforming raw data into clear, actionable business strategies. Expert in modeling data schemas in SQL, designing automated workflows in Excel, and building highly polished Power BI and Tableau dashboards.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with hc2:
        st.markdown(
            """
            <div class="glass-card">
                <h4 style="color: var(--primary);"><span style="margin-right: 0.5rem;">🤖</span>AI & Machine Learning</h4>
                <p style="font-size: 0.95rem; line-height: 1.5; color: var(--text-muted);">
                    Designing state-of-the-art predictive algorithms and LLM-powered RAG chatbots. Proficient in machine learning pipelines, text processing, OCR, and deploying streamlit applications.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
