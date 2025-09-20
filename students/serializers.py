from rest_framework import serializers
from .models import Student, Courses, ProfileImage
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate



class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        


class StudentRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, read_only=True, required=False)

    class Meta:
        model = Student
        fields = ['id', 'email', 'first_name', 'last_name', 'middle_name', 'city', 'state', 'country_name', 'primary_phone','password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)

        Student.set_password(self, password)
        student = Student.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            middle_name=validated_data.get('middle_name', ''),
            city=validated_data.get('city', ''),
            state=validated_data.get('state', ''),
            country_name=validated_data.get('country_name', ''),
            primary_phone=validated_data.get('primary_phone', ''),
        )
        student.set_password(password)
        student.save()
        return student

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user and user.is_active:
                data['user'] = user
                return data
            else:
                raise serializers.ValidationError("Invalid email or password.")


class CourseSerializer(serializers.ModelSerializer):
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