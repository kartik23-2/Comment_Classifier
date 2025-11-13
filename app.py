from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import uvicorn

# Load both models
spam_model = joblib.load("spam_model.pkl")
profanity_model = joblib.load("profanity_model.pkl")

app = FastAPI(title="Comment Filter API", version="1.0")

class Comment(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Welcome to the Comment Filter API 🚀"}

@app.post("/check-comment")
def check_comment(comment: Comment):
    text = comment.text

    # ----------- SPAM CHECK WITH THRESHOLD -----------
    try:
        spam_prob = spam_model.predict_proba([text])[0][1]   # probability of spam class
    except:
        spam_prob = 1.0

    spam_threshold = 0.6
    spam_pred = 1 if spam_prob >= spam_threshold else 0


    # ----------- PROFANITY CHECK WITH THRESHOLD -----------
    try:
        prof_prob = profanity_model.predict_proba([text])[0][1]
    except:
        prof_prob = 1.0

    prof_threshold = 0.6
    prof_pred = 1 if prof_prob >= prof_threshold else 0


    # ----------- RESPONSE -----------
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
