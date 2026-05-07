# Day 34: Shadow IT Discovery Tool (Cyber MVP)

A cybersecurity focused MVP that scans organization OAuth environments to discover unauthorized or high-risk third-party applications.

## 🚀 How to Run
1. Navigate to this directory:
   ```bash
   cd builds/day-34
   ```
2. Build and run with Docker:
   ```bash
   docker-compose up --build
   ```
3. Open `http://localhost:8000` in your browser.

## 📸 Instagram Content Guide

### 1. The Reel Hook
- **Visual:** A close-up of a screen showing a red "High Risk" alert next to a seemingly harmless app like "Free PDF Converter".
- **Text Overlay:** "This 'free' app is reading your company's emails 📧⚠️"
- **Audio:** Fast, tense tech beat.

### 2. The Carousel Strategy
- **Slide 1:** "Shadow IT: The silent killer of startup security." (Visual: The ShadowGuard Dashboard)
- **Slide 2:** "What is Shadow IT?" (Visual: Diagram of users connecting apps without IT approval)
- **Slide 3:** "The Risks: Data Exfiltration via OAuth scopes." (Visual: Highlight `mail.read` and `files.read.all` in the dashboard)
- **Slide 4:** "The Solution: Automated Discovery & Revocation." (Visual: Clicking the 'Revoke' button)
- **Slide 5:** "Senior Tip: Monitor for high-risk scopes."

### 3. The Caption
"Did you know 80% of employees use non-approved SaaS apps at work? 😱

This Shadow IT Discovery MVP helps IT teams find and revoke access to high-risk apps before they become a breach.

**Senior Tip:** When auditing OAuth apps, don't just look at the app name. Look at the 'Scopes'. An app requesting `mail.read` or `files.read.all` should be a P0 priority for review.

Want to build security tools like this? DM 'CYBER' for the architectural blueprint! 🛡️

#CyberSecurity #BuildInPublic #SeniorEngineer #SaaS #InfoSec #OAuth #ShadowIT"

## 🛠️ Tech Stack
- **Backend:** FastAPI (Python)
- **Frontend:** HTML5, Tailwind CSS, JavaScript (Vanilla)
- **Iconography:** FontAwesome 6
- **Deployment:** Docker / Docker-Compose
