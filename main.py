from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# Important for Render health check
app = FastAPI(
    title="NUMs API",
    version="1.0.0"
)

# ✅ CORS enabled (frontend can call API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change later to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🌍 Language messages
messages = {
    "en": {
        "welcome": "Welcome to NUMs API! Use /mulank?dob=YYYY-MM-DD&lang=en",
        "invalid_date": "Invalid date format. Use YYYY-MM-DD.",
        "result": "Your Numerology Result"
    },
    "hi": {
        "welcome": "NUMs API में आपका स्वागत है! /mulank?dob=YYYY-MM-DD&lang=hi का उपयोग करें",
        "invalid_date": "गलत तारीख प्रारूप। YYYY-MM-DD उपयोग करें।",
        "result": "आपका मूलांक परिणाम"
    }
}

# ✅ Root route (prevents 404 on homepage)
@app.get("/")
def home(lang: str = Query("en")):
    lang = lang if lang in messages else "en"
    return {
        "message": messages[lang]["welcome"],
        "status": "API is running 🚀"
    }

# ✅ Health check route (Render uses this internally)
@app.get("/health")
def health():
    return {"status": "ok"}

# 🔢 Mulank Endpoint
@app.get("/mulank")
def mulank(
    dob: str = Query(..., description="Date of Birth YYYY-MM-DD"),
    lang: str = Query("en")
):
    lang = lang if lang in messages else "en"

    # Validate date format
    try:
        date_obj = datetime.strptime(dob, "%Y-%m-%d")
    except ValueError:
        return {"error": messages[lang]["invalid_date"]}

    # Calculate Mulank (digit sum of day)
    day = date_obj.day
    mulank = sum(int(d) for d in str(day))
    while mulank > 9:
        mulank = sum(int(d) for d in str(mulank))

    lucky_number = mulank + 7

    # Multilingual response
    if lang == "hi":
        return {
            "संदेश": messages[lang]["result"],
            "जन्मतिथि": dob,
            "मूलांक": mulank,
            "लकी नंबर": lucky_number
        }
    else:
        return {
            "message": messages[lang]["result"],
            "dob": dob,
            "mulank": mulank,
            "lucky_number": lucky_number
        }
