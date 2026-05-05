from fastapi import APIRouter

router = APIRouter()

from backend.utils.emotion_similarity import detect_emotion_semantic
from backend.utils.spotify_api import get_songs_by_emotion


@router.post("/predict")
def predict(data: dict):

    text = data.get("text", "")
    selected_emotion = data.get("emotion", "")
    language = data.get("language", "english")

    print("INPUT:", text, selected_emotion)

    # ✅ PRIORITY FIX
    if selected_emotion:
        predicted_emotion = selected_emotion
    elif text.strip():
        predicted_emotion = detect_emotion_semantic(text)
    else:
        predicted_emotion = "calm"

    print("FINAL:", predicted_emotion)

    songs = get_songs_by_emotion(predicted_emotion, language)

    return {
        "emotion": predicted_emotion,
        "message": f"Showing latest {predicted_emotion} songs 🎧",
        "songs": songs
    }