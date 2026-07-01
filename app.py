import streamlit as st
import os
import json
from datetime import datetime
from streamlit_option_menu import option_menu

# Import utility modules
from utils.helpers import inject_custom_css, increment_visitor_counter, get_base64_of_bin_file
from utils.github_api import fetch_github_profile

# Import page modules
from pages import Home, Projects, Skills, Education, Certificates, GitHub, LinkedIn, Contact, Internship

# 1. Page Configuration
st.set_page_config(
    page_title="Nitish Kumar Khavekar | Data Analyst & AI Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Setup Session State (Visitor Count & Theme)
if "visitor_count" not in st.session_state:
    st.session_state["visitor_count"] = increment_visitor_counter()
    
if "theme" not in st.session_state:
    st.session_state["theme"] = "dark-mode"

# Anchor for Back-to-Top
st.markdown("<div id='top'></div>", unsafe_allow_html=True)

# 3. Inject CSS
inject_custom_css()

# 4. Load Personal Bio Info for Sidebar
try:
    with open("data/contact.json", "r", encoding="utf-8") as f:
        contact_info = json.load(f)
except Exception:
    contact_info = {
        "full_name": "NITISHKUMAR KHAVEKAR",
        "title": "Data Analyst & AI/ML Engineer",
        "email": "khavekarnitishkumar@gmail.com",
        "linkedin_url": "https://linkedin.com/in/nitishkumarkhavekar",
        "github_url": "https://github.com/Nitishkumarkhavekar"
    }

# 5. Render Sidebar
with st.sidebar:
    # Profile Picture
    st.markdown('<div class="profile-container">', unsafe_allow_html=True)
    profile_path = "assets/profile.png"
    if os.path.exists(profile_path):
        try:
            img_base64 = get_base64_of_bin_file(profile_path)
            st.markdown(
                f'<img src="data:image/png;base64,{img_base64}" class="profile-img" width="130" height="130" style="margin-bottom: 0.8rem;">',
                unsafe_allow_html=True
            )
        except Exception:
            st.image("https://avatars.githubusercontent.com/u/169582171?v=4", width=130)
    else:
        st.image("https://avatars.githubusercontent.com/u/169582171?v=4", width=130)
        
    st.markdown(
        f"""
        <h3 style="text-align: center; margin-top: 0.5rem; margin-bottom: 0; font-size: 1.25rem; font-weight: 700; color: var(--text-color);">
            {contact_info['full_name']}
        </h3>
        <p style="text-align: center; color: var(--primary); font-size: 0.85rem; font-weight: 600; margin-top: 0.2rem; margin-bottom: 1.5rem;">
            {contact_info['title']}
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar Navigation Menu
    menu_options = [
        "Home", 
        "Projects", 
        "Internship", 
        "Skills", 
        "Education", 
        "Certificates", 
        "GitHub", 
        "LinkedIn", 
        "Contact"
    ]
    
    menu_icons = [
        "house", 
        "folder-fill", 
        "briefcase-fill", 
        "lightning-charge-fill", 
        "mortarboard-fill", 
        "award-fill", 
        "github", 
        "linkedin", 
        "envelope-fill"
    ]
    
    selected_page = option_menu(
        menu_title="Navigation",
        options=menu_options,
        icons=menu_icons,
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "var(--primary)", "font-size": "1rem"},
            "nav-link": {
                "font-size": "0.95rem", 
                "text-align": "left", 
                "margin": "0px", 
                "color": "var(--text-color)",
                "--hover-color": "rgba(0, 173, 181, 0.1)"
            },
            "nav-link-selected": {"background-color": "var(--primary)", "color": "white"},
        }
    )
    
    st.markdown("<hr style='border-color: var(--card-border); margin: 1.5rem 0 1rem 0;'>", unsafe_allow_html=True)
    
    # Theme Toggle Switcher
    st.markdown("<div style='text-align: center; margin-bottom: 1rem;'>", unsafe_allow_html=True)
    theme_label = "☀️ Light Mode" if st.session_state.theme == "dark-mode" else "🌙 Dark Mode"
    if st.button(theme_label, key="theme_toggle", use_container_width=True):
        if st.session_state.theme == "dark-mode":
            st.session_state.theme = "light-mode"
        else:
            st.session_state.theme = "dark-mode"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# 6. Render the Selected Page Content
st.markdown("<div class='main-content'>", unsafe_allow_html=True)

if selected_page == "Home":
    Home.show()
elif selected_page == "Projects":
    Projects.show()
elif selected_page == "Internship":
    Internship.show()
elif selected_page == "Skills":
    Skills.show()
elif selected_page == "Education":
    Education.show()
elif selected_page == "Certificates":
    Certificates.show()
elif selected_page == "GitHub":
    GitHub.show()
elif selected_page == "LinkedIn":
    LinkedIn.show()
elif selected_page == "Contact":
    Contact.show()

st.markdown("</div>", unsafe_allow_html=True)

# 7. Shared Footer Component
st.markdown(
    f"""
    <div class="footer-container">
        <div class="footer-social-links">
            <a href="{contact_info['linkedin_url']}" target="_blank">🔗 LinkedIn</a>
            <a href="{contact_info['github_url']}" target="_blank">💻 GitHub</a>
            <a href="mailto:{contact_info['email']}">📧 Email</a>
        </div>
        <p style="font-size: 0.8rem; color: var(--primary); font-weight: 500; margin-bottom: 1.5rem;">
            Profile visits: {st.session_state['visitor_count']}
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Render a modern, styled scroll to top button in the footer
# We use standard HTML scroll code pointing to top
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 2rem;">
        <a href="#top" style="text-decoration: none;">
            <button style="border: 1px solid var(--primary); border-radius: 6px; padding: 0.4rem 1rem; background: transparent; color: var(--primary); font-weight: 600; cursor: pointer; transition: all 0.3s ease;">
                ▲ Back to Top
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
