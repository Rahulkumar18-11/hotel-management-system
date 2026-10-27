import pytest
from app import create_app
from database.db import Database
import mongomock

@pytest.fixture
def app():
    """Create Flask test application fixture using mongomock database client."""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test_secret_key'
    })
    
    # Mock MongoDB connection for testing
    Database.client = mongomock.MongoClient()
    Database.db = Database.client['test_hotel_db']
    Database.setup_indexes()

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_login_page_renders(client):
    """Test that login page loads cleanly with HTTP 200."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b"GRAND HYATT" in response.data

def test_user_creation_and_auth(app):
    """Test Bcrypt password hashing and user model creation."""
    with app.app_context():
        from models.user_model import User
        user = User.create_user('testadmin', 'testadmin@hotel.com', 'AdminPass123', role='admin')
        assert user is not None
        assert user.username == 'testadmin'
        assert user.check_password('AdminPass123') is True
        assert user.check_password('WrongPassword') is False
