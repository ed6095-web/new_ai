from fastapi import FastAPI, Request
import openai
import os
import requests
import webbrowser

app = FastAPI()

# Set your OpenAI API key
openai.api_key = "your-openai-api-key"

# Task execution functions
def open_app(app_name):
    if "chrome" in app_name.lower():
        webbrowser.open("https://www.google.com")
        return "Opening Chrome..."
    elif "youtube" in app_name.lower():
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube..."
    return "I can't open this app yet!"

def get_weather(city):
    API_KEY = "your-weather-api-key"  # Use OpenWeather API
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()
    if response.get("main"):
        temp = response["main"]["temp"]
        return f"The temperature in {city} is {temp}°C."
    return "Couldn't fetch weather."

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    # Check for commands
    if "open" in user_message:
        return {"reply": open_app(user_message)}
    elif "weather" in user_message:
        city = user_message.split("weather in")[-1].strip()
        return {"reply": get_weather(city)}

    # Use OpenAI for chatbot response
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_message}]
    )
    return {"reply": response["choices"][0]["message"]["content"]}

# Run with: uvicorn main:app --reload
