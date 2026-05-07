# Senior Engineer Instagram Content Hub (60-Day Challenge)

This repository contains the full strategy, technical blueprints, and functional MVP builds for a "Build in Public" Instagram content challenge.

## 📁 Repository Structure
- `60_DAYS_PLAN.md`: The full 60-day content calendar with hooks, value props, and niche breakdown.
- `MVP_IDEAS_DETAIL.md`: Detailed technical architectural blueprints for 60 different MVPs.
- `builds/`: Contains the full-stack code for individual MVPs.
    - `day-31/`: **MeetingFlow** - AI-powered meeting-to-architecture summary engine (FastAPI + Claude 3.5).
    - `day-32/`: **AdminFlow** - Low-code internal admin panel builder (FastAPI + Tailwind).
    - `day-33/`: **DispatchFlow** - Field Service Dispatch MVP with real-time mapping (FastAPI + Leaflet.js).
    - `day-34/`: **ShadowGuard** - Shadow IT Discovery tool for OAuth auditing (FastAPI + Tailwind).

## 🚀 Getting Started (Day 31/32/33/34 MVPs)
Each build is designed to be easily launchable using Docker.

1. Navigate to the build directory:
   ```bash
   cd builds/day-31
   ```
2. Copy the environment file and add your `ANTHROPIC_API_KEY`:
   ```bash
   cp .env.example .env
   ```
3. Launch with Docker Compose:
   ```bash
   docker-compose up --build
   ```

## 📸 Content Strategy
The projects are designed to be visually appealing for Reels and Carousels:
- **Light/Dark Mode Support**: Essential for "Tech Aesthetic" shots.
- **Interactive UI**: Dashboard navigation, toast notifications, and live loaders.
- **B2B Focus**: The second 30 days focus heavily on cost-saving and workload reduction for startups.

---
*Created as part of the Senior Engineer Instagram Growth Strategy.*
