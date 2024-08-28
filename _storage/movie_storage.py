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
    
    users = relationship('User', back_populates='movies')
    reviews = relationship('Review', back_populates='movies')
    
    
    