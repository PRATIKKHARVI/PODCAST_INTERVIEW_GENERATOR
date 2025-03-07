## Podcast Interview Questions Generator (Overview)

The Podcast Interview Questions Generator is a web application designed to help podcasters create structured, engaging interview questions for their guests. It uses advanced language models through Open WebUI or local Ollama to generate customized questions based on the selected topic and interview style.

## Features

- Generate tailored interview questions based on the selected topic
- Choose the number of questions (5, 10, 15, or 20)
- Select interview tone (formal, casual, humorous, etc.)
- Include or exclude follow-up questions for a deeper conversation
- Select from available language models
- Copy results to clipboard with one click
- Responsive design for both desktop and mobile users

## Prerequisites

- Python 3.8+
- FastAPI and its dependencies
- Access to Open WebUI (https://chat.ivislabs.in) and/or local Ollama installation

## Installation Steps

1. *Create Project Structure*
   - Set up the project directory
   - Create necessary subdirectories for templates and static files

2. *Install Dependencies*
   - Install FastAPI, Uvicorn, Jinja2, HTTPX, and other required packages

3. *Configure API Settings*
   - Update the API key for Open WebUI if needed
   - Configure local Ollama settings if using it as a fallback

4. *Start the Application*
   - Run the FastAPI application with Uvicorn:
     sh
     uvicorn main:app --reload
     
   - Access the application at http://localhost:8000

## Using the Application

### Step 1: Set Your Interview Parameters
1. Enter the interview topic (e.g., "startup growth strategies", "mental health awareness")
2. Select the number of questions you want
3. Choose the interview tone
4. Decide whether to include follow-up questions
5. Select the preferred language model

### Step 2: Generate Questions
1. Click the "Generate Questions" button
2. Wait for the system to generate customized questions
3. View the results in the designated section

### Step 3: Use Your Questions
1. Review the generated interview questions
2. Use the "Copy to Clipboard" button to save them
3. Integrate them into your podcast interview planning

## How It Works

1. *User Inputs Parameters*
   - The user fills out the form with their interview preferences

2. *Application Sends Request to LLM*
   - The application constructs a prompt based on user inputs
   - It first attempts to connect to Open WebUI
   - Falls back to local Ollama if Open WebUI is unavailable

3. *LLM Generates Questions*
   - The language model processes the prompt
   - Returns structured and relevant interview questions

4. *Results Display*
   - The application formats the response neatly
   - Displays the generated questions for user review

## Troubleshooting

### API Connection Issues
- Ensure the API key is correct
- Check if Open WebUI is accessible from your network
- Review application logs for specific error messages

### No Models Available
- Confirm that the API is working properly
- Check for installed models if using local Ollama
- The application will use a default list if no models are found

### Generation Errors
- Try a different language model
- Simplify your request (fewer questions, no follow-ups)
- Ensure the prompt is properly structured

## Customization Options

- Modify prompt templates for different interview styles
- Adjust UI styling to match your branding
- Configure different LLM providers by updating API endpoints
- Add additional generation options based on your needs
