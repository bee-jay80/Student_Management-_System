from typing import Optional, Tuple, Dict, Any
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError

User = get_user_model()


class JWTHeaderAndCookieAuthentication(BaseAuthentication):
    """
    Custom authentication that:
    - Reads access token from 'Authorization: Bearer <token>' header.
    - If access token is expired, tries to use refresh token from cookie.
    - Automatically reissues new tokens if refresh is valid.
    - Ensures authenticated requests proceed without authorization errors.
    """

    keyword = "Bearer"
    refresh_cookie_name = getattr(settings, "JWT_REFRESH_COOKIE_NAME", "refresh_token")

    def authenticate(self, request) -> Optional[Tuple[Any, Any]]:
        header = get_authorization_header(request).split()
        access_token = None

        # --- 1️⃣ Get the Access Token from the header ---
        if header and header[0].lower() == self.keyword.lower().encode():
            if len(header) == 1:
                raise exceptions.AuthenticationFailed("Invalid Authorization header. No credentials provided.")
            access_token = header[1].decode()

        # --- 2️⃣ If no access token at all ---
        if not access_token:
            raise exceptions.AuthenticationFailed("No access token found in header.")

        try:
            # --- 3️⃣ Try validating access token ---
            access = AccessToken(access_token)
            user = self.get_user_from_token(access)
            return (user, {"access": str(access)})

        except TokenError as e:
            # Access token is invalid or expired
            refresh_token = request.COOKIES.get(self.refresh_cookie_name)
            if not refresh_token:
                raise exceptions.AuthenticationFailed("Access token expired and no refresh token cookie found.")

            # --- 4️⃣ Try using the refresh token ---
            try:
                refresh = RefreshToken(refresh_token)
            except TokenError:
                raise exceptions.AuthenticationFailed("Refresh token invalid or expired.")

            # --- 5️⃣ Get user from valid refresh token ---
            user = self.get_user_from_token(refresh)

            # --- 6️⃣ Issue new tokens ---
            new_refresh = RefreshToken.for_user(user)
            new_access = new_refresh.access_token

            # Optional: blacklist old refresh
            try:
                refresh.blacklist()
            except Exception:
                pass  # blacklisting not enabled

            # --- 7️⃣ Attach new tokens to the request ---
            tokens = {"access": str(new_access), "refresh": str(new_refresh)}
            request._new_tokens = tokens

            # --- 8️⃣ Proceed as authenticated ---
            return (user, tokens)

    def get_user_from_token(self, token) -> Any:
        """Get user from a validated JWT."""
        user_id = token.payload.get("user_id") or token.payload.get("user")
        if not user_id:
            raise exceptions.AuthenticationFailed("Token missing user_id claim.")

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("User not found.")

        if not user.is_active:
            raise exceptions.AuthenticationFailed("User is inactive.")

        return user
