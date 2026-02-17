from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

messages = {
    "en": {
        "welcome": "Welcome to NUMs API!",
        "invalid_date": "Invalid date format. Use YYYY-MM-DD.",
        "result": "Your Numerology Result"
    },
    "hi": {
        "welcome": "NUMs API में आपका स्वागत है!",
        "invalid_date": "गलत तारीख प्रारूप। YYYY-MM-DD उपयोग करें।",
        "result": "आपका मूलांक परिणाम"
    }
}

@app.get("/")
def home():
    return {"message": "NUMs API is LIVE 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/mulank")
def mulank(dob: str = Query(...), lang: str = Query("en")):
    lang = lang if lang in messages else "en"

    try:
        date_obj = datetime.strptime(dob, "%Y-%m-%d")
    except ValueError:
        return {"error": messages[lang]["invalid_date"]}

    day = date_obj.day
    mulank = sum(int(d) for d in str(day))
    while mulank > 9:
        mulank = sum(int(d) for d in str(mulank))

    lucky_number = mulank + 7

    if lang == "hi":
        return {
            "जन्मतिथि": dob,
            "मूलांक": mulank,
            "लकी नंबर": lucky_number
        }

    return {
        "dob": dob,
        "mulank": mulank,
        "lucky_number": lucky_number
    }
