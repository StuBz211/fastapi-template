from unittest import mock

import pytest

from tests.factories import create_create_user_payload, create_user, mimesis_g
from tests.utils import auth_client, get_activate_token
from user import crud as user_crud


@pytest.mark.asyncio
async def test_create_user(async_session, api_client):
    data = create_create_user_payload()
    with mock.patch("user.routers.activate_user_message") as mock_func:
        response = await api_client.post("users", json=data)
        assert mock_func.send.called

    assert response.status_code == 204, response.content
    user = await user_crud.read_by_email(async_session, data["email"])
    assert user is not None
    assert user.email == data["email"]


@pytest.mark.asyncio
async def test_update_user(async_session, api_client):
    user = await create_user(async_session, activated=True)
    auth_client(api_client, user)

    new_email = mimesis_g.person.email()
    response = await api_client.patch("users/me", json={"email": new_email})
    assert response.status_code == 200, response.content

    update_user = await user_crud.read_by_id(async_session, user_id=user.pk)
    assert update_user.email == new_email


@pytest.mark.asyncio
async def test_activate_user(async_session, api_client):
    user = await create_user(async_session)
    token = get_activate_token(user)
    response = await api_client.get("users/me/activate", params={"token": token})
    assert response.status_code == 200
    assert response.json()["activated"] is True


@pytest.mark.asyncio
class TestAdminUser:
    async def test_read_user_list(self, async_session, api_client):
        admin = await create_user(async_session, activated=True, is_admin=True)
        auth_client(api_client, admin)
        users = []
        for _ in range(5):
            user = await create_user(async_session)
            users.append(user)

        all_user = [u for u in (admin, *users)]

        response = await api_client.get("users")
        assert response.status_code == 200

        resp_data = response.json()
        assert len(resp_data) == len(all_user)

    async def test_read_user_detail(self, async_session, api_client):
        admin = await create_user(async_session, activated=True, is_admin=True)
        auth_client(api_client, admin)
        user = await create_user(async_session)

        response = await api_client.get(f"users/{user.pk}")
        assert response.status_code == 200
        assert response.json() == {"pk": user.pk, "email": user.email, "activated": False}

    async def test_update_user(self, async_session, api_client):
        admin = await create_user(async_session, activated=True, is_admin=True)
        auth_client(api_client, admin)
        user = await create_user(async_session)

        new_email = mimesis_g.person.email()
        response = await api_client.patch(f"users/{user.pk}", json={"email": new_email})
        assert response.status_code == 200
        assert response.json() == {"pk": user.pk, "email": new_email, "activated": False}

    async def test_delete_user(self, async_session, api_client):
        admin = await create_user(async_session, activated=True, is_admin=True)
        auth_client(api_client, admin)
        user = await create_user(async_session)

        response = await api_client.delete(f"users/{user.pk}")
        assert response.status_code == 204

        response = await api_client.delete(f"users/{user.pk}")
        assert response.status_code == 404

        with pytest.raises(user_crud.UserNotFound):
            await user_crud.read_by_id(async_session, user_id=user.pk)
