from django.urls import path, include
from .views import *

urlpatterns = [
    path('api/register/', register, name='register'),
    path('api/login/', login_view.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/current-user/', CurrentUserView.as_view(), name='current-user'),
    path('api/courses/', CourseListAPIView.as_view(), name='course-list'),
    path('api/courses/<int:course_id>/resources/', CourseResourceAPIView.as_view(), name='course-resources'),
    path('api/assignments/', AssignmentListAPIView.as_view(), name='assignment-list'),
    path('api/assignments/<int:assignment_id>/responses/', AssignmentResponseCreateView.as_view(), name='assignment-responses'),
]
