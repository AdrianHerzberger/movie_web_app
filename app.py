from flask import Flask, render_template, flash, request, redirect, url_for
from _storage.db_data_manager import SQLiteDataManager
import os
from datetime import datetime
from _storage.db_instance import db

app = Flask(__name__)
app.secret_key = "supersecretkey"

database_path = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "_data", "movies_data.sqlite"
)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path}"

db.init_app(app)

data_manager = SQLiteDataManager(db)


@app.route("/", methods=["GET"])
def home():
    if request.method == "GET":

        movies = data_manager.get_all_movies()

        return render_template("index.html", movies=movies)


@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        first_name = request.form["firstname"]
        last_name = request.form["lastname"]
        birth_date = request.form["birthdate"]
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()

        data_manager.add_user(first_name, last_name, birth_date)

        flash(f"User: {first_name} {last_name} added successfully!")
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

        release_date = datetime.strptime(release_date, "%Y-%m-%d").date()

        data_manager.add_movie(
            movie_title, release_date, directory, movie_rating, user_id
        )

        flash(f"Movie {movie_title} added successfully!")
        return redirect(url_for("add_movie"))

    users = data_manager.get_all_users()

    return render_template("add_movie.html", users=users)


@app.route("/update_movie/<int:movie_id>/", methods=["GET", "POST"])
def update_movie(movie_id):
    if request.method == "POST":
        movie_title = request.form.get("movietitle", "")
        release_date = request.form.get("releasedate", "")
        directory = request.form.get("directory", "")
        movie_rating = request.form.get("movierating", "")
        user_id = request.form.get("userid", "")

        if release_date:
            release_date = datetime.strptime(release_date, "%Y-%m-%d").date()

        data_manager.update_movie(
            movie_id, movie_title, release_date, directory, movie_rating, user_id
        )

        flash(f"Movie {movie_title} updated successfully!")
        return redirect(url_for("update_movie", movie_id=movie_id))

    movie = data_manager.get_movie_by_id(movie_id)
    users = data_manager.get_all_users()

    if not movie:
        flash("Movie not found.")
        return redirect(url_for("home"))

    return render_template("update_movie.html", movie=movie, users=users)


@app.route("/delete_movie/<int:movie_id>/", methods=["GET", "POST"])
def delete_movie(movie_id):
    if request.method == "POST":
        data_manager.delete_movie(movie_id)

        flash(f"Movie deleted sucessfully!")

    return render_template("delete_movie.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
