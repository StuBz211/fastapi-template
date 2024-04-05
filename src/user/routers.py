from fastapi import APIRouter
from fastapi import  Depends, Request
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from user import crud
from user import schemas
from database import get_session
from auth.dependencies import validate_permissions, AuthDependency
from auth.services import create_activate_token_by_user
from user.models import RolesEnum

from worker.tasks import activate_user_message

admin_roles = [RolesEnum.ADMIN.value]
router = APIRouter()


@router.get('', dependencies=[Depends(validate_permissions(admin_roles))])
async def user_list(session: AsyncSession = Depends(get_session)) -> list[schemas.User]:
    # TODO implement paginator
    users = await crud.reads(session, skip=0, limit=100)
    return users


@router.post('', status_code=204)
async def user_create(user_data: schemas.UserCreate, session: AsyncSession = Depends(get_session)):
    user = await crud.create(session, user_data)
    token = create_activate_token_by_user(user)
    activate_user_message.send(user.email, token)


@router.get('/me')
async def user_detail_me(
        auth: AuthDependency = Depends(),
        session: AsyncSession = Depends(get_session)
) -> schemas.User:

    user_id = auth.get_user_pk()
    user = await crud.read_by_id(session, user_id=user_id)
    return user


@router.patch('/me')
async def user_update(
        user_data: schemas.UserUpdate,
        auth: AuthDependency = Depends(),
        session: AsyncSession = Depends(get_session)
) -> schemas.User:
    user_id = auth.get_user_pk()
    user = await crud.update_by_id(session, user_id, user_data.dict())
    return user


@router.get('/me/activate')
async def user_activate(
        token: str,
        auth: AuthDependency.no_validate = Depends(),
        session: AsyncSession = Depends(get_session)
) -> schemas.User:
    auth.set_activate_token(token)
    user_id = auth.get_user_pk()
    user = await crud.update_by_id(session, user_id, user_data={'activated': True})
    return user


@router.get('/{user_id}', dependencies=[Depends(validate_permissions(admin_roles))])
async def user_detail(user_id: int, session: AsyncSession = Depends(get_session)) -> schemas.User:
    user = await crud.read_by_id(session, user_id)
    return user


@router.patch('/{user_id}', dependencies=[Depends(validate_permissions(admin_roles))])
async def user_update(user_id: int, user_data: schemas.UserUpdate, session: AsyncSession = Depends(get_session)) -> schemas.User:
    user = await crud.update_by_id(session, user_id, user_data.dict())
    return user


@router.delete('/{user_id}', dependencies=[Depends(validate_permissions(admin_roles))])
async def user_delete(user_id: int, session: AsyncSession = Depends(get_session)):
    await crud.delete_by_id(session, user_id)
    return JSONResponse({}, status_code=204)

