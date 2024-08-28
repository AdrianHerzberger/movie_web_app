import pytest
import os
from _storage.db_instance import db
from _storage.user_storage import User
from _storage.movie_storage import Movie
from app import app

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    test_database_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "_data_test", "test_movies_data.sqlite"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{test_database_path}"
    app.config['WTF_CSRF_ENABLED'] = False 

    with app.test_client() as client:
        with app.app_context():
            db.create_all()  
            yield client  
            

def test_add_user(test_client):
    user_data = {
        'firstname': 'John',
        'lastname': 'Doe',
        'birthdate': '1990-01-01'
    }
    
    response = test_client.post('/add_user', data=user_data, follow_redirects=True)
    
    assert response.status_code == 200

    user = User.query.filter_by(first_name='John', last_name='Doe').first()

    assert user is not None
    assert user.first_name == 'John'
    assert user.last_name == 'Doe'
    assert user.birth_date.strftime('%Y-%m-%d') == '1990-01-01'
    assert b'User: John Doe added successfully!' in response.data
    
    
def test_add_movie(test_client):
    user = User.query.filter_by(first_name='John', last_name='Doe').first()
    
    assert user is not None
    movie_data = {
        'movietitle': 'Test Movie',
        'releasedate': '2024-01-01',
        'directory': 'Some Directory',
        'movierating': 8.5,
        'userid': user.id 
    }

    response = test_client.post('/add_movie', data=movie_data, follow_redirects=True)

    assert response.status_code == 200

    movie = Movie.query.filter_by(movie_title='Test Movie').first()
    
    assert movie is not None
    assert movie.movie_title == 'Test Movie'
    assert movie.release_date.strftime('%Y-%m-%d') == '2016-01-16'
    assert movie.directory == 'N/A'
    assert movie.movie_rating == None
    assert movie.user_id == user.id  

    assert b'Movie: Test Movie added successfully!' in response.data
