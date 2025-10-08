from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from app.models.user import UserRole


def get_auth_headers(client: TestClient, db: Session, email: str, password: str, role: UserRole) -> dict:
    user_in = UserCreate(email=email, password=password, full_name=f"{role.value.capitalize()} User", role=role)
    crud.user.create_user(db, user=user_in)
    login_data = {"username": email, "password": password}
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    return {"Authorization": f"Bearer {a_token}"}


def test_create_campaign_by_brand(client: TestClient, db: Session) -> None:
    headers = get_auth_headers(client, db, "brand1@example.com", "brandpassword", UserRole.brand)
    data = {"name": "Test Campaign", "description": "A test campaign", "budget": 1000.0}
    r = client.post(
        f"{settings.API_V1_STR}/campaigns/",
        headers=headers,
        json=data,
    )
    assert r.status_code == 200
    created_campaign = r.json()
    assert created_campaign["name"] == data["name"]


def test_create_campaign_by_influencer_fails(client: TestClient, db: Session) -> None:
    headers = get_auth_headers(client, db, "influencer1@example.com", "influencerpassword", UserRole.influencer)
    data = {"name": "Test Campaign Fail", "description": "A test campaign", "budget": 1000.0}
    r = client.post(
        f"{settings.API_V1_STR}/campaigns/",
        headers=headers,
        json=data,
    )
    assert r.status_code == 403


def test_read_campaigns(client: TestClient, db: Session) -> None:
    headers = get_auth_headers(client, db, "brand2@example.com", "brandpassword", UserRole.brand)
    data = {"name": "Another Campaign", "description": "Another test campaign", "budget": 2000.0}
    client.post(f"{settings.API_V1_STR}/campaigns/", headers=headers, json=data)

    # Login as an influencer to read campaigns
    influencer_headers = get_auth_headers(client, db, "influencer2@example.com", "influencerpassword", UserRole.influencer)
    r = client.get(f"{settings.API_V1_STR}/campaigns/", headers=influencer_headers)
    assert r.status_code == 200
    campaigns = r.json()
    assert len(campaigns) > 0