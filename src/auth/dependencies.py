from fastapi import Request, Depends

from auth.services import AuthJWTService
from auth.exceptions import PermissionDenied, UnauthorizedException


class AuthDependency:
    AUTH_HEADER_KEY = 'Authorization'

    def __init__(
            self,
            request: Request,
            token_type: str = AuthJWTService.ACCESS_TOKEN_TYPE,
            extract_from_headers: bool=True
        ):
        self._auth = AuthJWTService()
        self._token = self._payload = None

        if extract_from_headers:
            self._token_type = token_type
            self._token = self._extract_token_from_header(request)
            self._payload = self._auth.decode_token_type(self._token, token_type)

    def set_token(self, token, token_type=AuthJWTService.ACCESS_TOKEN_TYPE):
        self._token = token
        self._token_type = token_type

    def set_refresh_token(self, token):
        self.set_token(token, token_type=AuthJWTService.REFRESH_TOKEN_TYPE)

    def set_activate_token(self, token):
        self.set_token(token, token_type=AuthJWTService.USER_ACTIVATE_TOKEN_TYPE)

    @property
    def payload(self):
        if not self._payload:
            self._payload = self._auth.decode_token_type(self._token, self._token_type)
        return self._payload

    @classmethod
    def no_validate(cls, request: Request):
        return cls(request, extract_from_headers=False)

    def _extract_token_from_header(self, request):
        auth: str = request.headers.get(self.AUTH_HEADER_KEY)
        if not auth:
            raise UnauthorizedException()

        parts = auth.split()
        return parts[1]

    def refresh_access_token(self):
        return self._auth.create_refresh_token(
            self.get_user_sub(),
            self.get_user_claims()
        )

    def get_user_claims(self):
        return self._auth.extract_user_claims(self.payload)

    def get_user_sub(self):
        return self._auth.decode_token(self._token)['sub']

    def get_user_pk(self):
        return self.get_user_claims()['user_pk']

    def get_user_role(self):
        return self.get_user_claims()['user_role']


def validate_permissions(roles):
    def validate(auth: AuthDependency = Depends()):
        if auth.get_user_role() not in roles:
            raise PermissionDenied()
        return True

    return validate
