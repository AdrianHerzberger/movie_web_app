from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .db_instance import db 

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    review_text = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, ForeignKey('movies.id'), nullable=False)

    author = relationship('User', back_populates='reviews')
    movie = relationship('Movie', back_populates='reviews')

    