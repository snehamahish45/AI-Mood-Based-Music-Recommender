from sentence_transformers import SentenceTransformer, util

model = None


def load_model():
    global model

    if model is None:
        model = SentenceTransformer('all-MiniLM-L6-v2')

    return model


emotion_bank = {
    "joy": [
        "happy",
        "excited",
        "fun",
        "cheerful",
        "energetic"
    ],

    "sad": [
        "lonely",
        "depressed",
        "hurt",
        "crying",
        "broken"
    ],

    "calm": [
        "relaxed",
        "peaceful",
        "tired",
        "exhausted",
        "sleepy"
    ],

    "love": [
        "romantic",
        "missing someone",
        "in love",
        "relationship"
    ],

    "angry": [
        "angry",
        "frustrated",
        "mad",
        "furious"
    ]
}


def detect_emotion_semantic(text):

    text_lower = text.lower()

    # ==================================
    # 🔥 FAST RULE BASED DETECTION
    # ==================================

    if any(word in text_lower for word in ["love", "romantic", "miss you", "crush"]):
        return "love"

    if any(word in text_lower for word in ["sad", "cry", "hurt", "depressed"]):
        return "sad"

    if any(word in text_lower for word in ["happy", "excited", "fun"]):
        return "joy"

    if any(word in text_lower for word in ["angry", "mad", "frustrated"]):
        return "angry"

    if any(word in text_lower for word in ["tired", "calm", "peaceful", "relax", "exhausted"]):
        return "calm"

    # ==================================
    # 🤖 AI MODEL DETECTION
    # ==================================

    model_instance = load_model()

    text_embedding = model_instance.encode(
        text,
        convert_to_tensor=True
    )

    best_emotion = "calm"
    best_score = -1

    for emotion, samples in emotion_bank.items():

        # 🔥 FIX
        sample_embeddings = model_instance.encode(
            samples,
            convert_to_tensor=True
        )

        score = util.cos_sim(
            text_embedding,
            sample_embeddings
        ).mean().item()

        print(f"Emotion: {emotion} | score: {score}")

        if score > best_score:
            best_score = score
            best_emotion = emotion

    print("🎯 FINAL:", best_emotion)

    return best_emotion