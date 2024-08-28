import pytest
from app import app

@pytest.fixture(scope='module')
def test_client():
    with app.test_client() as client:
        with app.app_context():
            yield client 

def test_homepage(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Welcome to your movie app!' in response.data