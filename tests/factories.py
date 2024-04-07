from mimesis import Generic, Locale

from user import crud as user_crud
from user import schemas as user_schemas

mimesis_g = Generic(locale=Locale.EN)


def create_create_user_payload(email=None, password=None):
    return {"email": email or mimesis_g.person.email(), "password": password or mimesis_g.person.password()}


async def create_user(async_session, email=None, password=None, activated=False, is_admin=False):
    data = create_create_user_payload(email=email, password=password)
    user = await user_crud.create(async_session, user_schemas.UserCreate(**data))

    to_update = {}
    if activated:
        to_update["activated"] = True
    if is_admin:
        to_update["role"] = "admin"

    if to_update:
        user = await user_crud.update_by_id(async_session, user.pk, to_update)

    return user
