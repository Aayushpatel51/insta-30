# Day 31: Automated Meeting Minutes (AI/ML)

## 🚀 The Build
An automated pipeline that takes audio from Zoom/Teams meetings, transcribes it with speaker identification (diarization), summarizes the key points using GPT-4o, and automatically syncs action items to a Notion database.

### Features
- **Speaker Diarization:** Distinguishes between the Founder, Dev, and Designer.
- **AI Task Extraction:** Automatically identifies "Who" needs to do "What" and "When".
- **Notion Integration:** One-click sync to your project management board.

---

## 📸 Instagram Content Guide

### Reel Idea: "The Future of Meetings" (High Visual Impact)
1. **Hook (0-2s):** Start with the **Live Transcript** typing out in real-time. Text overlay: "POV: Your meetings write themselves."
2. **The Reveal (2-6s):** Pan across the **Intelligent Summary** appearing. Use a "Swoosh" sound effect. Text: "GPT-4o summarized 60 mins into 3 sentences."
3. **The 'Senior' Edge (6-10s):** Zoom in on the **Action Items** being extracted. Point out the "Speaker Diarization" architecture note.
4. **The Value (10-15s):** Show the "Export to Notion" button being clicked. Text: "80% less workload. More time for deep work."
5. **CTA:** "DM 'BUILD' for the source code."

### Carousel Idea: "How I Built a Meeting-to-Notion Pipeline"
- **Slide 1:** Hook: "Meeting Minutes on Autopilot (Senior Architect Level)"
- **Slide 2:** The Architecture: Flowchart (Audio -> Whisper -> GPT-4o -> Notion).
- **Slide 3:** Code Snippet: Show the `transcribe_and_diarize` function. Explain why Diarization is key for B2B apps.
- **Slide 4:** The AI Prompt: Explain how to prompt for "Action Item" extraction.
- **Slide 5:** Why this is an MVP: Explain the business value (Time = Money for startups).

---

## 🛠️ Setup (For Real Use)
1. Clone the repo.
2. `pip install python-dotenv openai notion-client`
3. Copy `.env.example` to `.env` and fill in your keys.
4. Replace the `use_mock=True` with your real logic in `app.py`.
5. Run `python app.py`.
