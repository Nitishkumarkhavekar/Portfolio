import streamlit as st
import datetime
from utils.project_loader import load_all_projects
from utils.helpers import get_base64_of_bin_file
import os

def show():
    st.markdown("<h2>📂 My Projects</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-muted); margin-bottom: 2rem;'>A collection of local analytics, reporting, and AI projects, merged with live GitHub statistics.</p>", unsafe_allow_html=True)
    
    # 1. Load projects with a spinner
    with st.spinner("Fetching and merging projects information..."):
        all_projects = load_all_projects()
        
    if not all_projects:
        st.warning("No projects found.")
        return
        
    # 2. Extract unique technologies for the filter dropdown
    unique_techs = set()
    for proj in all_projects:
        for tech in proj.get("technologies", []):
            unique_techs.add(tech)
    sorted_techs = sorted(list(unique_techs))
    
    # 3. Control Panel (Search, Filter, Sort) in a glass-card
    st.markdown("<div class='glass-card' style='padding: 1.2rem; margin-bottom: 2rem;'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1.5, 1.2, 1], gap="medium")
    
    with c1:
        search_query = st.text_input("🔍 Search Projects", placeholder="Type project name, description or technologies...")
        
    with c2:
        selected_techs = st.multiselect("🛠️ Filter by Technology", options=sorted_techs)
        
    with c3:
        sort_by = st.selectbox("↕️ Sort by", options=["Latest", "GitHub Stars", "Alphabetical"])
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 4. Filter logic
    filtered_projects = []
    for proj in all_projects:
        # Search matching (case-insensitive)
        search_text = (proj["name"] + " " + proj["description"] + " " + " ".join(proj["technologies"])).lower()
        if search_query and search_query.lower() not in search_text:
            continue
            
        # Tech filter matching (all selected must be present, or if none selected)
        if selected_techs and not all(t in proj["technologies"] for t in selected_techs):
            continue
            
        filtered_projects.append(proj)
        
    # 5. Sorting logic
    def get_sort_key(proj):
        w = proj.get("weight", 0)
        if sort_by == "Alphabetical":
            return (w, proj["name"].lower(), 0.0)
        elif sort_by == "GitHub Stars":
            return (w, -proj.get("stars", 0), proj["name"].lower())
        else:  # "Latest"
            # Sort by last updated timestamp. Parse iso date or fallback to epoch
            updated_str = proj.get("last_updated")
            if updated_str:
                try:
                    # Strip Z and milliseconds if needed, or parse directly
                    clean_str = updated_str.replace("Z", "+00:00")
                    dt = datetime.datetime.fromisoformat(clean_str)
                    return (w, -dt.timestamp(), proj["name"].lower())
                except Exception:
                    pass
            # Fallback for projects without timestamp: sort oldest, then alphabetically
            return (w, 0.0, proj["name"].lower())
            
    try:
        filtered_projects.sort(key=get_sort_key)
    except Exception as e:
        st.error(f"⚠️ Project sorting encountered an error: {e}. Falling back to alphabetical listing.")
        # Diagnostic display to pinpoint the exact incompatible project key
        diag_list = []
        for p in filtered_projects:
            try:
                k = get_sort_key(p)
                diag_list.append({
                    "Project Name": p["name"],
                    "Category": p["category"],
                    "Sort Key": str(k),
                    "Key Component Types": str([type(x).__name__ for x in k])
                })
            except Exception as inner_e:
                diag_list.append({
                    "Project Name": p["name"],
                    "Category": p["category"],
                    "Sort Key": f"ERROR: {inner_e}",
                    "Key Component Types": "N/A"
                })
        st.dataframe(diag_list)
        # Safe fallback sort
        filtered_projects.sort(key=lambda x: (x.get("weight", 0), x["name"].lower()))
    
    # 6. Group projects by category
    categories = {
        "📊 Excel": [],
        "📈 Power BI": [],
        "📉 Tableau": [],
        "🐍 Python": [],
        "🤖 AI / Machine Learning": []
    }
    
    for proj in filtered_projects:
        cat = proj.get("category", "🐍 Python")
        if cat in categories:
            categories[cat].append(proj)
        else:
            categories["🐍 Python"].append(proj)
            
    # 7. Render Projects using Streamlit Tabs
    tabs = st.tabs(list(categories.keys()))
    
    for tab_idx, (cat_name, cat_projects) in enumerate(categories.items()):
        with tabs[tab_idx]:
            if not cat_projects:
                st.markdown(
                    f"<div style='text-align: center; color: var(--text-muted); padding: 3rem 0;'>"
                    f"No projects found matching the criteria in {cat_name}."
                    f"</div>",
                    unsafe_allow_html=True
                )
                continue
                
            # Render projects in a grid or stack
            for proj in cat_projects:
                # Render each project card
                render_project_card(proj)

def render_project_card(proj):
    """
    Renders a clean card containing screenshots, metadata, badges, and code links.
    """
    # Build tags HTML
    tags_html = "".join([f'<span class="tag-badge">{t}</span>' for t in proj["technologies"]])
    
    # GitHub stats badges if stars/forks > 0
    github_stats_html = ""
    if proj.get("stars", 0) > 0 or proj.get("forks", 0) > 0:
        github_stats_html = f"""
        <div style="display: flex; gap: 0.8rem; margin-top: 0.5rem; font-size: 0.85rem; color: var(--text-muted); font-weight: 500;">
            <span>⭐ {proj.get('stars')} stars</span>
            <span>🍴 {proj.get('forks')} forks</span>
        </div>
        """
        
    last_updated_html = ""
    if proj.get("last_updated"):
        try:
            date_part = proj["last_updated"][:10]
            last_updated_html = f'<div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.4rem;">📅 Updated: {date_part}</div>'
        except Exception:
            pass
            
    # Clean image logic. If local screenshot exists, render it as base64, otherwise default category icon/bg
    img_tag_html = ""
    screenshot_path = proj.get("screenshot")
    if screenshot_path and os.path.exists(screenshot_path):
        try:
            img_base64 = get_base64_of_bin_file(screenshot_path)
            img_tag_html = f'<img src="data:image/png;base64,{img_base64}" style="width:100%; border-radius: 12px; object-fit: cover; height: 180px; border: 1px solid var(--card-border);" alt="Screenshot">'
        except Exception:
            pass
            
    if not img_tag_html:
        # Fallback category gradients
        gradient_map = {
            "📊 Excel": "linear-gradient(135deg, #1D7044 0%, #107C41 100%)",
            "📈 Power BI": "linear-gradient(135deg, #E6AD12 0%, #F2C811 100%)",
            "📉 Tableau": "linear-gradient(135deg, #1F4E79 0%, #3B7FB9 100%)",
            "🐍 Python": "linear-gradient(135deg, #306998 0%, #FFD43B 100%)",
            "🤖 AI / Machine Learning": "linear-gradient(135deg, #0052D4 0%, #4364F7 50%, #6FB1FC 100%)"
        }
        grad = gradient_map.get(proj["category"], "linear-gradient(135deg, #00ADB5 0%, #393E46 100%)")
        cat_icon = proj["category"].split()[0]
        
        img_tag_html = f"""<div style="width: 100%; height: 180px; background: {grad}; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 4rem; box-shadow: inset 0 0 40px rgba(0,0,0,0.15); border: 1px solid var(--card-border);">{cat_icon}</div>"""
        
    st.markdown(
        f"""<div class="glass-card" style="margin-bottom: 1.5rem;">
<div style="display: flex; gap: 1.5rem; flex-wrap: wrap; align-items: flex-start;">
<div style="flex: 1 1 200px; max-width: 250px;">
{img_tag_html}
</div>
<div style="flex: 2 2 400px; display: flex; flex-direction: column; justify-content: space-between;">
<div>
<div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 0.5rem; flex-wrap: wrap;">
<h3 style="margin: 0; font-size: 1.4rem; color: var(--text-color); font-weight: 700;">{proj['name']}</h3>
<span class="tag-badge" style="background: rgba(14, 165, 233, 0.1); border: 1px solid rgba(14,165,233,0.25); color: var(--primary); margin: 0; padding: 0.2rem 0.6rem; font-size: 0.8rem; font-weight: 600;">{proj['category']}</span>
</div>
{github_stats_html}
<p style="margin: 0.8rem 0; font-size: 0.98rem; line-height: 1.5; color: var(--text-muted);">{proj['description']}</p>
<div style="margin: 0.8rem 0 0.5rem 0;">{tags_html}</div>
{last_updated_html}
</div>
</div>
</div>
</div>""",
        unsafe_allow_html=True
    )
    
    # Render interactive button triggers for GitHub and Live Demo using streamlit buttons side-by-side
    bcol1, bcol2, _ = st.columns([1, 1, 2], gap="small")
    
    with bcol1:
        if proj.get("github_url"):
            st.markdown(
                f'<a href="{proj["github_url"]}" target="_blank" style="text-decoration: none;"><button style="width: 100%; border: none; border-radius: 6px; padding: 0.5rem; background: var(--secondary); color: var(--text-color); font-weight: 600; cursor: pointer; transition: background 0.2s;">💻 View Code</button></a>',
                unsafe_allow_html=True
            )
        else:
            st.markdown('<button style="width: 100%; border: none; border-radius: 6px; padding: 0.5rem; background: var(--card-border); color: var(--text-muted); font-weight: 600; cursor: not-allowed;" disabled>🔒 Private</button>', unsafe_allow_html=True)
            
    with bcol2:
        if proj.get("demo_url"):
            st.markdown(
                f'<a href="{proj["demo_url"]}" target="_blank" style="text-decoration: none;"><button style="width: 100%; border: none; border-radius: 6px; padding: 0.5rem; background: var(--primary); color: white; font-weight: 600; cursor: pointer; transition: background 0.2s;">🚀 Live Demo</button></a>',
                unsafe_allow_html=True
            )
            
    st.markdown("<br>", unsafe_allow_html=True)
