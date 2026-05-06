# Day 31: Automated Meeting Minutes (AI/ML)

## 🚀 The Build
An automated pipeline that takes audio from Zoom/Teams meetings, transcribes it with speaker identification (diarization), summarizes the key points using GPT-4o, and automatically syncs action items to a Notion database.

### Features
- **Speaker Diarization:** Distinguishes between the Founder, Dev, and Designer.
- **AI Task Extraction:** Automatically identifies "Who" needs to do "What" and "When".
- **Notion Integration:** One-click sync to your project management board.

---

## 📸 Instagram Content Guide

### Reel Idea: "Stop Taking Notes Manually"
1. **Hook (0-2s):** Text overlay: "POV: You're a Senior Engineer who hates manual notes." Show yourself (faceless) closing a physical notebook.
2. **The Problem (2-5s):** Record a Zoom screen with 3+ people talking. Text: "1-hour meeting = 30 mins of manual documentation."
3. **The Solution (5-12s):** Fast-cut screen recording of running `python app.py`. Show the terminal scrolling through the transcription and the "✅ Task Extracted" logs.
4. **The Value (12-15s):** Show the Notion board instantly populated with the tasks. Text: "Save 5 hours/week on admin."
5. **CTA:** "DM 'BUILD' to automate your workflow."

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
