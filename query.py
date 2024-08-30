import requests
import openai


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
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # or another engine such as gpt-4
            prompt=f"Suggest some movies for: {query}",
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        recommendations = response.choices[0].text.strip()
        return recommendations
    except Exception as e:
        print(f"Error fetching recommendation: {e}")
        return None