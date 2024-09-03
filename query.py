import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = "chat-gpt-3-5-turbo2.p.rapidapi.com" 


def fetch_movie_details_from_omdb(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "Released" in data and data["Released"] != "N/A":
            try:
                data["Released"] = datetime.strptime(
                    data["Released"], "%d %b %Y"
                ).date()
            except ValueError:
                data["Released"] = None
        return data
    else:
        return None


def get_movie_recommendation(query):
    url = f"https://{RAPIDAPI_HOST}/chat/completions"

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Suggest some movies for: {query}"}
        ],
        "max_tokens": 150,
        "temperature": 0.7,
        "n": 1
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        recommendations = data['choices'][0]['message']['content'].strip()
        return recommendations
    except requests.exceptions.RequestException as e:
        print(f"Error fetching recommendation: {e}")
        return None
