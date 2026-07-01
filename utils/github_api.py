import os
import requests
import streamlit as st

GITHUB_API_URL = "https://api.github.com"
USERNAME = "Nitishkumarkhavekar"

# Retrieve token from environment variable if available
TOKEN = os.getenv("GITHUB_PAT") or os.getenv("GITHUB_TOKEN")

def get_headers():
    headers = {
        "Accept": "application/vnd.github+json"
    }
    if TOKEN:
        headers["Authorization"] = f"token {TOKEN}"
    return headers

@st.cache_data(ttl=3600)  # Cache for 1 hour to avoid rate limit hits
def fetch_github_profile():
    """
    Fetches public profile details for the user.
    """
    url = f"{GITHUB_API_URL}/users/{USERNAME}"
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.warning(f"Failed to fetch GitHub profile (HTTP {response.status_code}). Using fallback profile.")
            return get_fallback_profile()
    except Exception as e:
        st.error(f"Error fetching GitHub profile: {e}")
        return get_fallback_profile()

@st.cache_data(ttl=3600)  # Cache for 1 hour to avoid rate limit hits
def fetch_github_repos():
    """
    Fetches all public repositories for the user.
    """
    url = f"{GITHUB_API_URL}/users/{USERNAME}/repos?per_page=100&sort=updated"
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.warning(f"Failed to fetch GitHub repositories (HTTP {response.status_code}). Using fallback repos.")
            return get_fallback_repos()
    except Exception as e:
        st.error(f"Error fetching GitHub repositories: {e}")
        return get_fallback_repos()

def get_fallback_profile():
    return {
        "login": USERNAME,
        "avatar_url": "https://avatars.githubusercontent.com/u/169582171?v=4",
        "html_url": f"https://github.com/{USERNAME}",
        "name": "NITISHKUMAR KHAVEKAR",
        "company": None,
        "blog": "",
        "location": "Sangli, MH",
        "email": "khavekarnitishkumar@gmail.com",
        "bio": "Data Analyst and AI/ML Engineer. Proficient in Python, SQL, Power BI, and Machine Learning.",
        "public_repos": 26,
        "followers": 5,
        "following": 5
    }

def get_fallback_repos():
    # List of realistic repos on Nitish's profile from previous drive scan:
    return [
        {
            "name": "Superstore_Sales_Dashboard_With_Streamlit",
            "description": "Interactive retail sales dashboard built using Streamlit and Python.",
            "stargazers_count": 0,
            "forks_count": 0,
            "language": "Python",
            "updated_at": "2026-06-23T22:00:00Z",
            "html_url": f"https://github.com/{USERNAME}/Superstore_Sales_Dashboard_With_Streamlit"
        },
        {
            "name": "Telecom_Customer_Churn_Prediction",
            "description": "Predicting customer churn using Machine Learning algorithms in Python.",
            "stargazers_count": 0,
            "forks_count": 0,
            "language": "Python",
            "updated_at": "2026-06-23T21:00:00Z",
            "html_url": f"https://github.com/{USERNAME}/Telecom_Customer_Churn_Prediction"
        },
        {
            "name": "intelligent_document_extractor",
            "description": "AI-powered document information extraction tool.",
            "stargazers_count": 0,
            "forks_count": 0,
            "language": "Python",
            "updated_at": "2026-06-22T18:00:00Z",
            "html_url": f"https://github.com/{USERNAME}/intelligent_document_extractor"
        },
        {
            "name": "RAG-Based_AI_Chatbot",
            "description": "Retrieval Augmented Generation chatbot querying multiple documents.",
            "stargazers_count": 0,
            "forks_count": 0,
            "language": "Python",
            "updated_at": "2026-06-22T20:00:00Z",
            "html_url": f"https://github.com/{USERNAME}/RAG-Based_AI_Chatbot"
        },
        {
            "name": "Banking_Customer_Churn_Predictive_Analytics",
            "description": "Predicting churn risk for bank customers using classification models.",
            "stargazers_count": 0,
            "forks_count": 0,
            "language": "Python",
            "updated_at": "2026-06-23T19:00:00Z",
            "html_url": f"https://github.com/{USERNAME}/Banking_Customer_Churn_Predictive_Analytics"
        },
        {
            "name": "Student_Performance_Prediction_-SML_Project-",
            "description": "Supervised Machine Learning project for predicting student academic performance.",
            "stargazers_count": 0,
            "forks_count": 0,
            "language": "Python",
            "updated_at": "2026-06-23T19:30:00Z",
            "html_url": f"https://github.com/{USERNAME}/Student_Performance_Prediction_-SML_Project-"
        }
    ]
