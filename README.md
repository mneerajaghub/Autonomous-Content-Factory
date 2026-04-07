# Autonomous Content Factory

## Project Title
Autonomous Content Factory

## The Problem
Creating high-quality, fact-checked content is time-consuming and requires significant manual effort. This project addresses the challenge of automating content generation while ensuring factual accuracy.

## The Solution
The Autonomous Content Factory automates the process of content generation and fact-checking using a FastAPI backend and a simple frontend interface. It integrates mock responses for OpenAI API calls to demonstrate the pipeline's functionality. Key features include endpoints for fact-checking, content generation, and a full pipeline integration.

### Note:
The mock system is designed to simulate real functionality. It dynamically generates content based on the input topic but may use predefined templates or varied phrasing for demonstration purposes. The real functionality, when connected to the OpenAI API, would provide more sophisticated and contextually relevant outputs.

## Tech Stack
- **Programming Languages**: Python, JavaScript
- **Frameworks**: FastAPI
- **Databases**: None (mock responses used for demonstration)
- **APIs or Third-party Tools**: None (mock responses replace external API calls)

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd Autonomous-Content-Factory
   ```
3. Set up a virtual environment:
   ```bash
   python -m venv .venv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
5. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
6. Run the backend server:
   ```bash
   uvicorn backend.main:app --reload
   ```
7. Open the `index.html` file in the `frontend` folder to access the frontend interface.

---

## Source Code
The complete source code is available on GitHub: [GitHub Repository](https://github.com/mneerajaghub/Autonomous-Content-Factory.git)

## Demo Video
You can view the demo video of the project [here](https://drive.google.com/drive/folders/1ZBXvymwcxUezgUPYSQuWIsqV1VyKRUJe).

## Hosted Link (Optional)
- **Live URL**: [Hosted Application](<live-url>)