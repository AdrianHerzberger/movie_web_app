import os
import unittest
from datetime import datetime
from app import app, db, data_manager
from _storage.user_storage import User
from _storage.movie_storage import Movie


class TestUserStorage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_db_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "test_movies_data.sqlite",
        )
        
        print(f"Test DB path: {cls.test_db_path}")

        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{cls.test_db_path}"
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.session.remove()
            db.drop_all()
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

    def test_add_user(self):
        with app.app_context():
            data_manager.add_user("John", "Doe", datetime(1990, 1, 1).date())
            user = User.query.filter_by(first_name="John", last_name="Doe").first()

            self.assertIsNotNone(user)
            self.assertEqual(user.first_name, "John")
            self.assertEqual(user.last_name, "Doe")
            self.assertEqual(user.birth_date.strftime("%Y-%m-%d"), "1990-01-01")

    def test_add_movie(self):
        with app.app_context():
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
            self.assertEqual(movie.movie_rating, None)
            self.assertEqual(movie.user_id, 3)


if __name__ == "__main__":
    unittest.main()
