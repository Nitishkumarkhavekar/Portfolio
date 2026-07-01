import streamlit as st
import json

def show():
    # Load education data
    with open("data/education.json", "r", encoding="utf-8") as f:
        education_data = json.load(f)
        
    st.markdown("<h2>🎓 Education Journey</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-muted); margin-bottom: 2rem;'>Here is a timeline summary of my academic history, achievements, and qualifications.</p>", unsafe_allow_html=True)
    
    # Create HTML Timeline structure
    timeline_html = '<div class="timeline">'
    
    for item in education_data:
        timeline_html += f"""<div class="timeline-item">
<div class="timeline-dot"></div>
<div class="timeline-date">{item['year']}</div>
<div class="glass-card" style="margin-left: 0.5rem; margin-top: 0.5rem;">
<div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 0.5rem;">
<h3 style="margin: 0; color: var(--text-color); font-size: 1.25rem;">{item['degree']}</h3>
<span class="tag-badge" style="margin: 0; padding: 0.3rem 0.8rem; font-size: 0.85rem;">🏆 {item['grade']}</span>
</div>
<div style="font-weight: 500; color: var(--primary); margin-top: 0.4rem; font-size: 1rem;">
🏫 {item['college']}
</div>
<div style="font-size: 0.9rem; color: var(--text-muted); margin-top: 0.2rem; font-style: italic;">
🏛️ {item['university']}
</div>
<p style="margin-top: 0.8rem; margin-bottom: 0; font-size: 0.95rem; line-height: 1.5; color: var(--text-muted);">
{item['description']}
</p>
</div>
</div>"""
        
    timeline_html += '</div>'
    
    st.markdown(timeline_html, unsafe_allow_html=True)
