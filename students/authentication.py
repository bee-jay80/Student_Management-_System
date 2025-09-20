from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        # Try access token first
        if token:
            try:
                validated_token = self.get_validated_token(token)
                user = self.get_user(validated_token)
                return user, validated_token
            except AuthenticationFailed:
                pass  # Try refresh below

        # If access token fails, try refresh token
        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                new_access_token = str(refresh.access_token)
                validated_token = self.get_validated_token(new_access_token)
                user = self.get_user(validated_token)
                # attach the new token to the request for middleware/view to set cookie
                request._new_access_token = new_access_token
                return user, validated_token
            except TokenError:
                raise AuthenticationFailed("Session expired. Please log in again.")
            except AuthenticationFailed as e:
                raise AuthenticationFailed(f"Token validation failed after refresh: {str(e)}")

        return None