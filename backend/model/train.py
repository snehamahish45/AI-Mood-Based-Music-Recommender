import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# 📂 Load dataset
df = pd.read_csv("emotion_dataset.csv")

# 🔍 Adjust column names if needed
TEXT_COL = "text"
LABEL_COL = "emotion"

# 🧹 Clean
df = df.dropna()

X = df[TEXT_COL]
y = df[LABEL_COL]

# ✂ Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 🧠 Vectorize
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)

# 🤖 Model
model = LogisticRegression(max_iter=200)
model.fit(X_train_vec, y_train)

# 💾 Save
joblib.dump(model, "emotion_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("✅ Model trained & saved")