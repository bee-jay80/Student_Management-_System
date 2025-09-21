from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.utils.timezone import now
from django.conf import settings

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        """
        Custom JWT authentication that tries:
        1. Standard header-based JWT (Authorization: Bearer <token>)
        2. Cookie-based access_token
        3. If access_token expired -> try refresh_token from cookies
        """
        # 1. Check headers first (standard behavior)
        header = self.get_header(request)
        if header is not None:
            return super().authenticate(request)

        # 2. Try access_token cookie
        raw_access_token = request.COOKIES.get("access_token")
        raw_refresh_token = request.COOKIES.get("refresh_token")

        if raw_access_token:
            try:
                validated_token = self.get_validated_token(raw_access_token)
                return self.get_user(validated_token), validated_token
            except TokenError as e:
                # If access expired, fall back to refresh
                if raw_refresh_token:
                    try:
                        refresh = RefreshToken(raw_refresh_token)
                        # Make sure refresh token is still valid
                        if refresh["exp"] < now().timestamp():
                            raise InvalidToken("Refresh token expired")

                        # Generate a new access token
                        new_access = str(refresh.access_token)
                        validated_token = self.get_validated_token(new_access)

                        # Attach new token to request so views can continue
                        request.new_access_token = new_access
                        return self.get_user(validated_token), validated_token

                    except TokenError:
                        raise InvalidToken("Refresh token invalid or expired")
                else:
                    raise InvalidToken("Access token expired and no refresh token")
        
        return None
