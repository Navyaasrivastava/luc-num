from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI(title="NUMs API", version="1.0")

# ✅ CORS (frontend can access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🌍 Multilingual messages
messages = {
    "en": {
        "welcome": "Welcome to NUMs API 🚀",
        "invalid_date": "Invalid date format. Use YYYY-MM-DD.",
        "result": "Your Numerology Result"
    },
    "hi": {
        "welcome": "NUMs API में आपका स्वागत है 🚀",
        "invalid_date": "गलत तारीख प्रारूप। YYYY-MM-DD उपयोग करें।",
        "result": "आपका मूलांक परिणाम"
    }
}

# ✅ Root route (no 404)
@app.get("/")
def home(lang: str = Query("en")):
    lang = lang if lang in messages else "en"
    return {
        "message": messages[lang]["welcome"],
        "usage": "/mulank?dob=2005-08-15&lang=en"
    }

# ✅ Health check (Render uses this)
@app.get("/health")
def health():
    return {"status": "ok"}

# 🔢 Mulank API
@app.get("/mulank")
def mulank(dob: str = Query(...), lang: str = Query("en")):
    lang = lang if lang in messages else "en"

    # Validate date
    try:
        date_obj = datetime.strptime(dob, "%Y-%m-%d")
    except ValueError:
        return {"error": messages[lang]["invalid_date"]}

    # Mulank calculation (digit sum of day)
    day = date_obj.day
    mulank = sum(int(d) for d in str(day))
    while mulank > 9:
        mulank = sum(int(d) for d in str(mulank))

    lucky_number = mulank + 7

    # 🌍 Multilingual response
    if lang == "hi":
        return {
            "संदेश": messages[lang]["result"],
            "जन्मतिथि": dob,
            "मूलांक": mulank,
            "लकी नंबर": lucky_number
        }

    return {
        "message": messages[lang]["result"],
        "dob": dob,
        "mulank": mulank,
        "lucky_number": lucky_number
    }

