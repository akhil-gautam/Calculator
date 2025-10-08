from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from app.models.user import UserRole


def test_create_user(client: TestClient, db: Session) -> None:
    username = "test@example.com"
    password = "testpassword"
    data = {"email": username, "password": password, "full_name": "Test User", "role": "brand"}
    r = client.post(
        f"{settings.API_V1_STR}/users/",
        json=data,
    )
    assert r.status_code == 200
    created_user = r.json()
    user = crud.user.get_user_by_email(db, email=username)
    assert user
    assert user.email == created_user["email"]


def test_login(client: TestClient, db: Session) -> None:
    username = "brand@example.com"
    password = "brandpassword"
    user_in = UserCreate(email=username, password=password, full_name="Brand User", role=UserRole.brand)
    crud.user.create_user(db, user=user_in)
    login_data = {"username": username, "password": password}
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert r.status_code == 200
    tokens = r.json()
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_get_current_user(client: TestClient, db: Session) -> None:
    username = "influencer@example.com"
    password = "influencerpassword"
    user_in = UserCreate(email=username, password=password, full_name="Influencer User", role=UserRole.influencer)
    user = crud.user.create_user(db, user=user_in)
    login_data = {"username": username, "password": password}
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=headers)
    assert r.status_code == 200
    current_user = r.json()
    assert current_user
    assert current_user["email"] == username