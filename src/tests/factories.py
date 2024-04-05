from mimesis import Generic, Locale

from user import crud as user_crud
from user import schemas as user_schemas

g = Generic(locale=Locale.EN)


def create_create_user_payload(email=None, password=None):
    return {"email": email or g.person.email(), "password": password or g.person.password()}


async def create_user(async_session, email=None, password=None, activated=False):
    data = create_create_user_payload(email=email, password=password)
    user = await user_crud.create(async_session, user_schemas.UserCreate(**data))
    if activated:
        user = await user_crud.update_by_id(async_session, user.pk, {"activated": True})

    return user
