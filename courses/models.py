from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.contrib.auth.models import BaseUserManager

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('lecturer', 'Lecturer'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")

    def __str__(self):
        return self.username

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

class Course(models.Model):
    status = (('Compulsory', 'Compulsory'), ('Required', 'Required'), ('Prerequisite', 'Prerequisite'))

    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    unit = models.IntegerField()
    status = models.CharField(choices=status, max_length=50)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')

    def save(self, *args, **kwargs):
        # Check if the instructor has an admin role
        if self.instructor.role == 'student':
            raise ValidationError("Only users with 'admin' and 'lecturer' role can be assigned as instructors.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Resource(models.Model):
    RESOURCE_TYPE = (
        ('document', 'Document'),
        ('image', 'Image'),
        ('link', 'Link'),
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='resources')
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPE)  # e.g., document, video, link
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.course.title

class ResourceFile(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='resources/')

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    question = models.TextField()
    due_date = models.DateTimeField()

    def __str__(self):
        return self.title

class AssignmentResponse(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    submission_date = models.DateTimeField(auto_now_add=True)
    response_text = models.TextField()  # You can change this field based on your requirements (e.g., FileField for file uploads)

    class Meta:
        unique_together = ('assignment', 'user')  # Ensure one response per user per assignment

    def __str__(self):
        return f"{self.user.username} - {self.assignment.title}"