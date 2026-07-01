import streamlit as st
import json

def show():
    # Load certificates data
    with open("data/certificates.json", "r", encoding="utf-8") as f:
        certs_data = json.load(f)
        
    st.markdown("<h2>🏅 Certifications & Badges</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-muted); margin-bottom: 2rem;'>Professional certifications and courses validating my data analysis, machine learning, and AI capabilities.</p>", unsafe_allow_html=True)
    
    # Grid layout: 2 columns for larger screens
    col1, col2 = st.columns(2, gap="large")
    cols = [col1, col2]
    
    for idx, cert in enumerate(certs_data):
        target_col = cols[idx % 2]
        
        # Build skills list
        skills_html = ""
        for skill in cert.get("skills", []):
            skills_html += f'<span class="tag-badge" style="font-size: 0.75rem; margin-right: 0.3rem; margin-bottom: 0.3rem; padding: 0.2rem 0.5rem;">{skill}</span>'
            
        # Draw card in HTML
        with target_col:
            st.markdown(
                f"""<div class="glass-card" style="height: 230px; display: flex; flex-direction: column; justify-content: space-between; margin-bottom: 1.5rem;">
<div>
<div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 0.5rem;">
<h3 style="margin: 0; font-size: 1.15rem; color: var(--text-color); font-weight: 700; line-height: 1.4;">{cert['name']}</h3>
<span style="font-size: 0.8rem; color: var(--text-muted); white-space: nowrap; font-weight: 500;">📅 {cert['date']}</span>
</div>
<div style="font-weight: 600; color: var(--primary); font-size: 0.95rem; margin-top: 0.4rem;">
🏫 {cert['organization']}
</div>
<div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">
ID: {cert.get('credential_id', 'N/A')}
</div>
<div style="margin-top: 0.8rem;">
{skills_html}
</div>
</div>
</div>""",
                unsafe_allow_html=True
            )
            
            # Interactive Streamlit Link Button
            link_val = cert.get("link")
            if link_val:
                import os
                if os.path.exists(link_val):
                    with open(link_val, "rb") as f:
                        pdf_bytes = f.read()
                    st.download_button(
                        label="📥 Download Certificate",
                        data=pdf_bytes,
                        file_name=os.path.basename(link_val),
                        mime="application/pdf",
                        key=f"cert_dl_{idx}",
                        use_container_width=True
                    )
                else:
                    st.markdown(
                        f'<a href="{link_val}" target="_blank" style="text-decoration: none;"><button style="width: 100%; border: none; border-radius: 6px; padding: 0.5rem; background: var(--primary); color: white; font-weight: 600; cursor: pointer; transition: background 0.2s;">View Certificate ↗</button></a>',
                        unsafe_allow_html=True
                    )
                
            st.markdown("<br><br>", unsafe_allow_html=True)
