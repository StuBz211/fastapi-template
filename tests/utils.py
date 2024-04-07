from auth.services import create_activate_token_by_user, create_token_pair_by_user


def get_activate_token(user):
    return create_activate_token_by_user(user)


def get_token_pair(user):
    return create_token_pair_by_user(user)


def auth_client(api_client, user):
    token = get_token_pair(user)["access"]
    api_client.headers["Authorization"] = f"Bearer {token}"
