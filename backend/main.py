from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define input model for fact-checking
class FactCheckInput(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None

# Define output model for fact-sheet
class FactSheet(BaseModel):
    features: list[str]
    target_audience: str
    key_points: list[str]
    unclear_info: Optional[list[str]] = None

# Define input model for content generation
class ContentGenerationInput(BaseModel):
    features: list[str]
    target_audience: str
    key_points: list[str]

# Define output model for generated content
class GeneratedContent(BaseModel):
    blog: str
    social_media_posts: list[str]
    email_teaser: str

# Mock flag to toggle between real and mock responses
USE_MOCK = True

def generate_fact_sheet_mock(text):
    return {
        "features": [
            "Automated content generation",
            "Multi-platform output",
            "Consistent messaging"
        ],
        "target_audience": "Marketing teams and content creators",
        "key_points": [
            "Saves time",
            "Improves consistency",
            "Reduces manual effort"
        ],
        "unclear_info": []
    }

def generate_content_mock(fact_sheet, user_input):
    return {
        "blog": f"This AI-powered platform helps {user_input} generate high-quality content across blogs, social media, and email campaigns. By using a structured fact-sheet approach, it ensures consistency and accuracy in messaging. This reduces manual effort and speeds up content production, making it ideal for fast-paced marketing environments.",
        "social_media_posts": [
            f"1. 🚀 Automate your content creation with AI for {user_input}!",
            "2. ✨ Consistent messaging across all platforms",
            "3. ⏱ Save time and boost productivity",
            "4. 📢 Perfect for marketing teams",
            "5. 🔥 One input, multiple outputs!"
        ],
        "email_teaser": f"Boost your marketing efficiency with AI-powered content generation tailored for {user_input} — consistent, fast, and reliable."
    }

# Endpoint for fact-checking
@app.post("/fact-check", response_model=FactSheet)
def fact_check(input_data: FactCheckInput):
    if not input_data.text and not input_data.url:
        raise HTTPException(status_code=400, detail="Either 'text' or 'url' must be provided.")

    if USE_MOCK:
        return generate_fact_sheet_mock(input_data.text or input_data.url)

    # Prepare the prompt for the LLM
    prompt = f"Extract features, target audience, and key points from the following content:\n{input_data.text or input_data.url}"

    try:
        response = client.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant that extracts structured information from text."},
                {"role": "user", "content": prompt}
            ]
        )
        result = response.choices[0].message.content.strip()
        # Placeholder parsing logic (update as needed)
        features = ["Feature 1", "Feature 2"]
        target_audience = "General Audience"
        key_points = ["Key point 1", "Key point 2"]
        unclear_info = ["Unclear detail 1"]

        return FactSheet(
            features=features,
            target_audience=target_audience,
            key_points=key_points,
            unclear_info=unclear_info
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing input: {str(e)}")

# Endpoint for content generation
@app.post("/generate-content", response_model=GeneratedContent)
def generate_content(input_data: ContentGenerationInput):
    if USE_MOCK:
        return generate_content_mock(input_data)

    # Prepare the prompt for the LLM
    prompt = (
        f"Generate a blog, social media posts, and an email teaser based on the following fact-sheet:\n"
        f"Features: {', '.join(input_data.features)}\n"
        f"Target Audience: {input_data.target_audience}\n"
        f"Key Points: {', '.join(input_data.key_points)}"
    )

    try:
        response = client.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant that generates platform-specific content."},
                {"role": "user", "content": prompt}
            ]
        )
        result = response.choices[0].message.content.strip()
        # Placeholder parsing logic (update as needed)
        blog = "This is a 500-word blog based on the fact-sheet."
        social_media_posts = [
            "Post 1: Key point 1",
            "Post 2: Key point 2",
            "Post 3: Feature 1",
            "Post 4: Feature 2",
            "Post 5: General Audience"
        ]
        email_teaser = "This is an email teaser based on the fact-sheet."

        return GeneratedContent(
            blog=blog,
            social_media_posts=social_media_posts,
            email_teaser=email_teaser
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating content: {str(e)}")

# Endpoint for full pipeline: fact-check + content generation
@app.post("/generate-full-content", response_model=GeneratedContent)
def generate_full_content(input_data: FactCheckInput):
    if not input_data.text:
        raise HTTPException(status_code=400, detail="'text' must be provided.")

    if USE_MOCK:
        fact_sheet = generate_fact_sheet_mock(input_data.text)
        return generate_content_mock(fact_sheet, input_data.text)

    # Real implementation would go here
    raise NotImplementedError("Real implementation is not yet available.")