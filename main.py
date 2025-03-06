import os
from typing import List, Optional
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import httpx
from pydantic import BaseModel
import json
from prompt_templates import PODCAST_INTERVIEW_PROMPT
from dotenv import load_dotenv
load_dotenv()
app = FastAPI(title="Podcast Interview Question Generator")

# Set up templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuration for open-webui API
WEBUI_ENABLED = True
WEBUI_BASE_URL = "https://chat.ivislabs.in/api"
API_KEY = os.getenv("API_KEY")  # Use environment variable for security
DEFAULT_MODEL = "gemma2:2b"

# Fallback to local Ollama API if needed
OLLAMA_ENABLED = True
OLLAMA_HOST = "localhost"
OLLAMA_PORT = "11434"
OLLAMA_API_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api"

# Validate API Key
if WEBUI_ENABLED and not API_KEY:
    raise ValueError("API_KEY is missing. Please set it in your environment variables.")

class GenerationRequest(BaseModel):
    guest_name: str
    expertise: str
    num_questions: int = 5
    tone: Optional[str] = "professional"

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate_questions(
    guest_name: str = Form(),
    expertise: str = Form(),
    num_questions: int = Form(5),
    tone: str = Form("professional"),
    model: str = Form(DEFAULT_MODEL)
):
    try:
        num_questions = int(num_questions)
        prompt = PODCAST_INTERVIEW_PROMPT.format(
            guest_name=guest_name,
            expertise=expertise,
            num_questions=num_questions,
            tone=tone
        )
        print(f"Generated Prompt: {prompt}")
        if WEBUI_ENABLED:
            try:
                messages = [{"role": "user", "content": prompt}]
                request_payload = {"model": model, "messages": messages}
                print("Sending request to WebUI...")

                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{WEBUI_BASE_URL}/chat/completions",
                        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
                        json=request_payload,
                        timeout=60.0
                    )
                    print(f"WebUI Response Status: {response.status_code}")
                    print(f"WebUI Response Text: {response.text}")
                    
                    if response.status_code == 200:
                        result = response.json()
                        generated_text = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                        if generated_text:
                            return {"generated_questions": generated_text}
            except Exception as e:
                print(f"Open-webui API attempt failed: {str(e)}")

        if OLLAMA_ENABLED:
            try:
                print("Sending request to Ollama...")
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{OLLAMA_API_URL}/generate",
                        json={"model": model, "prompt": prompt, "stream": False},
                        timeout=60.0
                    )
                    print(f"Ollama Response Status: {response.status_code}")
                    print(f"Ollama Response Text: {response.text}")

                    if response.status_code == 200:
                        result = response.json()
                        return {"generated_questions": result.get("response", "")}
            except Exception as e:
                print(f"Ollama API attempt failed: {str(e)}")
                
        raise HTTPException(status_code=500, detail="Failed to generate questions")
    except Exception as e:
        print(f"Error generating questions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating questions: {str(e)}")

@app.get("/models")
async def get_models():
    try:
        if WEBUI_ENABLED:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{WEBUI_BASE_URL}/models", headers={"Authorization": f"Bearer {API_KEY}"})
                if response.status_code == 200:
                    models_data = response.json()
                    model_names = [model["id"] for model in models_data.get("data", []) if "id" in model]
                    return {"models": model_names}
        
        if OLLAMA_ENABLED:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{OLLAMA_API_URL}/tags")
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    return {"models": [model.get("name") for model in models]}
        
        return {"models": [DEFAULT_MODEL, "gemma2:2b", "qwen2.5:0.5b", "deepseek-r1:1.5b", "deepseek-coder:latest"]}
    except Exception as e:
        print(f"Unexpected error in get_models: {str(e)}")
        return {"models": [DEFAULT_MODEL]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)