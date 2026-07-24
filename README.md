# 🌊 AI Ocean Studio

An emotion-driven music discovery web application designed to personalize your listening experience in real time using client-side facial expression analysis and voice energy tracking.

Developed during my Web Development Internship at **Traversa Private Limited**.

---

## 🌟 Key Features

- 🎭 **Real-Time Facial Emotion Detection:** Classifies expressions (*Happy, Sad, Angry, Fear, Tired, Exhausted, Neutral*) locally in the browser.
- 🎛️ **Manual & Voice Control:** Offers manual mood overrides, ambient ocean background audio, and voice search capability.
- 🎵 **Multi-Platform Streaming Integration:** Dynamically fetches and plays recommendations from both **YouTube** and **Spotify**.
- 🔒 **100% On-Device & Privacy-First:** Built with client-side neural landmark analysis—no webcam footage or audio recordings leave the browser session.

---

## 🛠️ Tech Stack & Architecture

- **Backend:** Python, Flask, YouTube API, Spotify Search API
- **Frontend:** JavaScript, Web Audio API, Web Speech API, Custom CSS, HTML5
- **ML Engine:** Client-side neural models (`face-api.js`) for real-time landmark tracking
- **UI/UX:** Responsive Design with Light/Dark Mode support

---

## 🚀 How to Run Locally

1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_GITHUB_USERNAME/AI-Ocean-Studio.git](https://github.com/YOUR_GITHUB_USERNAME/AI-Ocean-Studio.git)
   cd AI-Ocean-Studio
   
  2. Install requirements 
pip install -r requirements.txt

3. Run flask app
python app.py

4.Open in browser:
Navigate to http://127.0.0.1:5000
