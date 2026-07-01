import os
import json
import streamlit as st
import base64
from datetime import datetime

COUNTER_FILE = "data/visitor_counter.txt"
MESSAGES_FILE = "data/contact_messages.json"
RESUME_FILE = "assets/resume.pdf"

def get_base64_of_bin_file(bin_file):
    """
    Returns the base64 string of a binary file.
    """
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def inject_custom_css():
    """
    Reads the style.css file and injects it into Streamlit's header.
    It also determines the theme (dark or light) and overrides variables at the :root level.
    """
    css_path = "assets/css/style.css"
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        
        # Check active theme in session state
        theme_class = st.session_state.get("theme", "dark-mode")
        
        # Override :root variables based on active theme
        theme_overrides = ""
        if theme_class == "light-mode":
            theme_overrides = """
            <style>
            :root {
                --primary: #0284c7;
                --primary-glow: rgba(2, 132, 199, 0.2);
                --sidebar-bg: #f1f5f9;
                --dark-bg: #f8fafc;
                --card-bg: rgba(255, 255, 255, 0.85);
                --card-border: rgba(2, 132, 199, 0.12);
                --text-color: #0f172a;
                --text-muted: #64748b;
            }
            </style>
            """
        else:
            theme_overrides = """
            <style>
            :root {
                --primary: #0ea5e9;
                --primary-glow: rgba(14, 165, 233, 0.4);
                --sidebar-bg: #0b0f19;
                --dark-bg: #080b11;
                --card-bg: rgba(17, 24, 39, 0.7);
                --card-border: rgba(14, 165, 233, 0.2);
                --text-color: #f8fafc;
                --text-muted: #94a3b8;
            }
            </style>
            """
            
        # Inject standard style sheet and active overrides
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
        st.markdown(theme_overrides, unsafe_allow_html=True)

def increment_visitor_counter():
    """
    Increments a local file-based visitor counter and returns the count.
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(COUNTER_FILE) or '.', exist_ok=True)
    
    count = 0
    if os.path.exists(COUNTER_FILE):
        try:
            with open(COUNTER_FILE, 'r') as f:
                count = int(f.read().strip())
        except ValueError:
            count = 0
            
    count += 1
    
    try:
        with open(COUNTER_FILE, 'w') as f:
            f.write(str(count))
    except Exception:
        pass
        
    return count

def save_contact_message(name, email, message):
    """
    Saves a message submitted via the contact form to a local JSON file.
    """
    os.makedirs(os.path.dirname(MESSAGES_FILE) or '.', exist_ok=True)
    
    new_message = {
        "timestamp": datetime.now().isoformat(),
        "name": name,
        "email": email,
        "message": message
    }
    
    messages = []
    if os.path.exists(MESSAGES_FILE):
        try:
            with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
                messages = json.load(f)
        except Exception:
            messages = []
            
    messages.append(new_message)
    
    try:
        with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

def render_typing_animation(words, speed=100, delay=1500):
    """
    Generates a CSS typing animation for a list of words.
    """
    words_js = json.dumps(words)
    html_content = f"""
    <div style="font-size: 1.5rem; font-weight: 500; min-height: 50px;">
        <span id="typing-text" style="color: var(--primary); font-weight: 700; border-right: 2px solid var(--primary); padding-right: 5px;"></span>
    </div>
    <script>
        (function() {{
            const words = {words_js};
            let wordIndex = 0;
            let charIndex = 0;
            let isDeleting = false;
            const typingText = window.parent.document.getElementById('typing-text') || document.getElementById('typing-text');
            
            function type() {{
                if (!typingText) return;
                const currentWord = words[wordIndex];
                if (isDeleting) {{
                    typingText.textContent = currentWord.substring(0, charIndex - 1);
                    charIndex--;
                }} else {{
                    typingText.textContent = currentWord.substring(0, charIndex + 1);
                    charIndex++;
                }}
                
                let typeSpeed = {speed};
                if (isDeleting) {{
                    typeSpeed /= 2;
                }}
                
                if (!isDeleting && charIndex === currentWord.length) {{
                    typeSpeed = {delay};
                    isDeleting = true;
                }} else if (isDeleting && charIndex === 0) {{
                    isDeleting = false;
                    wordIndex = (wordIndex + 1) % words.length;
                    typeSpeed = 500;
                }}
                
                setTimeout(type, typeSpeed);
            }}
            setTimeout(type, 500);
        }})();
    </script>
    """
    # Dynamic colors based on active theme
    is_dark = st.session_state.get("theme", "dark-mode") == "dark-mode"
    text_color = "#f8fafc" if is_dark else "#0f172a"
    muted_color = "#94a3b8" if is_dark else "#64748b"
    primary_color = "#0ea5e9" if is_dark else "#0284c7"

    import streamlit.components.v1 as components
    components.html(
        f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700&display=swap');
                body {{
                    font-family: 'Outfit', sans-serif;
                    margin: 0;
                    padding: 0;
                    background: transparent;
                    color: {text_color};
                }}
                .cursor {{
                    animation: blink 0.75s step-end infinite;
                }}
                @keyframes blink {{
                    from, to {{ border-color: transparent }}
                    50% {{ border-color: {primary_color} }}
                }}
            </style>
        </head>
        <body>
            <div style="font-size: 1.5rem; font-weight: 500;">
                <span id="typing-text" style="color: {primary_color}; font-weight: 700; border-right: 2px solid {primary_color}; padding-right: 5px;" class="cursor"></span>
            </div>
            <script>
                const words = {words_js};
                let wordIndex = 0;
                let charIndex = 0;
                let isDeleting = false;
                const typingText = document.getElementById('typing-text');
                
                function type() {{
                    const currentWord = words[wordIndex];
                    if (isDeleting) {{
                        typingText.textContent = currentWord.substring(0, charIndex - 1);
                        charIndex--;
                    }} else {{
                        typingText.textContent = currentWord.substring(0, charIndex + 1);
                        charIndex++;
                    }}
                    
                    let typeSpeed = 100;
                    if (isDeleting) {{
                        typeSpeed = 50;
                    }}
                    
                    if (!isDeleting && charIndex === currentWord.length) {{
                        typeSpeed = 2000; // Pause at end of word
                        isDeleting = true;
                    }} else if (isDeleting && charIndex === 0) {{
                        isDeleting = false;
                        wordIndex = (wordIndex + 1) % words.length;
                        typeSpeed = 300;
                    }}
                    
                    setTimeout(type, typeSpeed);
                }}
                document.addEventListener("DOMContentLoaded", function() {{
                    setTimeout(type, 1000);
                }});
            </script>
        </body>
        </html>
        """,
        height=60
    )

def load_resume_bytes():
    """
    Returns the bytes of the resume for the download button.
    If the file does not exist, it will auto-generate a sample/placeholder PDF.
    """
    # Ensure assets directory exists
    os.makedirs("assets", exist_ok=True)
    
    if not os.path.exists(RESUME_FILE):
        # We can write a simple placeholder text file and name it as PDF or a small basic PDF string
        # Let's write a simple PDF file to satisfy downloading.
        # Below is a valid, very basic 1-page PDF file structure:
        pdf_content = (
            b"%PDF-1.4\n"
            b"1 0 obj <</Type/Catalog/Pages 2 0 R>> endobj\n"
            b"2 0 obj <</Type/Pages/Kids[3 0 R]/Count 1>> endobj\n"
            b"3 0 obj <</Type/Page/Parent 2 0 R/MediaBox[0 0 595 842]/Contents 4 0 R/Resources<</Font<</F1 5 0 R>>>>>> endobj\n"
            b"4 0 obj <</Length 73>> stream\n"
            b"BT\n/F1 24 Tf\n100 700 Td\n(Nitish Kumar Khavekar - Resume Placeholder) Tj\nET\n"
            b"endstream\nendobj\n"
            b"5 0 obj <</Type/Font/Subtype/Type1/BaseFont/Helvetica>> endobj\n"
            b"xref\n0 6\n0000000000 65535 f\n0000000009 00000 n\n0000000056 00000 n\n0000000111 00000 n\n0000000212 00000 n\n0000000334 00000 n\n"
            b"trailer <</Size 6/Root 1 0 R>>\n"
            b"startxref\n412\n%%EOF\n"
        )
        try:
            with open(RESUME_FILE, 'wb') as f:
                f.write(pdf_content)
        except Exception:
            pass
            
    try:
        with open(RESUME_FILE, 'rb') as f:
            return f.read()
    except Exception:
        return b"Sample resume contents."
