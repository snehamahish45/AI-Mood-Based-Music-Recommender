import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# ===============================
# 📂 PATHS
# ===============================
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_PATH  = os.path.join(BASE_DIR, "..", "data", "emotion_dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "emotion_model.pkl")
VEC_PATH   = os.path.join(BASE_DIR, "vectorizer.pkl")

TEXT_COL  = "text"
LABEL_COL = "emotion"

# ===============================
# 📂 LOAD DATASET
# ===============================
print("📂 Loading dataset...")

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"❌ Dataset not found at: {DATA_PATH}")

df = pd.read_csv(DATA_PATH)
print(f"✅ Dataset loaded → {len(df)} rows")

# ===============================
# ✅ VALIDATE COLUMNS
# ===============================
if TEXT_COL not in df.columns or LABEL_COL not in df.columns:
    raise ValueError(
        f"❌ Dataset must have '{TEXT_COL}' and '{LABEL_COL}' columns.\n"
        f"Found columns: {list(df.columns)}"
    )

# ===============================
# 🧹 CLEAN DATA
# ===============================
df = df.dropna(subset=[TEXT_COL, LABEL_COL])
df[TEXT_COL]  = df[TEXT_COL].astype(str).str.strip()
df[LABEL_COL] = df[LABEL_COL].astype(str).str.strip().str.lower()

print(f"✅ After cleaning → {len(df)} rows")

# ===============================
# 📊 LABEL DISTRIBUTION CHECK
# ===============================
print("\n📊 Label Distribution:")
dist = df[LABEL_COL].value_counts()
print(dist)

# ✅ WARN IF IMBALANCED
max_count = dist.max()
min_count = dist.min()
if max_count / min_count > 5:
    print(
        "\n⚠️  WARNING: Dataset is imbalanced!"
        f"\n   Max class: {max_count} | Min class: {min_count}"
        "\n   Consider balancing your dataset for better accuracy."
    )

# ===============================
# ✂ SPLIT
# ===============================
X = df[TEXT_COL]
y = df[LABEL_COL]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y       # ✅ keeps label balance in both splits
)

print(f"\n✅ Train size: {len(X_train)} | Test size: {len(X_test)}")

# ===============================
# 🧠 VECTORIZE
# ===============================
print("\n🧠 Vectorizing text...")

vectorizer = TfidfVectorizer(
    max_features=10000,   # ✅ limit features for speed
    ngram_range=(1, 2),   # ✅ unigrams + bigrams (better accuracy)
    sublinear_tf=True     # ✅ log normalization
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec  = vectorizer.transform(X_test)

print(f"✅ Vocabulary size: {len(vectorizer.vocabulary_)}")

# ===============================
# 🤖 TRAIN MODEL
# ===============================
print("\n🤖 Training model...")

model = LogisticRegression(
    max_iter=1000,     # ✅ increased from 200 (avoids convergence warning)
    C=1.0,
    solver='lbfgs',
    multi_class='auto'
)

model.fit(X_train_vec, y_train)
print("✅ Model trained!")

# ===============================
# 📊 EVALUATE
# ===============================
print("\n📊 Evaluating model...")

y_pred = model.predict(X_test_vec)

accuracy = accuracy_score(y_test, y_pred)
print(f"\n🎯 Accuracy: {round(accuracy * 100, 2)}%")

print("\n📋 Classification Report:")
print(classification_report(y_test, y_pred))

print("🔲 Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# ===============================
# 💾 SAVE MODEL
# ===============================
joblib.dump(model,      MODEL_PATH)
joblib.dump(vectorizer, VEC_PATH)

print(f"\n✅ Model saved     → {MODEL_PATH}")
print(f"✅ Vectorizer saved → {VEC_PATH}")
print("\n🚀 Training complete!")