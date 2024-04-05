import pytest
from unittest import mock

from tests.factories import create_create_user_payload
from user import crud as user_crud


@pytest.mark.asyncio
async def test_create_user(async_session, api_client):
    data = create_create_user_payload()
    with mock.patch('user.routers.activate_user_message') as mock_func:
        response = await api_client.post('users', json=data)
        assert mock_func.send.called

    assert response.status_code == 204, response.content
    user = await user_crud.read_by_email(async_session, data['email'])
    assert user is not None
    assert user.email == data['email']

