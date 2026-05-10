# predict.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from utils.emotion_similarity import detect_emotion_semantic
from utils.youtube_api import get_songs_by_emotion

router = APIRouter()

class PredictRequest(BaseModel):
    text: Optional[str] = ""
    emotion: Optional[str] = ""
    language: Optional[str] = "english"
    refresh: Optional[bool] = False

VALID_EMOTIONS = {"joy", "sad", "calm", "love", "angry", "motivated", "anxious"}
VALID_LANGUAGES = {
    "english", "hindi", "bengali", "tamil", "telugu",
    "marathi", "gujarati", "kannada", "malayalam",
    "punjabi", "assamese", "odia", "urdu"
}

@router.post("/predict")
def predict(data: PredictRequest):

    text             = (data.text or "").strip()
    selected_emotion = (data.emotion or "").strip().lower()
    language         = (data.language or "english").strip().lower()

    if len(text) > 500:
        raise HTTPException(status_code=400, detail="Text too long. Max 500 characters.")

    if selected_emotion and selected_emotion not in VALID_EMOTIONS:
        raise HTTPException(status_code=400, detail=f"Invalid emotion.")

    if language not in VALID_LANGUAGES:
        language = "english"

    try:
        if selected_emotion:
            predicted_emotion = selected_emotion
        elif text:
            predicted_emotion = detect_emotion_semantic(text)
        else:
            predicted_emotion = "calm"
    except Exception as e:
        print(f"❌ Emotion detection failed: {e}")
        predicted_emotion = "calm"

    try:
        songs = get_songs_by_emotion(predicted_emotion, language)
    except Exception as e:
        print(f"❌ Song fetch failed: {e}")
        songs = []

    return {
        "emotion": predicted_emotion,
        "message": f"Showing {predicted_emotion} songs 🎧",
        "song_count": len(songs),
        "songs": songs
    }