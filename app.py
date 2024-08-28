from flask import Flask, render_template, flash, request, redirect, url_for
from _storage.db_data_manager import SQLiteDataManager
import os
import requests
from datetime import datetime
from _storage.db_instance import db
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = "supersecretkey"

database_path = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "_data", "movies_data.sqlite"
)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path}"
db.init_app(app)
data_manager = SQLiteDataManager(db)

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

def fetch_movie_details_from_omdb(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "Released" in data and data["Released"] != "N/A":
            try:
                data["Released"] = datetime.strptime(data["Released"], "%d %b %Y").date()
            except ValueError:
                data["Released"] = None
        return data
    else:
        return None
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/", methods=["GET"])
def home():
    if request.method == "GET":
        try:
            movies = data_manager.get_all_movies()
            users = data_manager.get_all_users()
        except Exception as e:
            flash(f"Error fethcing movies or users: {str(e)}")
            
        return render_template("index.html", movies=movies, users=users)
    
    
@app.route("/users", methods=["GET"])
def list_users():
    if request.method == "GET":
        
        try:
            users = data_manager.get_all_users()
        except Exception as e:
            flash(f"Error fetching users: {str(e)}")
    
    return render_template("users.html", users=users)    


@app.route("/add_user", methods=["GET", "POST"])    
def add_user():
    if request.method == "POST":
        first_name = request.form["firstname"]
        last_name = request.form["lastname"]
        birth_date = request.form["birthdate"]
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
        
        try:
            data_manager.add_user(first_name, last_name, birth_date)
            flash(f"User: {first_name} {last_name} added successfully!")
        except Exception as e:
            flash(f"Error adding user: {str(e)}")
            
        return redirect(url_for("add_user"))

    return render_template("add_user.html")


@app.route("/add_movie", methods=["GET", "POST"])
def add_movie():
    if request.method == "POST":
        movie_title = request.form["movietitle"]
        release_date = request.form["releasedate"]
        directory = request.form["directory"]
        movie_rating = request.form["movierating"]
        user_id = request.form["userid"]

        omdb_data = fetch_movie_details_from_omdb(movie_title)
        
        if omdb_data:
            full_title = omdb_data.get("Title", movie_title)
            movie_title = full_title.split(" AKA:")[0].strip() 
            release_date = omdb_data.get("Released", "N/A") 
            directory = omdb_data.get("Director", directory)
            movie_rating = omdb_data.get("imdbRating", movie_rating)
            
        if release_date and release_date != "N/A":
            try:
                if isinstance(release_date, str) and release_date:
                    release_date = datetime.strptime(release_date, "%Y-%m-%d").date()
            except ValueError:
                release_date = None
        else:
            release_date = None
            
        try:
            movie_rating = float(movie_rating)
        except ValueError:
            movie_rating = None
        
        try:
            data_manager.add_movie(
                movie_title, release_date, directory, movie_rating, user_id
            )
            flash(f"Movie: {movie_title} added successfully!")
        except Exception as e:
            flash(f"Error adding movie: {str(e)}")

        return redirect(url_for("add_movie"))

    users = data_manager.get_all_users()

    return render_template("add_movie.html", users=users)


@app.route("/update_movie/<int:movie_id>/", methods=["GET", "POST"])
def update_movie(movie_id):
    movie = data_manager.get_movie_by_id(movie_id)
    users = data_manager.get_all_users()

    if not movie:
        flash("Movie not found.")
        return redirect(url_for("home"))

    if request.method == "POST":
        movie_title = request.form.get("movietitle", movie.movie_title)
        release_date = request.form.get("releasedate", movie.release_date)
        directory = request.form.get("directory", movie.directory)
        movie_rating = request.form.get("movierating", movie.movie_rating)
        user_id = request.form.get("userid", movie.user_id)

        if isinstance(release_date, str) and release_date:
            release_date = datetime.strptime(release_date, "%Y-%m-%d").date()
            
        try:
            data_manager.update_movie(
                movie_id, movie_title, release_date, directory, movie_rating, user_id
            )
            flash(f"Movie {movie_title} updated successfully!")
        except Exception as e:
            flash(f"Error updating movie: {str(e)}")
            
        return redirect(url_for("update_movie", movie_id=movie_id))

    return render_template("update_movie.html", movie=movie, users=users)


@app.route("/users/<int:user_id>/delete_movie/<int:movie_id>/", methods=["GET", "POST"])
def delete_movie(user_id, movie_id):
    if request.method == "POST":
        user = data_manager.get_user(user_id)
        if user:
            try:
                data_manager.delete_movie(movie_id)
                flash("Movie deleted successfully!")
            except Exception as e:
                flash(f"Error updating movie: {str(e)}")

    return render_template("delete_movie.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
