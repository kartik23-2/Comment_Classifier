from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import uvicorn

# Load both models
spam_model = joblib.load("spam_model.pkl")
profanity_model = joblib.load("profanity_model.pkl")

app = FastAPI(title="Comment Filter API", version="1.0")

# Input schema
class Comment(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Welcome to the Comment Filter API 🚀"}

@app.post("/check-comment")
def check_comment(comment: Comment):
    text = comment.text

    # Spam Check 
    spam_pred = spam_model.predict([text])[0]
    try:
        spam_prob = spam_model.predict_proba([text])[0].max()
    except:
        spam_prob = 1.0  # for models without predict_proba

    # Profanity Check 
    prof_pred = profanity_model.predict([text])[0]
    try:
        prof_prob = profanity_model.predict_proba([text])[0].max()
    except:
        prof_prob = 1.0

    result = {
        "text": text,
        "spam_check": {
            "is_spam": bool(spam_pred),
            "confidence": round(float(spam_prob), 4)
        },
        "profanity_check": {
            "is_profane": bool(prof_pred),
            "confidence": round(float(prof_prob), 4)
        }
    }

    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
