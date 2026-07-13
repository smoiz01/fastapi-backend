from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env.test", override=True)

import pytest
from sqlmodel import Session, SQLModel
from fastapi.testclient import TestClient

from app import models
from app.main import app
from app.database import engine, get_session


@pytest.fixture()
def client():
    SQLModel.metadata.drop_all(bind=engine)
    SQLModel.metadata.create_all(bind=engine)
    def override_get_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture()
def test_user(client):
    res = client.post(
        "/users/",
        json={"email": "user@example.com", "password": "secret123"},
    )

    return {
        "password": "secret123",
        **res.json()
    }

@pytest.fixture()
def test_token(client, test_user):
    res = client.post("/login", data = {
            "username": test_user["email"],
            "password": test_user["password"]
        })

    return res.json()["access_token"]

@pytest.fixture
def authorized_client(test_token):
    return TestClient(app, headers={"Authorization": f"Bearer {test_token}"})

@pytest.fixture
def test_post(authorized_client):
    res = authorized_client.post("/posts/", json = {
    "title": "test post",
    "content": "testing",
    })
    
    return res.json()

@pytest.fixture()
def test_user_2(client):
    res = client.post(
        "/users/",
        json={"email": "user2@example.com", "password": "secret2_123"},
    )

    return {
        "password": "secret2_123",
        **res.json()
    }

@pytest.fixture()
def test_token_2(client, test_user_2):
    res = client.post("/login", data = {
            "username": test_user_2["email"],
            "password": test_user_2["password"]
        })

    return res.json()["access_token"]

@pytest.fixture
def authorized_client_2(test_token_2):
    return TestClient(app, headers={"Authorization": f"Bearer {test_token_2}"})

@pytest.fixture
def test_post_2(authorized_client_2):
    res = authorized_client_2.post("/posts/", json = {
    "title": "test post 2",
    "content": "testing testing 2",
    })
    
    return res.json()

