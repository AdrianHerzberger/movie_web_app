from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .db_instance import db 

class Director(db.Model):
    __tablename__ = 'directors'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    director_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    movie_id = db.Column(db.Integer, ForeignKey('movies.id'), nullable=False)
    
    directed_movies = relationship('Movie', back_populates='director')

