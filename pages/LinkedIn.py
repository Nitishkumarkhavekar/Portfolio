import streamlit as st
import json

def show():
    # Load contact/linkedin URL details
    with open("data/contact.json", "r", encoding="utf-8") as f:
        contact_data = json.load(f)
        
    st.markdown("<h2>💼 LinkedIn Integration</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-muted); margin-bottom: 2rem;'>Connect with me on LinkedIn to discuss analytics opportunities, machine learning research, or technical collaboration.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5], gap="large")
    
    with col1:
        # Mock LinkedIn Profile Badge View
        st.markdown(
            f"""<div class="glass-card" style="text-align: center; padding: 2rem 1.5rem; border-top: 5px solid #0077B5;">
<div style="background: #0077B5; color: white; display: inline-block; padding: 0.2rem 0.6rem; border-radius: 4px; font-weight: 700; font-size: 0.8rem; margin-bottom: 1rem;">in</div>
<div style="margin-bottom: 1rem;">
<img src="https://avatars.githubusercontent.com/u/169582171?v=4" style="border-radius: 50%; width: 100px; height: 100px; border: 2px solid #0077B5;" alt="Profile Picture">
</div>
<h3 style="margin: 0; font-size: 1.25rem; color: var(--text-color);">{contact_data['full_name']}</h3>
<p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.3rem; line-height: 1.4;">{contact_data['title']}</p>
<p style="font-size: 0.8rem; color: var(--primary); margin-top: 0.4rem; font-weight: 500;">📍 {contact_data['location']}</p>
<hr style="border-color: var(--card-border); margin: 1rem 0;">
<div style="font-size: 0.8rem; color: var(--text-muted); display: flex; justify-content: space-around;">
<div>
<div style="font-weight: 700; color: var(--text-color);">500+</div>
<div>connections</div>
</div>
</div>
</div>""",
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        # Visit LinkedIn button
        st.markdown(
            f'<a href="{contact_data["linkedin_url"]}" target="_blank" style="text-decoration: none;"><button style="width: 100%; border: none; border-radius: 6px; padding: 0.6rem; background: #0077B5; color: white; font-weight: 600; cursor: pointer; transition: background 0.2s;">Visit LinkedIn ↗</button></a>',
            unsafe_allow_html=True
        )
        
    with col2:
        st.markdown("<h3>Professional Summary</h3>", unsafe_allow_html=True)
        st.markdown(
            f"""<div class="glass-card">
<p style="font-size: 1rem; line-height: 1.6; color: var(--text-color);">
I regularly share insights about data analytics pipelines, dashboard designs, Python frameworks, and AI application breakthroughs. 
<br><br>
<b>What we can discuss:</b>
<ul style="margin-top: 0.5rem; padding-left: 1.2rem; color: var(--text-muted); line-height: 1.6;">
<li>Deploying business intelligence solutions in Power BI & Tableau</li>
<li>Building custom machine learning classification/regression models</li>
<li>Creating LLM chatbots and agentic workflows</li>
<li>Data manipulation, preprocessing, and ETL pipelines</li>
</ul>
</p>
</div>""",
            unsafe_allow_html=True
        )
        
        st.info("💡 Note: The LinkedIn URL displayed here is fully configurable. You can update it anytime in data/contact.json.")
