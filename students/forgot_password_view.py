import jwt
from django.conf import settings
from datetime import datetime, timedelta
from django.core.mail import send_mail
from .models import Student
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.template.loader import render_to_string
from .serializers import ForgotPasswordSerializer,ResetPasswordSerializer


class ForgotPasswordViewSet(viewsets.ViewSet):
    serializer_class = ForgotPasswordSerializer
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = Student.objects.get(email=email)

            if not user:
                return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
            

            # Generate a unique token and expiration time
            payload = {
                "email":user.email,
                "exp": datetime.utcnow() + timedelta(minutes=5),
                "type": "password_reset"
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

            # Generate reset link
            reset_link = f"http://127.0.0.1:8000/api/reset-password/?token={token}"

             # Render HTML email template
            email_content = render_to_string("password_reset.html", {"reset_link": reset_link, "user": user})


            # Send email
            send_mail(
                subject="Password Reset Request",
                message="Click the link below to reset your password.",
                from_email="Nice Admin",
                recipient_list=[user.email],
                html_message=email_content,  # Send as HTML
            )

            return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ResetPasswordViewSet(viewsets.ViewSet):
    serializer_class = ResetPasswordSerializer
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data["token"]

            if not token:
                return Response({"error": "Missing token."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                email = payload.get("email")

                if not email:
                    return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
                
                user = Student.objects.get(email=email)
                
                # Check if user exists 
                if not user:
                    return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
                
                user.set_password(serializer.validated_data["new_password"])
                user.save()

                # Clear token and timestamp from cookies after successful reset
                response = Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)

            except jwt.ExpiredSignatureError:
                return Response({"error": "Token expired."}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.DecodeError:
                return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        

            return response


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
