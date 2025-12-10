from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model

User = get_user_model()

class JWTAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        query_params = parse_qs(scope["query_string"].decode())
        token_list = query_params.get("token")

        if token_list:
            token = token_list[0]
            user = await self.get_user(token)
            scope["user"] = user

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, token):
        try:
            auth = JWTAuthentication()
            validated = auth.get_validated_token(token)
            return auth.get_user(validated)
        except Exception:
            return None
