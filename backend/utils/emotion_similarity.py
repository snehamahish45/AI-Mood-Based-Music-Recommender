# TOP of emotion_similarity.py — no backend. prefix
from sentence_transformers import SentenceTransformer, util
model = None

def load_model():
    global model
    if model is None:
        print("🤖 Loading SentenceTransformer model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Model loaded!")
    return model


# ✅ EXPANDED EMOTION BANK
emotion_bank = {
    "joy": [
        "happy", "excited", "fun", "cheerful", "energetic",
        "joyful", "thrilled", "elated", "ecstatic", "delighted",
        "great", "awesome", "fantastic", "wonderful", "celebratingi",
        "jumping with joy", "on top of the world", "blessed", "grateful",
        "positive", "laughing", "smiling", "enjoying life"
    ],
    "sad": [
        "lonely", "depressed", "hurt", "crying", "broken",
        "unhappy", "miserable", "heartbroken", "hopeless", "sorrowful",
        "grief", "loss", "empty", "pain", "suffering",
        "tearful", "gloomy", "devastated", "disappointed", "down",
        "nobody understands me", "feeling low", "cant stop crying",
        "missing someone", "left alone", "abandoned"
    ],
    "calm": [
        "relaxed", "peaceful", "tired", "exhausted", "sleepy",
        "chill", "quiet", "serene", "tranquil", "mellow",
        "at ease", "slow", "rest", "unwind", "meditate",
        "breathing slowly", "no stress", "mind at rest",
        "lazy day", "soft music", "cozy", "gentle"
    ],
    "love": [
        "romantic", "missing someone", "in love", "relationship",
        "crush", "heart", "affection", "adore", "passionate",
        "beloved", "darling", "sweetheart", "intimacy", "caring",
        "valentine", "cute couple", "falling in love",
        "thinking about someone", "unconditional love", "soulmate",
        "hugging", "kissing", "dating", "forever together"
    ],
    "angry": [
        "angry", "frustrated", "mad", "furious",
        "rage", "irritated", "annoyed", "aggressive", "outraged",
        "hate", "betrayed", "cheated", "lied to", "disrespected",
        "fed up", "enough", "cant take it anymore",
        "want to scream", "losing control", "revenge",
        "fight", "breaking things", "explosive anger"
    ],
    "motivated": [
        "motivated", "inspired", "determined", "focused",
        "ambitious", "driven", "unstoppable", "grind", "hustle",
        "goal", "achieve", "success", "winning", "champion",
        "never give up", "work hard", "push harder",
        "level up", "keep going", "strong mindset"
    ],
    "anxious": [
        "anxious", "nervous", "worried", "stressed", "panic",
        "overthinking", "cant sleep", "restless", "uneasy",
        "fear", "scared", "tension", "pressure", "overwhelmed",
        "too much on my mind", "cant focus", "shaking",
        "heartbeat fast", "sweating", "breathless"
    ]
}


# ✅ EXPANDED RULE-BASED KEYWORDS
rule_based = {
    "love": [
        "love", "romantic", "miss you", "crush", "heart",
        "darling", "sweetheart", "adore", "falling for",
        "thinking about you", "soulmate", "forever"
    ],
    "sad": [
        "sad", "cry", "hurt", "depressed", "lonely",
        "broken", "hopeless", "grief", "miss", "empty",
        "nobody", "abandoned", "devastated", "crying"
    ],
    "joy": [
        "happy", "excited", "fun", "joy", "great",
        "awesome", "fantastic", "celebrate", "thrilled",
        "blessed", "wonderful", "laugh", "smile"
    ],
    "angry": [
        "angry", "mad", "frustrated", "furious", "rage",
        "hate", "irritated", "annoyed", "fed up",
        "betrayed", "revenge", "fight", "outraged"
    ],
    "calm": [
        "tired", "calm", "peaceful", "relax", "exhausted",
        "sleepy", "chill", "quiet", "serene", "rest",
        "unwind", "cozy", "mellow", "slow"
    ],
    "motivated": [
        "motivated", "inspired", "focused", "determined",
        "grind", "hustle", "achieve", "goal", "success",
        "unstoppable", "champion", "never give up"
    ],
    "anxious": [
        "anxious", "nervous", "worried", "stressed",
        "panic", "overthinking", "cant sleep", "overwhelmed",
        "scared", "fear", "pressure", "restless"
    ]
}


def detect_emotion_semantic(text):

    text_lower = text.lower()

    # ✅ RULE-BASED FAST DETECTION
    for emotion, keywords in rule_based.items():
        if any(word in text_lower for word in keywords):
            print(f"⚡ Rule-based match → {emotion}")
            return emotion

    # ✅ AI MODEL DETECTION WITH CONFIDENCE THRESHOLD
    model_instance = load_model()

    text_embedding = model_instance.encode(
        text,
        convert_to_tensor=True
    )

    best_emotion = "calm"
    best_score = -1
    CONFIDENCE_THRESHOLD = 0.15  # ✅ minimum score to accept

    for emotion, samples in emotion_bank.items():
        sample_embeddings = model_instance.encode(
            samples,
            convert_to_tensor=True
        )
        score = util.cos_sim(
            text_embedding,
            sample_embeddings
        ).mean().item()

        print(f"📊 Emotion: {emotion} | Score: {round(score, 4)}")

        if score > best_score:
            best_score = score
            best_emotion = emotion

    # ✅ CONFIDENCE CHECK
    if best_score < CONFIDENCE_THRESHOLD:
        print(f"⚠️ Low confidence ({best_score}) → defaulting to calm")
        return "calm"

    print(f"🎯 FINAL: {best_emotion} (score: {round(best_score, 4)})")
    return best_emotion