from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken
from django.http import JsonResponse
from .models import Student


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        protected_paths = ['/api/protected/','/api/change-password/','api/course/','/api/grades/']  # Add other protected paths if needed

        if request.path in protected_paths:
            access_token = request.COOKIES.get('access_token')

            if not access_token:
                return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=401)

            try:
                token = AccessToken(access_token)
                user_id = token['user_id']
                user = Student.objects.get(id=user_id)

                if user.is_active:
                    request.user = user  # Attach user to request for view use
                else:
                    return JsonResponse({'detail': 'Inactive user.'}, status=401)
            except Student.DoesNotExist:
                return JsonResponse({'detail': 'User not found.'}, status=401)
            except Exception as e:
                return JsonResponse({'detail': str(e)}, status=401)

        return None