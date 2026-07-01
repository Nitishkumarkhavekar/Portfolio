import streamlit as st
import json

def show():
    # Load internship data
    with open("data/internship.json", "r", encoding="utf-8") as f:
        internships = json.load(f)
        
    st.markdown("<h2>💼 Internship Experience</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-muted); margin-bottom: 2rem;'>Here is a summary of my industrial training, hands-on project roles, and developer internships.</p>", unsafe_allow_html=True)
    
    for idx, job in enumerate(internships):
        # Build highlights list
        bullets_html = ""
        for item in job.get("highlights", []):
            bullets_html += f"<li>{item}</li>"
            
        # Draw card in HTML without leading indentation spaces to prevent Markdown code block bugs
        st.markdown(
            f"""<div class="glass-card" style="margin-bottom: 1.5rem;">
<div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 0.5rem; flex-wrap: wrap;">
<h3 style="margin: 0; font-size: 1.3rem; color: var(--text-color); font-weight: 700;">{job['role']}</h3>
<span class="tag-badge" style="background: rgba(14, 165, 233, 0.1); border: 1px solid rgba(14,165,233,0.25); color: var(--primary); margin: 0; padding: 0.25rem 0.75rem; font-size: 0.8rem; font-weight: 600;">📅 {job['duration']}</span>
</div>
<div style="font-weight: 600; color: var(--primary); font-size: 1rem; margin-top: 0.4rem;">
🏢 {job['company']} <span style="color: var(--text-muted); font-weight: 400; font-size: 0.9rem; margin-left: 0.5rem;">📍 {job['location']}</span>
</div>
<p style="margin: 0.8rem 0; font-size: 0.98rem; line-height: 1.5; color: var(--text-color);">{job['description']}</p>
<ul style="margin-top: 0.5rem; padding-left: 1.2rem; line-height: 1.6; color: var(--text-muted); font-size: 0.95rem;">
{bullets_html}
</ul>
</div>""",
            unsafe_allow_html=True
        )
