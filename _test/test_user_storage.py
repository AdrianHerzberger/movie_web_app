import os
import unittest
from flask import Flask
from flask_migrate import Migrate
from datetime import datetime
from _storage.db_data_manager import SQLiteDataManager
from _storage.db_instance import db
from _storage.user_storage import User
from _storage.movie_storage import Movie

test_app = Flask(__name__)
data_manager = SQLiteDataManager(db)

class TestUserStorage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        test_db_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "test_movies_data.sqlite",
        )

        print(f"Test DB path: {test_db_path}")
        
        test_app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{test_db_path}"
        test_app.config["TESTING"] = True
        test_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False#
        
        db.init_app(test_app)
        
        with test_app.app_context():
            db.create_all()
        
    @classmethod
    def tearDownClass(cls):
        with test_app.app_context():
            db.session.remove()
            db.drop_all()

        test_db_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "test_movies_data.sqlite",
        )

        # if os.path.exists(test_db_path):
        #     os.remove(test_db_path)

    def test_add_user(self):

        with test_app.app_context():

            data_manager.add_user("John", "Doe", datetime(1990, 1, 1).date())

            user = User.query.filter_by(first_name="John", last_name="Doe").first()

            self.assertIsNotNone(user)

            self.assertEqual(user.first_name, "John")

            self.assertEqual(user.last_name, "Doe")

            self.assertEqual(user.birth_date.strftime("%Y-%m-%d"), "1990-01-01")

    def test_add_movie(self):

        with test_app.app_context():

            data_manager.add_user("Jane", "Doe", datetime(1985, 5, 15).date())

            user = User.query.filter_by(first_name="Jane", last_name="Doe").first()

            data_manager.add_movie(
                movie_title="Test Movie",
                release_date=datetime(2016, 1, 16).date(),
                directory="N/A",
                movie_rating=8.5,
                user_id=user.id,
            )

            movie = Movie.query.filter_by(movie_title="Test Movie").first()

            self.assertIsNotNone(movie)

            self.assertEqual(movie.movie_title, "Test Movie")

            self.assertEqual(movie.release_date, datetime(2016, 1, 16).date())

            self.assertEqual(movie.directory, "N/A")

            self.assertEqual(movie.movie_rating, 8.5)

            self.assertEqual(movie.user_id, 1)


if __name__ == "__main__":
    unittest.main()