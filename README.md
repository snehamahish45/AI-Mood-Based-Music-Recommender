🎵 AI Mood-Based Music Recommender

An intelligent AI-powered music recommendation system that detects user emotions from text input and recommends songs accordingly using semantic emotion analysis and YouTube search.

Built with FastAPI, Sentence Transformers, and yt-dlp.

🚀 Features
🎭 AI-based emotion detection using NLP
🧠 Semantic similarity matching with Sentence Transformers
⚡ Fast rule-based emotion detection
🌍 Multi-language song recommendations
🎵 Dynamic YouTube music search
🔥 Trending & mood-based playlists
📱 REST API support
☁️ Render deployment ready
🛠️ Technologies Used
Python
FastAPI
Sentence Transformers
PyTorch
yt-dlp
Uvicorn
Scikit-learn
Pandas
NumPy
📂 Project Structure
AI-Mood-Music-Recommender/
│
├── app.py
├── routes/
│   └── predict.py
│
├── utils/
│   ├── emotion_similarity.py
│   └── youtube_api.py
│
├── requirements.txt
├── runtime.txt
├── render.yaml
│
└── frontend/
    └── index.html
⚙️ Installation
1️⃣ Clone Repository
git clone https://github.com/your-username/AI-Mood-Music-Recommender.git

cd AI-Mood-Music-Recommender
2️⃣ Create Virtual Environment
Windows
python -m venv venv

venv\Scripts\activate
Linux / Mac
python3 -m venv venv

source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt

Dependencies are defined in requirements.txt including:

FastAPI
Sentence Transformers
Torch
yt-dlp
Uvicorn
Scikit-learn

▶️ Run the Project
python app.py

Server runs at:

http://127.0.0.1:8000

Backend configuration uses FastAPI + Uvicorn.

🧠 Emotion Detection System

The project supports these emotions:

Joy
Sad
Calm
Love
Angry
Motivated
Anxious

Emotion detection is implemented using:

Rule-based keyword matching
Semantic similarity using Sentence Transformers

🌍 Supported Languages
English
Hindi
Bengali
Tamil
Telugu
Marathi
Gujarati
Kannada
Malayalam
Punjabi
Assamese
Odia
Urdu

📡 API Endpoint
POST /predict
Request Body
{
  "text": "I feel very happy today",
  "language": "english"
}

OR

{
  "emotion": "joy",
  "language": "hindi"
}
Response Example
{
  "emotion": "joy",
  "message": "Showing joy songs 🎧",
  "song_count": 10,
  "songs": [
    {
      "name": "Song Name",
      "artist": "Artist Name",
      "thumbnail": "Thumbnail URL",
      "videoId": "YouTube Video ID",
      "duration": 240
    }
  ]
}

Prediction route implementation:

🎵 Song Recommendation System

Songs are fetched dynamically from YouTube using yt-dlp.

Features:

Trending searches
Emotion-based keywords
Multi-language recommendations
Duplicate filtering
Fallback recommendations

Implementation:

☁️ Deployment on Render

This project is fully compatible with Render deployment.

Required Files
render.yaml
requirements.txt
runtime.txt

Python runtime:

python-3.11.9

📦 Important Packages
fastapi
uvicorn
sentence-transformers
torch
yt-dlp
scikit-learn
pandas
numpy

🔥 Future Improvements
Spotify API integration
User authentication
Playlist saving
Mood history tracking
Real-time music streaming
AI chatbot integration
Frontend React app
Mobile app version
👨‍💻 Author

Developed by Sneha Mahish

Data Sciencence Engineer

⭐ If You Like This Project

Give this repository a ⭐ on GitHub and support the project.
