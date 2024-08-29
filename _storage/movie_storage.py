from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .db_instance import db 

class Movie(db.Model):
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_title = db.Column(db.String(100), nullable=False)
    movie_rating = db.Column(db.Float, nullable=True)
    directory = db.Column(db.String, nullable=True)
    release_date = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)

    owner = relationship('User', back_populates='movies')
    director = relationship('Director', back_populates='directed_movies')
    reviews = relationship('Review', back_populates='movie')

    def to_dict(self):
        return {
            'id': self.id,
            'movie_title': self.movie_title,
            'release_date': self.release_date.isoformat() if self.release_date else None,
            'directory': self.directory,
            'movie_rating': self.movie_rating,
            'user_id': self.user_id
        }