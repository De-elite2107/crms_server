from rest_framework import serializers
from .models import *

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        """Check that the email is unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_username(self, value):
        """Check that the username is unique."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already in use.")
        return value

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer()
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'unit', 'status', 'instructor']
    def validate_instructor(self, value):
        if value.role == 'student':
            raise serializers.ValidationError("Only users with 'admin' and 'lecturer role can be assigned as instructors.")
        return value

class ResourceFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceFile
        fields = ['id', 'file']

class ResourceSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    files = ResourceFileSerializer(many=True)  # Include files in the resource serializer
    class Meta:
        model = Resource
        fields = ['id', 'course', 'resource_type', 'url', 'files']

class AssignmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    class Meta:
        model = Assignment
        fields = ['id', 'course', 'title', 'question', 'due_date']

class AssignmentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentResponse
        fields = ['response_text']
        read_only_fields = ['user', 'assignment']  # Make user and assignment read-only since they are set automatically

    def create(self, validated_data):
        # In this case, we don't need to override create since we handle it in perform_create
        return super().create(validated_data)