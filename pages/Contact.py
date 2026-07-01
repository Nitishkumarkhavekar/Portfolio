import streamlit as st
import json
from utils.helpers import save_contact_message

def show():
    # Load contact information
    with open("data/contact.json", "r", encoding="utf-8") as f:
        contact_data = json.load(f)
        
    st.markdown("<h2>📬 Contact Details</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-muted); margin-bottom: 2rem;'>Let's connect! Feel free to reach out using the contact details below, or send me a message directly through the form.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.2], gap="large")
    
    with col1:
        st.markdown("<h3>Get In Touch</h3>", unsafe_allow_html=True)
        
        # Grid of contact detail rows
        details = [
            {"icon": "👤", "label": "Full Name", "value": contact_data["full_name"], "url": None},
            {"icon": "📧", "label": "Email", "value": contact_data["email"], "url": f"mailto:{contact_data['email']}"},
            {"icon": "📞", "label": "Phone Number", "value": contact_data["phone"], "url": f"tel:{contact_data['phone']}"},
            {"icon": "📍", "label": "Location", "value": contact_data["location"], "url": None},
            {"icon": "💼", "label": "LinkedIn", "value": "LinkedIn Profile", "url": contact_data["linkedin_url"]},
            {"icon": "💻", "label": "GitHub", "value": "Nitishkumarkhavekar", "url": contact_data["github_url"]},
            {"icon": "🌐", "label": "Portfolio Website", "value": "nitishkumarkhavekar.github.io", "url": contact_data["website_url"]}
        ]
        
        for item in details:
            val_html = item["value"]
            if item["url"]:
                val_html = f'<a href="{item["url"]}" target="_blank" style="color: var(--primary); text-decoration: none; font-weight: 500;">{item["value"]} ↗</a>'
                
            st.markdown(
                f"""
                <div class="glass-card" style="padding: 1rem; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 1rem;">
                    <div style="font-size: 1.8rem; line-height: 1;">{item['icon']}</div>
                    <div>
                        <div style="font-size: 0.8rem; color: var(--text-muted); font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">{item['label']}</div>
                        <div style="font-size: 1rem; color: var(--text-color); margin-top: 2px;">{val_html}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
    with col2:
        st.markdown("<h3>Send a Message</h3>", unsafe_allow_html=True)
        
        with st.form("contact_form", clear_on_submit=True):
            name = st.text_input("Your Name", placeholder="Enter your full name")
            email = st.text_input("Your Email", placeholder="Enter your email address")
            message = st.text_area("Your Message", placeholder="Type your message here...", height=150)
            
            submit_button = st.form_submit_button("Send Message 🚀")
            
            if submit_button:
                if not name.strip():
                    st.error("Please enter your name.")
                elif not email.strip() or "@" not in email:
                    st.error("Please enter a valid email address.")
                elif not message.strip():
                    st.error("Please enter a message.")
                else:
                    success = save_contact_message(name, email, message)
                    if success:
                        st.success("Thank you! Your message has been saved successfully. I will get back to you soon.")
                        # Show notification
                        st.balloons()
                    else:
                        st.error("Failed to save the message. Please try again.")
                        
    # Custom CSS fix for clickable links in cards
    st.markdown(
        """
        <style>
            a:hover {
                text-decoration: underline !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
