from dataclasses import dataclass, asdict
import uuid

import core_exceptions
from user.models import User
from config import settings

from datetime import timedelta, datetime
from jose import jwt, JOSEError

from user.password import verify_password

from user import crud as user_crud

from auth.exceptions import InvalidTokenType, InvalidToken


@dataclass
class AuthUserClaims:
    user_role: str
    user_pk: int

    @staticmethod
    def from_user(user: User):
        return AuthUserClaims(user_pk=user.pk, user_role=user.role)

    def as_dict(self):
        return asdict(self)


class AuthJWTService:  # TODO find async library?
    ACCESS_TOKEN_TYPE = 'access'
    REFRESH_TOKEN_TYPE = 'refresh'
    RESET_PASSWORD_TOKEN_TYPE = 'reset'
    USER_ACTIVATE_TOKEN_TYPE = 'activate'
    CUSTOM_TOKEN_TYPES = (RESET_PASSWORD_TOKEN_TYPE, USER_ACTIVATE_TOKEN_TYPE)
    TOKEN_CLAIMS = ("jti", 'iat', 'exp', 'sub', 'type')

    def decode_token_type(self, token: str, token_type: str):
        payload = self.decode_token(token)
        if payload['type'] != token_type:
            raise InvalidTokenType("Invalid token type")
        return payload

    def create_token(self, sub: str, user_claims: dict, token_type):
        if token_type not in self.CUSTOM_TOKEN_TYPES:
            raise InvalidTokenType

        return self._create_token(sub, user_claims, token_type)

    def create_access_token(self, sub: str, user_claims: dict):
        return self._create_token(sub, user_claims, self.ACCESS_TOKEN_TYPE)

    def create_refresh_token(self, sub: str, user_claims: dict):
        return self._create_token(sub, user_claims, self.REFRESH_TOKEN_TYPE)

    def extract_user_claims(self, payload):
        return {
            claim_key: claim_value
            for claim_key,claim_value in payload.items()
            if claim_key not in self.TOKEN_CLAIMS
        }

    @staticmethod
    def _get_jti():
        return str(uuid.uuid4())

    def _get_expire(self, iat: datetime, token_type: str):
        if token_type == self.ACCESS_TOKEN_TYPE:
            expire = iat + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        else:
            expire = iat + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        return expire

    def _get_token_claims(self, token_type: str):
        iat = datetime.utcnow()

        return {
            'jti': self._get_jti(),
            'iat': iat,
            'exp': self._get_expire(iat, token_type),
            'type': token_type
        }

    def _create_token(self, sub: str, user_claims: dict, token_type: str ):
        to_encode = {**user_claims, 'sub': sub}
        to_encode.update(self._get_token_claims(token_type))
        return jwt.encode(to_encode, settings.JWT_PRIVATE_KEY, algorithm=settings.ALGORITHM)

    @staticmethod
    def decode_token(token):
        try:
            return jwt.decode(token, settings.JWT_PUBLIC_KEY, algorithms=[settings.ALGORITHM])
        except JOSEError as exc:
            raise InvalidToken(detail=str(exc))


async def authenticate_user(session, email: str, password: str) -> User | bool:
    try:
        user = await user_crud.read_by_email(session, email)
    except core_exceptions.NotFoundException:
        return False

    if not user.activated:
        return False
    if verify_password(password, user.hashed_password):
        return user
    return False


def create_activate_token_by_user(user: User) -> str:
    sub = user.email
    user_claims = AuthUserClaims.from_user(user).as_dict()
    auth_service = AuthJWTService()
    return auth_service.create_token(sub, user_claims, auth_service.USER_ACTIVATE_TOKEN_TYPE)


def create_token_pair_by_user(user: User) -> dict[str, str]:
    sub = user.email
    user_claims = AuthUserClaims.from_user(user).as_dict()

    auth_service = AuthJWTService()
    refresh_token = auth_service.create_refresh_token(sub, user_claims)
    access_token = auth_service.create_access_token(sub, user_claims)
    return {'access': access_token, 'refresh': refresh_token}
