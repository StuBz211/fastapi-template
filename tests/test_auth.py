import pytest

from tests.factories import create_user
from tests.utils import get_token_pair


@pytest.mark.asyncio
async def test_auth(api_client, async_session):
    my_email = "mysuper@mail.com"
    my_password = "password12345"
    await create_user(async_session, email=my_email, password=my_password, activated=True)
    response = await api_client.post("/auth/login", json={"email": my_email, "password": my_password})

    assert response.status_code == 200, response.content
    data = response.json()
    assert "access" in data
    assert "refresh" in data


@pytest.mark.asyncio
async def test_refresh(api_client, async_session):
    user = await create_user(async_session, activated=True)
    refresh_token = get_token_pair(user)["refresh"]
    response = await api_client.post("auth/refresh", json={"token": refresh_token})
    assert response.status_code == 200
    assert "access" in response.json()
