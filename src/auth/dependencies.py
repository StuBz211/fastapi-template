from typing import Annotated, Union

from fastapi import Depends, Header, Request

from auth.exceptions import PermissionDenied, UnauthorizedException
from auth.services import TokenProvider


class TokenData:
    def __init__(self, token: str | None, token_type: str = TokenProvider.ACCESS_TOKEN_TYPE):
        self._auth = TokenProvider()
        self._payload = None
        if token:
            self._token = token
            self._token_type = token_type
            self.validate()

    def validate(self):
        self._payload = self._auth.decode_token_type(self._token, self._token_type)

    def get_user_claims(self):
        return self._auth.extract_user_claims(self.payload)

    def get_user_sub(self):
        return self._auth.decode_token(self._token)["sub"]

    def get_user_pk(self):
        return self.get_user_claims()["user_pk"]

    def get_user_role(self):
        return self.get_user_claims()["user_role"]

    @property
    def payload(self):
        if not self._payload:
            self.validate()
        return self._payload

    def set_token(self, token, token_type=TokenProvider.ACCESS_TOKEN_TYPE):
        self._token = token
        self._token_type = token_type
        self.validate()

    def set_refresh_token(self, token):
        self.set_token(token, token_type=TokenProvider.REFRESH_TOKEN_TYPE)

    def set_activate_token(self, token):
        self.set_token(token, token_type=TokenProvider.USER_ACTIVATE_TOKEN_TYPE)

    def refresh_access_token(self):
        return self._auth.create_refresh_token(self.get_user_sub(), self.get_user_claims())


class AuthDependency:
    AUTH_HEADER_KEY = "Authorization"

    def __call__(self, request: Request, authorization: Annotated[Union[str, None], Header()]):
        token = self._extract_token_from_header(request)
        return TokenData(token)

    @classmethod
    def no_validate(cls, request: Request):  # noqa just for apidocs
        return TokenData(token=None)

    def _extract_token_from_header(self, request):
        auth: str = request.headers.get(self.AUTH_HEADER_KEY)
        if not auth:
            raise UnauthorizedException()

        parts = auth.split()
        return parts[1]


auth_dependency = AuthDependency()
auth_dependency_no_validate = AuthDependency().no_validate


def validate_permissions(roles):
    def validate(auth: auth_dependency = Depends()):
        if auth.get_user_role() not in roles:
            raise PermissionDenied()
        return True

    return validate
