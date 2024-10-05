import pytest
from fastapi.testclient import TestClient
from app import app 
from database import SessionLocal, Base, engine
from models import Post, User, Comment, Tag

# Setup the Test Client
client = TestClient(app)

# Override the database for testing
@pytest.fixture(scope="module")
def test_db():
    # Create the test database
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Sample test data
def create_test_data(db):
    user = User(username="testuser")
    post = Post(text="Test Post", draft=True, user=user)
    tag = Tag(name="testtag")
    comment = Comment(text="Test Comment", post=post, user=user)
    db.add_all([user, post, tag, comment])
    db.commit()

@pytest.fixture(scope="function")
def setup_test_data(test_db):
    create_test_data(test_db)

# Test the GET /api/posts endpoint
def test_get_posts(setup_test_data):
    response = client.get("/api/posts?status=draft&include=tags,user")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "tags" in data[0]
    assert "user" in data[0]

# Test the GET /api/posts/1 endpoint
def test_get_post_by_id(setup_test_data):
    response = client.get("/api/posts/1?include=tags,user,comments")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "tags" in data
    assert "comments" in data

# Test the GET /api/users/1 endpoint
def test_get_user_by_id(setup_test_data):
    response = client.get("/api/users/1?include=posts,comments")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "posts" in data
    assert "comments" in data
