from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import random
import re
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Models
# -----------------------------
class FactCheckInput(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None

class FactSheet(BaseModel):
    features: list[str]
    target_audience: str
    key_points: list[str]
    unclear_info: Optional[list[str]] = []

class ContentGenerationInput(BaseModel):
    features: list[str]
    target_audience: str
    key_points: list[str]

class GeneratedContent(BaseModel):
    blog: str
    social_media_posts: list[str]
    email_teaser: str

# -----------------------------
# Helper: Clean weird JSON text
# -----------------------------
def clean_text(text: str) -> str:
    if not text:
        return ""
    # Remove JSON-like patterns
    text = re.sub(r"\{.*?\}", "", text)
    return text.strip()

# -----------------------------
# Dynamic Fact Sheet Generator
# -----------------------------
def generate_fact_sheet_dynamic(user_input: str):
    text = user_input.lower()

    if "fuel" in text:
        return {
            "features": ["On-demand fuel delivery", "Mobile app ordering", "Real-time tracking"],
            "target_audience": "Vehicle owners and fleet operators",
            "key_points": ["Saves time", "Avoids fuel station queues", "Doorstep convenience"]
        }

    elif "ai" in text:
        return {
            "features": ["AI automation", "Smart analytics", "User-friendly interface"],
            "target_audience": "Businesses and tech enthusiasts",
            "key_points": ["Improves efficiency", "Reduces manual work", "Enhances decision making"]
        }

    elif "health" in text:
        return {
            "features": ["Digital health tracking", "AI diagnostics", "Remote consultation"],
            "target_audience": "Patients and healthcare professionals",
            "key_points": ["Better healthcare access", "Early diagnosis", "Improved patient care"]
        }

    elif "education" in text:
        return {
            "features": ["Online courses", "Interactive learning tools", "Personalized progress tracking"],
            "target_audience": "Students and educators",
            "key_points": ["Flexible learning", "Affordable education", "Engaging content"]
        }

    elif "fitness" in text:
        return {
            "features": ["Workout plans", "Nutrition tracking", "Progress monitoring"],
            "target_audience": "Fitness enthusiasts and trainers",
            "key_points": ["Achieve goals faster", "Stay motivated", "Track progress easily"]
        }

    elif "travel" in text:
        return {
            "features": ["Itinerary planning", "Budget-friendly options", "Local guides"],
            "target_audience": "Travelers and adventurers",
            "key_points": ["Explore new places", "Save money", "Travel hassle-free"]
        }

    # Default fallback
    return {
        "features": ["Smart automation", "User-friendly interface", "Scalable solution"],
        "target_audience": "General users",
        "key_points": ["Saves time", "Improves efficiency", "Easy to use"]
    }

# -----------------------------
# Dynamic Content Generator
# -----------------------------
def generate_content_mock(fact_sheet):
    features = fact_sheet["features"]
    audience = clean_text(fact_sheet["target_audience"])
    points = fact_sheet["key_points"]

    # Blog templates
    blog_templates = [
        f"Imagine a solution built specifically for {audience}. With features like {', '.join(features)}, it transforms user experience. Key benefits include {', '.join(points)}, making it a powerful modern solution.",

        f"In today’s fast-paced world, {audience} need smarter tools. This platform offers {', '.join(features)} and helps users by {', '.join(points)}.",

        f"This innovative platform targets {audience} with features like {', '.join(features)}. It ensures {', '.join(points)} while improving overall efficiency."
    ]

    # Social media templates
    social_templates = [
        [
            f"🚀 Built for {audience}!",
            f"✨ Features: {', '.join(features)}",
            f"🔥 {points[0]}",
            "📢 Smarter. Faster. Better.",
            "💡 Try it today!"
        ],
        [
            f"🎯 Perfect for {audience}",
            f"⚙️ {features[0]} + {features[1]}",
            f"⏱ {points[0]}",
            "🚀 Upgrade your workflow",
            "✨ Experience the difference"
        ],
        [
            f"💥 Game changer for {audience}",
            f"📦 {', '.join(features)}",
            f"✅ {', '.join(points)}",
            "🔥 Don't miss out",
            "🚀 Start now!"
        ]
    ]

    # Email templates
    email_templates = [
        f"Discover a smarter solution for {audience}. With features like {', '.join(features)}, you can now {points[0]} easily.",

        f"Looking to improve efficiency? Our platform for {audience} offers {', '.join(features)} to help you {points[0]}.",

        f"Introducing a powerful solution for {audience}. Experience {', '.join(features)} and enjoy {points[0]}."
    ]

    return {
        "blog": random.choice(blog_templates),
        "social_media_posts": random.choice(social_templates),
        "email_teaser": random.choice(email_templates)
    }

# -----------------------------
# API: Fact Check
# -----------------------------
@app.post("/fact-check", response_model=FactSheet)
def fact_check(input_data: FactCheckInput):
    if not input_data.text:
        raise HTTPException(status_code=400, detail="Text is required")

    result = generate_fact_sheet_dynamic(input_data.text)

    return FactSheet(
        features=result["features"],
        target_audience=result["target_audience"],
        key_points=result["key_points"],
        unclear_info=[]
    )

# -----------------------------
# API: Generate Content
# -----------------------------
@app.post("/generate-content", response_model=GeneratedContent)
def generate_content(input_data: ContentGenerationInput):
    fact_sheet = {
        "features": input_data.features,
        "target_audience": input_data.target_audience,
        "key_points": input_data.key_points
    }

    result = generate_content_mock(fact_sheet)

    return GeneratedContent(
        blog=result["blog"],
        social_media_posts=result["social_media_posts"],
        email_teaser=result["email_teaser"]
    )

# -----------------------------
# API: Full Pipeline
# -----------------------------
@app.post("/generate-full-content")
def generate_full_content(input_data: FactCheckInput):
    if not input_data.text:
        raise HTTPException(status_code=400, detail="Text is required")

    fact_sheet = generate_fact_sheet_dynamic(input_data.text)
    generated_content = generate_content_mock(fact_sheet)

    return {
        "fact_sheet": fact_sheet,
        "generated_content": generated_content
    }