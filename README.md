# Data Analytics & AI/ML Portfolio Website

A highly interactive, modern, and professional portfolio website built with Python and Streamlit. This website features custom styling (glassmorphism), a dark/light theme switcher, live GitHub REST API integration, and scans local project folders to present structured analytics and machine learning repositories.

## 🚀 Features

- **Dynamic Navigation**: Sleek sidebar option menu with custom icons.
- **Theme Support**: Dark/Light mode toggle that dynamically adjusts color variables.
- **Home Page**: Includes professional highlights, dynamic role typing animations, download resume support, and aggregated visits/repo/certs metrics.
- **Contact Form**: Responsive inputs saving messages directly to a local JSON file for persistence.
- **Education Timeline**: Custom HTML/CSS academic milestones cards.
- **Live GitHub Sync**: Real-time followers, stars, and repos listing with client-side searching.
- **Skills Mapping**: Animated progress bars paired with an interactive Plotly radar chart illustrating tech proficiency.
- **Certificates Shelf**: Cards displaying certificate tags and links.
- **Local Project Loader**:
  - Automatically scans `E:\Projects` directory on start.
  - Groups them into categories: 📊 Excel, 📈 Power BI, 📉 Tableau, 🐍 Python, and 🤖 AI / Machine Learning.
  - Matches local directory names with GitHub repository names to display live fork and star counts.
  - Reads metadata from `project.json` or parses `README.md` descriptions.

---

## 🛠️ Project Directory Structure

```text
Portfolio/
│
├── app.py                      # Main entrypoint, page routing, and theme control
├── requirements.txt            # Python library dependencies
├── README.md                   # Setup and usage documentation
│
├── assets/                     # Assets folder
│     ├── profile.png           # Professional avatar placeholder
│     ├── resume.pdf            # PDF copy of resume (downloadable)
│     ├── css/
│     │    └── style.css        # Theme variables, layouts, and animations stylesheet
│     └── certificates/         # Directory for local credentials images
│
├── data/                       # Structured JSON data stores
│     ├── certificates.json     # List of credentials/badges
│     ├── education.json        # Academic timeline items
│     ├── contact.json          # Social handles, locations, and bios
│     └── skills.json           # Categorized tech skill points
│
├── utils/                      # Helper libraries
│     ├── github_api.py         # Handles request fetching and caching from GitHub REST API
│     ├── project_loader.py     # Local projects directory scanner & GitHub merger
│     └── helpers.py            # Local visits tracker, message saver, typing animations
│
└── pages/                      # Individual page modules
      ├── Home.py
      ├── Contact.py
      ├── Education.py
      ├── Projects.py
      ├── Skills.py
      ├── Certificates.py
      ├── GitHub.py
      └── LinkedIn.py
```

---

## 💻 Setup & Installation

### 1. Clone the repository
Make sure the files are extracted in your active workspace (e.g., `C:\Users\user\.gemini\antigravity\scratch\Portfolio`).

### 2. Configure Local Projects
Ensure your projects folder on Windows is located at `E:\Projects`. Inside this folder, you can structure your projects as:
- Top-level folders (e.g., `intelligent-document-extractor`, `Superstore-Sales-Dashboard-with-Streamlit`)
- Specialized containers (e.g., `Excel Projects/`, `Power BI Projects/`, `Tableau Projects/`) containing specific dashboard folders.

*Optional*: If you want custom icons or screenshots, place an image named `screenshot.png` inside any project folder.

### 3. Add personal configurations
- Replace `assets/profile.png` with your portrait photo.
- Replace `assets/resume.pdf` with your updated curriculum vitae.
- Edit `data/contact.json`, `data/education.json`, `data/certificates.json`, and `data/skills.json` to customize the titles, links, and content.

### 4. Install Dependencies
Run the command:
```bash
pip install -r requirements.txt
```

### 5. Launch the Application
Start the Streamlit server:
```bash
streamlit run app.py
```

---

## 🔑 GitHub API Authentication (Optional)

The GitHub API limits unauthenticated requests to 60 per hour. To increase this to 5,000 requests per hour, set your GitHub Personal Access Token (PAT) as an environment variable:

**Command Prompt / PowerShell:**
```powershell
$env:GITHUB_PAT="your_personal_access_token_here"
```

Then run `streamlit run app.py`. The app will automatically read the token and authenticate its requests.
