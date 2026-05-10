import uvicorn
import os
import sys

# ✅ Add backend to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

if __name__ == "__main__":
    print("🚀 Starting AI Mood Music Recommender...")
    print("🌐 Open → http://127.0.0.1:8000")
    print("📖 API Docs → http://127.0.0.1:8000/docs")
    print("⏹  Press CTRL+C to stop\n")

    uvicorn.run(
        "backend.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["backend"]
    )