from sentence_transformers import SentenceTransformer, util

model = None

def load_model():
    global model
    if model is None:
        model = SentenceTransformer('all-MiniLM-L6-v2')
    return model

emotion_bank = {
    "joy": ["happy", "excited", "fun"],
    "sad": ["lonely", "depressed", "hurt"],
    "calm": ["relaxed", "peaceful", "tired", "exhausted"],
    "love": ["romantic", "missing someone"],
    "angry": ["angry", "frustrated"]
}


def detect_emotion_semantic(text):

    text_lower = text.lower()

    # 🔥 rule-based override (very important)
    if any(word in text_lower for word in ["love", "romantic", "miss you"]):
        return "love"
    if any(word in text_lower for word in ["sad", "cry", "hurt"]):
        return "sad"
    if any(word in text_lower for word in ["happy", "excited"]):
        return "joy"

    # fallback to model
    model_instance = load_model()
    text_embedding = model_instance.encode(text, convert_to_tensor=True)

    best_emotion = None
    best_score = -1

    for emotion, samples in emotion_bank.items():
        sample_embeddings = model_instance.encode(samples, convert_to_tensor=True)
        score = util.cos_sim(text_embedding, sample_embeddings).mean().item()

        if score > best_score:
            best_score = score
            best_emotion = emotion

    # safer fallback
    if best_score < 0.50:
        best_emotion = "calm"

    return best_emotion