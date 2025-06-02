# from urllib.parse import parse_qs
# from channels.auth import AuthMiddlewareStack
# from channels.middleware import BaseMiddleware
# from django.contrib.auth.models import AnonymousUser
# from rest_framework_simplejwt.tokens import UntypedToken
# from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# from django.db import close_old_connections
# from django.contrib.auth import get_user_model
# from channels.db import database_sync_to_async  # Import this

# User = get_user_model()

# @database_sync_to_async
# def get_user(validated_token):
#     try:
#         user = User.objects.get(id=validated_token['user_id'])
#         return user
#     except User.DoesNotExist:
#         return AnonymousUser()

# class JWTAuthMiddleware:
#     def __init__(self, inner):
#         self.inner = inner

#     def __call__(self, scope):
#         return JWTAuthMiddlewareInstance(scope, self)

# class JWTAuthMiddlewareInstance:
#     def __init__(self, scope, middleware):
#         self.scope = scope
#         self.middleware = middleware
#         self.inner = middleware.inner

#     async def __call__(self, receive, send):
#         close_old_connections()
#         query_string = parse_qs(self.scope['query_string'].decode())
#         token = query_string.get('token', None)

#         if token:
#             try:
#                 untokenized_token = UntypedToken(token[0])
#                 self.scope['user'] = await get_user(untokenized_token)
#             except (InvalidToken, TokenError):
#                 self.scope['user'] = AnonymousUser()

#         inner = self.inner(self.scope)
#         return await inner(receive, send)

# def JWTAuthMiddlewareStack(inner):
#     return JWTAuthMiddleware(AuthMiddlewareStack(inner))
