from flask import Blueprint, jsonify, request
from _storage.db_data_manager import SQLiteDataManager
from _storage.db_instance import db
from datetime import datetime
import os
import json

api = Blueprint("api", __name__)
data_manager = SQLiteDataManager(db)

@api.route("/users", methods=["GET"])
def get_users():
    try:
        users = data_manager.get_all_users()
        users_list = []
        for user in users:
            users_list.append(user.to_dict())
        
        return jsonify(users_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route("/users/<int:user_id>/movies", methods=["GET"])
def get_user_movies(user_id):
    try:
        user = data_manager.get_user(user_id)
        if user:
            movie_list = []
            movies = user.movies
            for movie in movies:
                movie_list.append(movie.to_dict())
                
            return jsonify(movie_list), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route("/users/<int:user_id>/movies", methods=["POST"])
def add_user_movie(user_id):
    try:
        movie_data = request.json
        movie_title = movie_data.get("movie_title")
        release_date = movie_data.get("release_date")
        directory = movie_data.get("directory")
        movie_rating = movie_data.get("movie_rating")

        if release_date:
            release_date = datetime.strptime(release_date, "%Y-%m-%d").date()

        data_manager.add_movie(
            movie_title, release_date, directory, movie_rating, user_id
        )
        
        return jsonify({"message": "Movie added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500