from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from django.core.mail import send_mail
from .models import Student, Courses, ProfileImage
from .serializers import StudentRegisterSerializer, ChangePasswordSerializer, CourseSerializer, ProfileImageSerializer, LoginSerializer, StudentSerializer
from .utils import generate_unique_password
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import update_session_auth_hash
from django.template.loader import render_to_string
# Import RefreshToken 
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.parsers import MultiPartParser, FormParser
import cloudinary.uploader

class StudentRegisterViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = StudentRegisterSerializer
    queryset = Student.objects.all()

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"status": "success", "message": "Student deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



class LoginViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = Response({
                'status': 'success',
                'student': StudentSerializer(user).data,
            }, status=status.HTTP_200_OK)


            response.set_cookie(
                key = 'access_token',
                value = access_token,
                httponly = True,
                secure = True,  # Use HTTPS in production
                samesite = 'None',
                max_age=300,  # 5 minutes
                domain='student-management-system-1-ur04.onrender.com'
            )

            response.set_cookie(
                key = 'refresh_token',
                value = refresh_token,
                httponly = True,
                secure = True,  # Use HTTPS in production
                samesite = 'None',
                max_age=86400,  # 1 day
                domain='student-management-system-1-ur04.onrender.com'
            )

            return response
        return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
           

class LogoutViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                refresh.blacklist()  # Blacklist the token
            except Exception as e:
                return Response({"error": "Invalid token" + str(e)}, status=status.HTTP_400_BAD_REQUEST)    
        response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response



class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        tokens = response.data

        # Set the access token in a secure, HTTP-only cookie
        response.set_cookie(
            key='access_token',
            value=tokens['access'],
            httponly=True,
            secure=True,  # Use HTTPS in production
            samesite='Lax'
        )
        return response


class ProtectedStudentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        student = request.user
        serializer = StudentSerializer(student)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class ChangePasswordViewSet(viewsets.ViewSet):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

        print(user.email)

        if not user.check_password(old_password):
            return Response({"error": "Incorrect old password"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)  # Hash new password correctly
        user.save()

        # Update session to prevent logout
        update_session_auth_hash(request, user)

        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
    

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Courses.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"status": "success", "message": "Course deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    

class ProfileImageViewSet(viewsets.ModelViewSet):
    queryset = ProfileImage.objects.all()
    serializer_class = ProfileImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
       data = request.data.copy()
       student_id = data.get('student')
       image_file = request.FILES.get('image')

       if not student_id or not image_file:
              return Response({"status": "error", "errors": "Student ID and image file are required."}, status=status.HTTP_400_BAD_REQUEST)
       
       # Upload image to Cloudinary
       try:
            upload_result = cloudinary.uploader.upload(image_file, folder="profile_images/")
            image_url = upload_result.get('secure_url')
            # save in database
            profile = ProfileImage.objects.create(student_id=student_id, image_url=image_url)
            serializer = self.get_serializer(profile)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
       except Exception as e:
            return Response({"status": "error", "errors": f"Image upload failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       
       
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        image_file = request.FILES.get("image")

        if image_file:
            # Optional: delete old image from Cloudinary before uploading new
            if profile.image_url:
                public_id = profile.image_url.split("/")[-1].split(".")[0]  # extract public_id
                cloudinary.uploader.destroy(public_id)

            upload_result = cloudinary.uploader.upload(image_file)
            profile.image = image_file
            profile.image_url = upload_result.get("secure_url")
            profile.save()

        serializer = self.get_serializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        profile = self.get_object()

        # Delete from Cloudinary if exists
        if profile.image_url:
            try:
                public_id = profile.image_url.split("/")[-1].split(".")[0]
                cloudinary.uploader.destroy(public_id)
            except Exception as e:
                return Response({"error": f"Failed to delete Cloudinary image: {str(e)}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        profile.delete()
        return Response({"message": "Profile and image deleted successfully"},
                        status=status.HTTP_204_NO_CONTENT)