# Autonomous Content Factory

## Project Title
Autonomous Content Factory

## The Problem
Manually rewriting content for multiple platforms is repetitive, time-consuming, and prone to inconsistencies. This process delays product launches and causes creative burnout for marketing teams.

## The Solution
Autonomous Content Factory automates the process of content creation by using AI to verify facts and generate platform-specific content. The system ensures consistency, reduces manual effort, and accelerates the content production pipeline. Key features include fact-checking, structured fact-sheet generation, and multi-platform content creation (blogs, social media posts, and email teasers).

## Tech Stack
- **Programming Languages**: Python, JavaScript
- **Frameworks**: FastAPI (Backend), HTML/CSS/JavaScript (Frontend)
- **APIs**: OpenAI (mocked for development)
- **Databases**: None (current implementation is stateless)

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- Node.js (optional, for frontend development)

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Autonomous-Content-Factory
   ```
2. Set up a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
4. Start the backend server:
   ```bash
   uvicorn backend.main:app --reload
   ```
5. Open the `frontend/index.html` file in a browser to access the frontend.

---

## Source Code
The complete source code is available on GitHub: [GitHub Repository](<repository-url>)

## Video Demo
- **Duration**: 2-3 minutes
- **Content**:
  - Demonstrates the working application
  - Highlights key features and user flow
  - Shows a real usage scenario

## Hosted Link (Optional)
- **Live URL**: [Hosted Application](<live-url>)