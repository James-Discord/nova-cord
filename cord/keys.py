import secrets

async def create(user):
    return 'nv-' + secrets.token_urlsafe(32)
