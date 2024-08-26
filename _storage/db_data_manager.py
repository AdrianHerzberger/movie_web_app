from .user_storage import db, User
from .movie_storage import db, Movie
from .data_manager_interface import DataManagerInterface

class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_instance):
        self.db = db_instance
     
    def add_user(self, first_name, last_name, birth_date):
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
        )
        self.db.session.add(new_user)
        self.db.session.commit()
        
    def add_movie(self, movie_title, release_date, directory, movie_rating, user_id):
        new_movie = Movie(
            movie_title=movie_title,
            release_date=release_date,
            directory=directory,
            movie_rating=movie_rating,
            user_id=user_id
        )
        self.db.session.add(new_movie)
        self.db.session.commit()
              
    def get_all_users(self):
        return User.query.all()
    
    def get_all_movies(self):
        return Movie.query.all()
    
    def get_user_movies(self, user_id):
        user = User.query.get(user_id)
        if user:
            return user.movies  
        return None
    
    def update_movie(self, movie_id, movie_title, release_date, directory, movie_rating, user_id):
        movie = Movie.query.get(movie_id)
        if movie:
            movie.movie_title = movie_title
            movie.release_date = release_date
            movie.directory = directory
            movie.movie_rating = movie_rating
            movie.user_id = user_id  
            try:
                self.db.session.commit()
            except Exception as e:
                self.db.session.rollback()
                print(f"Error updating movie: {e}")
                return None
            return movie
        return None
    
    def get_movie_by_id(self, movie_id):
        return Movie.query.get(movie_id)

