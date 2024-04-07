from fastapi import Depends
from fastapi.routing import APIRouter
from sqlmodel.ext.asyncio.session import AsyncSession

from auth.dependencies import auth_dependency_no_validate
from auth.exceptions import AuthLoginException
from auth.schemas import AccessTokenSchema, TokenPairSchema, TokenPayload, UserLogin
from auth.services import authenticate_user, create_token_pair_by_user
from database import get_session

router = APIRouter()


@router.post("/login")
async def login_for_access_token(form_data: UserLogin, session: AsyncSession = Depends(get_session)) -> TokenPairSchema:

    user = await authenticate_user(session, form_data.email, form_data.password)
    if not user:
        raise AuthLoginException()

    token_pair: dict = create_token_pair_by_user(user)
    return TokenPairSchema(**token_pair)


@router.post("/refresh")
async def refresh_access_token(payload: TokenPayload, auth: auth_dependency_no_validate = Depends()):
    auth.set_refresh_token(payload.token)
    access_token = auth.refresh_access_token()
    return AccessTokenSchema(access=access_token)
