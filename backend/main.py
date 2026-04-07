from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI  # Updated OpenAI import
import random

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

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Add a flag to toggle between mock and real API calls
USE_MOCK = True

# Mock function for fact-checking
def generate_fact_sheet_mock(text):
    text = text.lower()

    # Predefined mock data for specific topics
    predefined_topics = {
        "fuel": {
            "features": [
                "On-demand fuel delivery",
                "Mobile app ordering",
                "Real-time tracking"
            ],
            "target_audience": "Vehicle owners and fleet operators",
            "key_points": [
                "Saves time",
                "Avoids fuel station queues",
                "Convenient doorstep service"
            ]
        },
        "food": {
            "features": [
                "Online food ordering",
                "Fast delivery",
                "Restaurant integration"
            ],
            "target_audience": "Food lovers and busy professionals",
            "key_points": [
                "Quick meals",
                "Wide variety",
                "Convenience"
            ]
        }
    }

    # Check if the topic matches predefined topics
    for keyword, data in predefined_topics.items():
        if keyword in text:
            return {
                **data,
                "unclear_info": []
            }

    # Default dynamic generation for other topics with varied wording
    synonyms = ["solutions", "innovations", "technologies", "platforms"]
    random_synonym = random.choice(synonyms)

    return {
        "features": [
            f"Cutting-edge {random_synonym} for {text}",
            f"Advanced tools to enhance {text}",
            f"User-friendly interfaces for better {text} management"
        ],
        "target_audience": f"Professionals and enthusiasts in the field of {text}",
        "key_points": [
            f"Boosts {text} efficiency",
            f"Delivers measurable improvements in {text}",
            f"Simplifies complex {text} workflows"
        ],
        "unclear_info": []
    }

# Mock function for content generation
def generate_content_mock(fact_sheet, user_input):
    return {
        "blog": f"This platform is designed for {fact_sheet['target_audience']}. It offers features like {', '.join(fact_sheet['features'])}. Key benefits include {', '.join(fact_sheet['key_points'])}. Overall, it provides a reliable and efficient solution for modern needs.",
        
        "social_media_posts": [
            f"🚀 Discover a solution for {fact_sheet['target_audience']}!",
            f"✨ Features: {', '.join(fact_sheet['features'])}",
            f"⏱ Benefits: {fact_sheet['key_points'][0]}",
            f"📢 Designed for convenience and efficiency",
            f"🔥 Try it today!"
        ],
        
        "email_teaser": f"Introducing a solution for {fact_sheet['target_audience']} with features like {', '.join(fact_sheet['features'])}. Experience {fact_sheet['key_points'][0]} today!"
    }

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

# Function to generate a Fact-Sheet from user input
@app.post("/fact-check", response_model=FactSheet)
def fact_check(input_data: FactCheckInput):
    if not input_data.text and not input_data.url:
        raise HTTPException(status_code=400, detail="Either 'text' or 'url' must be provided.")

    if USE_MOCK:
        return generate_fact_sheet_mock(input_data.text or input_data.url)

    prompt = f"Extract features, target audience, and key points from the following content:\n{input_data.text or input_data.url}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Extract features, target audience, and key points from the given text. Return ONLY JSON."
                },
                {
                    "role": "user",
                    "content": input_data.text
                }
            ]
        )

        result = response.choices[0].message.content

        import json
        parsed = json.loads(result)

        return FactSheet(
            features=parsed.get("features", []),
            target_audience=parsed.get("target_audience", ""),
            key_points=parsed.get("key_points", []),
            unclear_info=parsed.get("unclear_info", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing input: {str(e)}")

# Endpoint for content generation
@app.post("/generate-content", response_model=GeneratedContent)
def generate_content(input_data: ContentGenerationInput):
    print("Input Data:", input_data)  # Log input data

    if USE_MOCK:
        mock_output = generate_content_mock(
            {
                "features": input_data.features,
                "target_audience": input_data.target_audience,
                "key_points": input_data.key_points,
            },
            input_data.target_audience
        )
        print("Mock Output:", mock_output)  # Log mock output
        return mock_output

    prompt = (
        f"Generate a blog, social media posts, and an email teaser based on the following fact-sheet:\n"
        f"Features: {', '.join(input_data.features)}\n"
        f"Target Audience: {input_data.target_audience}\n"
        f"Key Points: {', '.join(input_data.key_points)}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Generate blog, social media posts, and email teaser from the given fact sheet. Return in JSON format with keys: blog, social_media_posts, email_teaser."
                },
                {
                    "role": "user",
                    "content": f"""
                    Features: {input_data.features}
                    Target Audience: {input_data.target_audience}
                    Key Points: {input_data.key_points}
                    """
                }
            ]
        )

        result = response.choices[0].message.content

        import json
        parsed = json.loads(result)

        return GeneratedContent(
            blog=parsed.get("blog", ""),
            social_media_posts=parsed.get("social_media_posts", []),
            email_teaser=parsed.get("email_teaser", "")
        )
    except Exception as e:
        print("Error:", str(e))  # Log the error
        raise HTTPException(status_code=500, detail=f"Error generating content: {str(e)}")

# Endpoint for full pipeline: fact-check + content generation
@app.post("/generate-full-content", response_model=dict)
def generate_full_content(input_data: FactCheckInput):
    if not input_data.text:
        raise HTTPException(status_code=400, detail="'text' must be provided.")

    try:
        # Step 1: Generate Fact-Sheet
        fact_sheet = fact_check(input_data)

        # Safe conversion of fact_sheet to ensure it's a Pydantic object
        if isinstance(fact_sheet, dict):
            fact_sheet = FactSheet(**fact_sheet)

        # Step 2: Pass Fact-Sheet to Content Generator
        content_input = ContentGenerationInput(
            features=fact_sheet.features,
            target_audience=fact_sheet.target_audience,
            key_points=fact_sheet.key_points
        )
        generated_content = generate_content(content_input)

        # Ensure dict format
        if not isinstance(generated_content, dict):
            generated_content = generated_content.dict()

        print("FINAL OUTPUT:", generated_content)  # Debugging log

        # Step 3: Return both Fact-Sheet and Generated Content
        return {
            "fact_sheet": fact_sheet if isinstance(fact_sheet, dict) else fact_sheet.dict(),
            "generated_content": generated_content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating full content: {str(e)}")