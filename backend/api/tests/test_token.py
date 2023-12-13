from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
import pytest


@pytest.mark.django_db
def test_token_obtain_pair(test_user: User, api_client: APIClient) -> None:
    response = api_client.post(
        "/api/token/",
        {"username": test_user.username, "password": "StrongP@ssw0rd123"},
    )
    assert response.status_code == status.HTTP_200_OK

    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_refresh_token(test_user: User, api_client: APIClient) -> None:
    response = api_client.post(
        "/api/token/",
        {"username": test_user.username, "password": "StrongP@ssw0rd123"},
    )
    assert response.status_code == status.HTTP_200_OK

    access_token = response.data["access"]
    refresh_token = response.data["refresh"]

    response = api_client.post(
        "/api/token/refresh/", {"refresh": refresh_token}
    )
    assert response.status_code == status.HTTP_200_OK

    new_access_token = response.data["access"]
    assert new_access_token != access_token


@pytest.mark.django_db
def test_verify_token(test_user: User, api_client: APIClient) -> None:
    response = api_client.post(
        "/api/token/",
        {"username": test_user.username, "password": "StrongP@ssw0rd123"},
    )
    assert response.status_code == status.HTTP_200_OK

    access_token = response.data["access"]
    response = api_client.post("/api/token/verify/", {"token": access_token})
    assert response.status_code == status.HTTP_200_OK
