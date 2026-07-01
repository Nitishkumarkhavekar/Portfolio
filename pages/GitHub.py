import streamlit as st
from utils.github_api import fetch_github_profile, fetch_github_repos
from datetime import datetime

def show():
    st.markdown("<h2>💻 GitHub Profile & Activity</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-muted); margin-bottom: 2rem;'>Live dashboard loading profile statistics and active repositories directly from the GitHub API.</p>", unsafe_allow_html=True)
    
    # 1. Fetch data
    with st.spinner("Connecting to GitHub API..."):
        profile = fetch_github_profile()
        repos = fetch_github_repos()
        
    if not profile:
        st.error("Could not load GitHub profile data.")
        return
        
    # 2. Render Profile Header
    col1, col2 = st.columns([1, 2.5], gap="large")
    
    with col1:
        avatar_url = profile.get("avatar_url", "https://avatars.githubusercontent.com/u/169582171?v=4")
        st.markdown(
            f"""
            <div style="text-align: center;">
                <img src="{avatar_url}" style="border-radius: 50%; border: 4px solid var(--primary); width: 100%; max-width: 180px; box-shadow: 0 0 15px rgba(0, 173, 181, 0.3);" alt="GitHub Avatar">
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f'<a href="{profile.get("html_url")}" target="_blank" style="text-decoration: none;"><button style="width: 100%; border: none; border-radius: 6px; padding: 0.6rem; background: var(--primary); color: white; font-weight: 600; cursor: pointer;">Visit GitHub Profile ↗</button></a>',
            unsafe_allow_html=True
        )
        
    with col2:
        name = profile.get("name", "Nitish Kumar Khavekar")
        bio = profile.get("bio", "Data Analyst & AI Developer")
        location = profile.get("location", "Pune, India")
        company = profile.get("company", "N/A")
        
        st.markdown(
            f"""
            <div class="glass-card" style="height: 100%; margin-bottom: 0;">
                <h3 style="margin-top: 0; color: var(--text-color);">{name or profile.get('login')}</h3>
                <p style="font-size: 0.95rem; font-style: italic; color: var(--text-muted); margin-bottom: 0.8rem;">@{profile.get('login')}</p>
                <p style="font-size: 1rem; color: var(--text-color); line-height: 1.5;">{bio or "No bio available."}</p>
                <div style="margin-top: 1rem; font-size: 0.9rem; color: var(--text-muted); display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
                    <div>📍 Location: {location or "N/A"}</div>
                    <div>🏢 Company: {company or "N/A"}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    # 3. Stats widgets
    st.markdown("<br>", unsafe_allow_html=True)
    sc1, sc2, sc3 = st.columns(3)
    
    # Calculate total stars in fetched repos
    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos)
    
    with sc1:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-val">{profile.get('public_repos', 0)}</div>
                <div class="stat-lbl">Public Repositories</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with sc2:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-val">{profile.get('followers', 0)}</div>
                <div class="stat-lbl">Followers</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with sc3:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-val">{total_stars}</div>
                <div class="stat-lbl">Total Stars Received</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # 4. Repository Search and List
    st.markdown("<h3>Repositories & Projects List</h3>", unsafe_allow_html=True)
    
    repo_search = st.text_input("🔍 Search Repositories...", placeholder="Enter repo name or language...")
    
    # Filter repositories
    filtered_repos = []
    for r in repos:
        # Ignore user profile meta repos
        if r["name"].lower() == profile.get("login", "").lower():
            continue
            
        search_text = (r["name"] + " " + (r["description"] or "") + " " + (r["language"] or "")).lower()
        if repo_search and repo_search.lower() not in search_text:
            continue
        filtered_repos.append(r)
        
    if not filtered_repos:
        st.markdown("<p style='color:var(--text-muted);'>No repositories match the query.</p>", unsafe_allow_html=True)
        return
        
    # Display in cards grid
    for r in filtered_repos:
        desc = r.get("description") or "No description provided."
        lang = r.get("language") or "Python"
        stars = r.get("stargazers_count", 0)
        forks = r.get("forks_count", 0)
        
        # Format updated time
        updated_part = ""
        if r.get("updated_at"):
            try:
                dt = datetime.strptime(r["updated_at"][:10], "%Y-%m-%d")
                updated_part = f"| Updated: {dt.strftime('%b %d, %Y')}"
            except Exception:
                pass
                
        st.markdown(
            f"""
            <div class="glass-card" style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 0.5rem; flex-wrap: wrap;">
                    <h4 style="margin: 0; font-size: 1.15rem; color: var(--primary);">
                        <a href="{r['html_url']}" target="_blank" style="color: var(--primary); text-decoration: none;">{r['name']} ↗</a>
                    </h4>
                    <span class="tag-badge" style="font-size: 0.75rem; margin: 0; background: rgba(255,255,255,0.05); color: var(--text-color); border-color: var(--card-border);">{lang}</span>
                </div>
                <p style="font-size: 0.92rem; color: var(--text-muted); margin: 0.6rem 0;">{desc}</p>
                <div style="font-size: 0.8rem; color: var(--text-muted); font-weight: 500; display: flex; gap: 0.8rem; margin-top: 0.4rem;">
                    <span>⭐ {stars} stars</span>
                    <span>🍴 {forks} forks</span>
                    <span>{updated_part}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
