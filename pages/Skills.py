import streamlit as st
import json
import plotly.graph_objects as go

def show():
    # Load skills data
    with open("data/skills.json", "r", encoding="utf-8") as f:
        skills_data = json.load(f)
        
    st.markdown("<h2>⚡ Skills & Proficiencies</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-muted); margin-bottom: 2rem;'>Here is a summary of my technical toolkit, analytical expertise, and programming capabilities.</p>", unsafe_allow_html=True)
    
    # 1. Plotly Chart - Visualizing Skills Categories Summary
    # Compute averages for each category
    categories = list(skills_data.keys())
    averages = []
    for cat in categories:
        lvl_sum = sum(skill["level"] for skill in skills_data[cat])
        averages.append(lvl_sum / len(skills_data[cat]))
        
    # Radar Chart or Polar Chart for nice visualization
    fig = go.Figure()
    
    # Check theme color in session state to make chart blend beautifully
    is_dark = st.session_state.get("theme", "dark-mode") == "dark-mode"
    bg_color = "rgba(0,0,0,0)"
    grid_color = "rgba(255, 255, 255, 0.1)" if is_dark else "rgba(0, 0, 0, 0.08)"
    text_color = "#f8fafc" if is_dark else "#0f172a"
    primary_color = "#0ea5e9" if is_dark else "#0284c7"
    fill_color = "rgba(14, 165, 233, 0.25)" if is_dark else "rgba(2, 132, 199, 0.2)"
    
    fig.add_trace(go.Scatterpolar(
        r=averages + [averages[0]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor=fill_color,
        line=dict(color=primary_color, width=3),
        name='Averages'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor=grid_color,
                color=text_color,
                tickfont=dict(size=10)
            ),
            angularaxis=dict(
                gridcolor=grid_color,
                color=text_color,
                tickfont=dict(size=12, family="Outfit")
            ),
            bgcolor=bg_color
        ),
        showlegend=False,
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        margin=dict(l=40, r=40, t=30, b=30),
        height=320
    )
    
    # 2 Columns: Left is Radar chart, Right is category listing summary
    col_chart, col_desc = st.columns([1.2, 1], gap="medium")
    with col_chart:
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
    with col_desc:
        st.markdown(
            """
            <div class="glass-card" style="height: 90%; display: flex; flex-direction: column; justify-content: center;">
                <h3 style="margin-top: 0; color: var(--primary);">Skills Mapping</h3>
                <p style="font-size: 0.95rem; line-height: 1.5; color: var(--text-muted); margin-bottom: 0;">
                    My technical expertise is divided into four key domain areas: Data Analytics, Core Programming, Advanced AI/ML modeling, and supporting Tools. 
                    <br><br>
                    The radar diagram shows my overall proficiency profile. I am highly comfortable with Python scripting, SQL data modeling, and designing business intelligence dashboards in Excel and Power BI.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Render categories and skills in a 2x2 grid
    cats = list(skills_data.keys())
    
    row1_col1, row1_col2 = st.columns(2, gap="large")
    row2_col1, row2_col2 = st.columns(2, gap="large")
    
    # Map columns
    grid_cols = [row1_col1, row1_col2, row2_col1, row2_col2]
    
    icons = {
        "Data Analytics": "📊",
        "Programming": "🐍",
        "AI/ML": "🤖",
        "Tools": "🛠️"
    }
    
    for idx, cat_name in enumerate(cats):
        with grid_cols[idx]:
            icon = icons.get(cat_name, "⚡")
            
            # Start Category Card
            card_html = f"""<div class="glass-card" style="height: 100%;">
<h3 style="margin-top: 0; color: var(--primary); display: flex; align-items: center; gap: 0.5rem;">
<span>{icon}</span> {cat_name}
</h3>
<div style="margin-top: 1.2rem;">"""
            
            # Append skill bars
            for s in skills_data[cat_name]:
                card_html += f"""<div class="skill-bar-container">
<div class="skill-info">
<span style="color: var(--text-color); font-size: 0.95rem;">{s['name']}</span>
<span style="color: var(--primary); font-size: 0.95rem;">{s['level']}%</span>
</div>
<div class="skill-bar-bg">
<div class="skill-bar-fill" style="width: {s['level']}%;"></div>
</div>
</div>"""
                
            card_html += """</div></div>"""
            st.markdown(card_html, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
