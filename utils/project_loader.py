import os
import json
import re
import pandas as pd
from pathlib import Path
import streamlit as st
from utils.github_api import fetch_github_repos

PROJECTS_DIR = "E:\\Projects"

# Manual mapping from local directory names to GitHub repository names
MANUAL_MAPPING = {
    "1_SuperStore Sales": "Superstore_Sales_Exploratory_Data_Analysis",
    "2_Bank Marketing": "Bank_Marketing-_Strategic_Campaign_-_Consumer_Behavior_Analysis",
    "3_Ecommerce": "E_Commerce_Revenue_Optimization_Customer_Behavior_Analysis",
    "4_Hospital charges": "Hospital_Charges_Healthcare_Cost_Payment_Efficiency_Analysis",
    "5_Golbal Air Pollution": "Global_Air_Pollution_Environmental_Impact_-_Spatial_Analysis",
    "Bank Customer Churn Risk Analysis": "Banking_Customer_Churn_Predictive_Analytics",
    "Netflix Content & User Insights Analysis": "Netflix_Content_Analysis",
    "Customer Trend analysis": "Customer_Shopping_Behavior_Consumer_Insights_Subscription_Analysis",
    "Electric vechile Population Analysis": "EV_KPI_Analysis-_Automotive_Business_Intelligence",
    "intelligent-document-extractor": "intelligent_document_extractor",
    "multi-doc-chatbot": "RAG-Based_AI_Chatbot",
    "rag-chatbot": "RAG_Based_Chatbot",
    "Student Performance Prediction & AnalysisSML_Project": "Student_Performance_Prediction_-SML_Project-",
    "Superstore-Sales-Dashboard-with-Streamlit": "Superstore_Sales_Dashboard_With_Streamlit",
    "Telecom-Customer-Churn-prediction": "Telecom_Customer_Churn_Prediction",
    "Weather Analysis": "Projects",
    "Fraud Detection": "Projects",
    "Heart Disease Analysis": "Projects",
    "Pubg Analysis": "Projects"
}

# Technologies keyword mapping for inferring tech list from README
TECH_KEYWORDS = {
    "Python": ["python", "py"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Scikit-Learn": ["scikit-learn", "sklearn", "ml", "machine learning"],
    "Streamlit": ["streamlit"],
    "Power BI": ["power bi", "powerbi", "dax"],
    "Tableau": ["tableau"],
    "Excel": ["excel", "vba", "formula"],
    "SQL": ["sql", "mysql", "postgresql", "queries"],
    "NLP": ["nlp", "text", "nltk", "spacy", "langchain"],
    "OpenAI": ["openai", "gpt", "llm", "rag"],
    "TensorFlow": ["tensorflow", "keras"],
    "PyTorch": ["pytorch"],
    "Docker": ["docker"],
    "Plotly": ["plotly"],
    "Matplotlib": ["matplotlib", "seaborn"]
}

def clean_title(name):
    """
    Cleans up directory names to create human-readable project titles.
    """
    # Remove prefix numbering like "1_", "2_"
    name = re.sub(r'^\d+_', '', name)
    # Replace hyphens and underscores with spaces
    name = name.replace('-', ' ').replace('_', ' ')
    # Capitalize words
    words = name.split()
    capitalized_words = []
    for word in words:
        if word.upper() in ["BI", "KPI", "AI", "ML", "RAG", "SML", "PDF"]:
            capitalized_words.append(word.upper())
        else:
            capitalized_words.append(word.capitalize())
    return " ".join(capitalized_words)

def read_readme_description(readme_path):
    """
    Tries to read README.md and extracts the first non-header block of text as description.
    """
    if not os.path.exists(readme_path):
        return ""
    try:
        with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Remove headers
        lines = content.split('\n')
        paragraphs = []
        current_paragraph = []
        for line in lines:
            line_stripped = line.strip()
            if line_stripped.startswith('#'):
                if current_paragraph:
                    paragraphs.append(" ".join(current_paragraph))
                    current_paragraph = []
                continue
            if line_stripped == '':
                if current_paragraph:
                    paragraphs.append(" ".join(current_paragraph))
                    current_paragraph = []
            else:
                current_paragraph.append(line_stripped)
        if current_paragraph:
            paragraphs.append(" ".join(current_paragraph))
            
        # Clean description
        for p in paragraphs:
            # Skip short paragraphs or those starting with images
            if len(p) > 30 and not p.startswith('!') and not p.startswith('['):
                # Trim long description
                return p[:300] + "..." if len(p) > 300 else p
        return ""
    except Exception:
        return ""

def infer_technologies(readme_path, folder_name, category):
    """
    Scans files and text to infer technologies used in the project.
    """
    techs = set()
    text = (folder_name + " " + clean_title(folder_name)).lower()
    
    # Read README if available to scan keywords
    if os.path.exists(readme_path):
        try:
            with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
                text += " " + f.read().lower()
        except Exception:
            pass
            
    for tech, keywords in TECH_KEYWORDS.items():
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', text):
                techs.add(tech)
                break
                
    # Add defaults based on category
    if "Excel" in category:
        techs.add("Excel")
    elif "Power BI" in category:
        techs.add("Power BI")
        techs.add("DAX")
    elif "Tableau" in category:
        techs.add("Tableau")
    elif "AI" in category or "Machine Learning" in category:
        techs.add("Python")
        techs.add("Scikit-Learn")
        
    if not techs:
        techs.add("Python")
        
    return list(techs)

# Custom Category and Weight Overrides
CATEGORY_OVERRIDES = {
    "computer_aided_monitoring_system_for_alzheimers_disease": "🐍 Python",
    "superstore-sales-dashboard-with-streamlit": "🐍 Python",
    "superstore_sales_dashboard_with_streamlit": "🐍 Python",
    "ai_job_trend_analysis_project": "📈 Power BI",
    "hospital_appointment_no-show_prediction_-_analysis": "📈 Power BI"
}

WEIGHT_OVERRIDES = {
    "hospital_appointment_no-show_prediction_-_analysis": -2,
    "ai_job_trend_analysis_project": -1
}

@st.cache_data(ttl=1800)  # Cache project load for 30 minutes
def load_all_projects():
    """
    Scans E:\\Projects, extracts local information, fetches matching GitHub repo info,
    and returns a combined list of projects with custom categorization and sorting weights.
    """
    raw_projects_list = []
    
    # 1. Fetch GitHub Repositories first to merge metadata
    github_repos = fetch_github_repos()
    repos_dict = {repo['name'].lower(): repo for repo in github_repos}
    
    # 2. Identify top level directories or fallback
    has_local = os.path.exists(PROJECTS_DIR) and os.path.isdir(PROJECTS_DIR)
    
    if not has_local:
        raw_projects_list = get_mocked_projects(github_repos)
    else:
        try:
            top_dirs = os.listdir(PROJECTS_DIR)
            for item in top_dirs:
                item_path = os.path.join(PROJECTS_DIR, item)
                if item.startswith('.') or not os.path.isdir(item_path) or item.lower() == "multi-doc-chatbot":
                    continue
                    
                # We categorize based on directory name or structure
                if item.lower() == "excel projects":
                    # Scan subdirectories
                    for sub in os.listdir(item_path):
                        sub_path = os.path.join(item_path, sub)
                        if not sub.startswith('.') and os.path.isdir(sub_path):
                            raw_projects_list.append(parse_project_folder(sub_path, sub, "📊 Excel", repos_dict))
                elif item.lower() == "power bi projects":
                    for sub in os.listdir(item_path):
                        sub_path = os.path.join(item_path, sub)
                        if not sub.startswith('.') and os.path.isdir(sub_path):
                            raw_projects_list.append(parse_project_folder(sub_path, sub, "📈 Power BI", repos_dict))
                elif item.lower() == "tableau projects":
                    for sub in os.listdir(item_path):
                        sub_path = os.path.join(item_path, sub)
                        if not sub.startswith('.') and os.path.isdir(sub_path):
                            raw_projects_list.append(parse_project_folder(sub_path, sub, "📉 Tableau", repos_dict))
                else:
                    # Top-level standalone projects (Python / AI / ML)
                    category = "🐍 Python"
                    # Deduce if AI/ML based on name keywords
                    ai_keywords = ["ai", "ml", "chatbot", "rag", "prediction", "predictor", "extractor", "sml", "learning"]
                    if any(k in item.lower() for k in ai_keywords):
                        category = "🤖 AI / Machine Learning"
                        
                    raw_projects_list.append(parse_project_folder(item_path, item, category, repos_dict))
        except Exception as e:
            st.error(f"Error reading local projects: {e}. Loading mocked projects.")
            raw_projects_list = get_mocked_projects(github_repos)
            
    # 3. Add GitHub repositories that are missing from the scanned local folder list
    loaded_repos = set()
    for p in raw_projects_list:
        github_name = MANUAL_MAPPING.get(p["folder_name"], p["folder_name"]).lower()
        loaded_repos.add(github_name)
        loaded_repos.add(p["folder_name"].lower())
        
    extra_repos = [
        "Computer_Aided_Monitoring_System_For_Alzheimers_Disease",
        "AI_Job_Trend_Analysis_Project",
        "Hospital_Appointment_No-Show_Prediction_-_Analysis"
    ]
    
    for extra in extra_repos:
        if extra.lower() not in loaded_repos:
            repo_info = repos_dict.get(extra.lower())
            if repo_info:
                category = CATEGORY_OVERRIDES.get(extra.lower(), "🐍 Python")
                proj_item = {
                    "name": clean_title(extra),
                    "folder_name": extra,
                    "category": category,
                    "description": repo_info.get("description") or f"GitHub repository for {clean_title(extra)}.",
                    "technologies": infer_technologies("", extra, category),
                    "github_url": repo_info.get("html_url", f"https://github.com/Nitishkumarkhavekar/{extra}"),
                    "demo_url": "",
                    "stars": repo_info.get("stargazers_count", 0),
                    "forks": repo_info.get("forks_count", 0),
                    "last_updated": repo_info.get("updated_at", ""),
                    "screenshot": "",
                    "weight": WEIGHT_OVERRIDES.get(extra.lower(), 0)
                }
                raw_projects_list.append(proj_item)

    # 4. Post-processing: apply category and weight overrides dynamically to all projects
    for proj in raw_projects_list:
        github_name = MANUAL_MAPPING.get(proj["folder_name"], proj["folder_name"]).lower()
        folder_name = proj["folder_name"].lower()
        
        # Category overrides
        if folder_name in CATEGORY_OVERRIDES:
            proj["category"] = CATEGORY_OVERRIDES[folder_name]
        elif github_name in CATEGORY_OVERRIDES:
            proj["category"] = CATEGORY_OVERRIDES[github_name]
            
        # Weight overrides
        if folder_name in WEIGHT_OVERRIDES:
            proj["weight"] = WEIGHT_OVERRIDES[folder_name]
        elif github_name in WEIGHT_OVERRIDES:
            proj["weight"] = WEIGHT_OVERRIDES[github_name]
        else:
            proj["weight"] = 0
            
    return raw_projects_list

def parse_project_folder(folder_path, folder_name, category, repos_dict):
    """
    Parses a single project folder, extracting metadata and merging GitHub stats.
    """
    path = Path(folder_path)
    json_path = path / "project.json"
    readme_path = path / "README.md"
    
    # 1. Initialize default values
    project_title = clean_title(folder_name)
    description = ""
    technologies = []
    github_url = ""
    demo_url = ""
    stars = 0
    forks = 0
    last_updated = ""
    
    # 2. Check for project.json
    if json_path.exists():
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
                project_title = metadata.get("name", project_title)
                description = metadata.get("description", "")
                technologies = metadata.get("technologies", [])
                github_url = metadata.get("github_url", "")
                demo_url = metadata.get("demo_url", "")
        except Exception:
            pass
            
    # 3. Read description and tech if not set by JSON
    if not description:
        description = read_readme_description(readme_path)
        if not description:
            description = f"A personal project focusing on {category.split()[-1]} developments."
            
    if not technologies:
        technologies = infer_technologies(readme_path, folder_name, category)
        
    # 4. Find screenshot
    screenshot_path = ""
    for ext in ["png", "jpg", "jpeg", "gif"]:
        for file in ["screenshot", "cover", "preview", folder_name]:
            test_file = path / f"{file}.{ext}"
            if test_file.exists():
                screenshot_path = str(test_file)
                break
        if screenshot_path:
            break
            
    # 5. Merge with GitHub details
    github_repo_name = MANUAL_MAPPING.get(folder_name)
    
    if github_repo_name:
        repo_info = repos_dict.get(github_repo_name.lower())
        if repo_info:
            github_url = repo_info.get("html_url", github_url or f"https://github.com/Nitishkumarkhavekar/{github_repo_name}")
            stars = repo_info.get("stargazers_count", 0)
            forks = repo_info.get("forks_count", 0)
            last_updated = repo_info.get("updated_at", "")
            
            # If description was empty, load it from GitHub
            if not description or description.startswith("A personal project"):
                repo_desc = repo_info.get("description")
                if repo_desc:
                    description = repo_desc
                    
    # Provide fallback URLs if missing
    if not github_url and github_repo_name:
        github_url = f"https://github.com/Nitishkumarkhavekar/{github_repo_name}"
        
    # Return structured data
    return {
        "name": project_title,
        "folder_name": folder_name,
        "category": category,
        "description": description,
        "technologies": technologies,
        "github_url": github_url,
        "demo_url": demo_url,
        "stars": stars,
        "forks": forks,
        "last_updated": last_updated,
        "screenshot": screenshot_path
    }

def get_mocked_projects(github_repos):
    """
    Generates a set of mock projects mapping local paths to details so the site runs when local dir is missing.
    """
    repos_dict = {repo['name'].lower(): repo for repo in github_repos}
    
    raw_projects = [
        # Excel
        {"folder_name": "1_SuperStore Sales", "category": "📊 Excel", "tech": ["Excel", "Pivot Tables", "VBA"]},
        {"folder_name": "2_Bank Marketing", "category": "📊 Excel", "tech": ["Excel", "Formulas", "Data Analysis"]},
        {"folder_name": "3_Ecommerce", "category": "📊 Excel", "tech": ["Excel", "Cohort Analysis", "Power Query"]},
        {"folder_name": "4_Hospital charges", "category": "📊 Excel", "tech": ["Excel", "Pivot Charts", "KPIs"]},
        {"folder_name": "5_Golbal Air Pollution", "category": "📊 Excel", "tech": ["Excel", "Statistical Analysis"]},
        # Power BI
        {"folder_name": "Bank Customer Churn Risk Analysis", "category": "📈 Power BI", "tech": ["Power BI", "DAX", "Data Modeling"]},
        {"folder_name": "Customer Trend analysis", "category": "📈 Power BI", "tech": ["Power BI", "Power Query", "Dashboards"]},
        {"folder_name": "Fraud Detection", "category": "📈 Power BI", "tech": ["Power BI", "Security Dashboards"]},
        {"folder_name": "Heart Disease Analysis", "category": "📈 Power BI", "tech": ["Power BI", "Data Analysis"]},
        {"folder_name": "Netflix Content & User Insights Analysis", "category": "📈 Power BI", "tech": ["Power BI", "Entertainment Insights"]},
        {"folder_name": "Pubg Analysis", "category": "📈 Power BI", "tech": ["Power BI", "Gaming Stats"]},
        {"folder_name": "Weather Analysis", "category": "📈 Power BI", "tech": ["Power BI", "Climatology Dashboards"]},
        # Tableau
        {"folder_name": "Electric vechile Population Analysis", "category": "📉 Tableau", "tech": ["Tableau", "Geomaps", "LOD Expressions"]},
        {"folder_name": "Investment Behaviour Analysis", "category": "📉 Tableau", "tech": ["Tableau", "Finance Dashboard"]},
        {"folder_name": "Social Media Usage Analysis", "category": "📉 Tableau", "tech": ["Tableau", "User Retention"]},
        # Python / AI / ML
        {"folder_name": "intelligent-document-extractor", "category": "🤖 AI / Machine Learning", "tech": ["Python", "OpenAI", "Streamlit", "OCR", "NLP"]},
        {"folder_name": "rag-chatbot", "category": "🤖 AI / Machine Learning", "tech": ["Python", "RAG", "Vector Embeddings", "Streamlit"]},
        {"folder_name": "Student Performance Prediction & AnalysisSML_Project", "category": "🤖 AI / Machine Learning", "tech": ["Python", "Scikit-Learn", "Pandas", "Regression"]},
        {"folder_name": "Superstore-Sales-Dashboard-with-Streamlit", "category": "🐍 Python", "tech": ["Python", "Streamlit", "Plotly", "Pandas"]},
        {"folder_name": "Telecom-Customer-Churn-prediction", "category": "🤖 AI / Machine Learning", "tech": ["Python", "Scikit-Learn", "Classification", "XGBoost"]}
    ]
    
    projects_list = []
    for item in raw_projects:
        folder_name = item["folder_name"]
        category = item["category"]
        tech = item["tech"]
        
        project_title = clean_title(folder_name)
        description = f"A personal portfolio project in {category.split()[-1]} focusing on business analysis and technical modeling."
        github_url = ""
        stars = 0
        forks = 0
        last_updated = ""
        
        github_repo_name = MANUAL_MAPPING.get(folder_name)
        if github_repo_name:
            repo_info = repos_dict.get(github_repo_name.lower())
            if repo_info:
                github_url = repo_info.get("html_url", "")
                stars = repo_info.get("stargazers_count", 0)
                forks = repo_info.get("forks_count", 0)
                last_updated = repo_info.get("updated_at", "")
                repo_desc = repo_info.get("description")
                if repo_desc:
                    description = repo_desc
                    
        if not github_url and github_repo_name:
            github_url = f"https://github.com/Nitishkumarkhavekar/{github_repo_name}"
            
        projects_list.append({
            "name": project_title,
            "folder_name": folder_name,
            "category": category,
            "description": description,
            "technologies": tech,
            "github_url": github_url,
            "demo_url": "",
            "stars": stars,
            "forks": forks,
            "last_updated": last_updated,
            "screenshot": ""
        })
        
    return projects_list
