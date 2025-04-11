from rest_framework import serializers
from .models import Student, Courses, ProfileImage
from .utils import generate_unique_password
from django.contrib.auth import get_user_model



class StudentRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, read_only=True, required=False)

    class Meta:
        model = Student
        fields = ['id', 'email', 'first_name', 'last_name', 'middle_name', 'city', 'state', 'country_name', 'primary_phone','password']

class courseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)

# Forgot password serializers
Student = get_user_model()

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not Student.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value
    
class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=6)
    token = serializers.CharField(write_only=True)

    def validate(self, data):
        if not data['new_password']:
            raise serializers.ValidationError({"new_password": "This field is required."})
        if len(data) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return data
    
class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = ['id','student','image','image_url']