import pytest

from tests.factories import create_user


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
