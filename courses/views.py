from rest_framework import viewsets
from .models import User
from .models import *
from .serializers import *
from django.contrib.auth import authenticate, login
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext as _
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'User registered successfully',
            'data': {
                'id': user.id,
                'username': user.username,
                'email': user.email,  # Include email if needed
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class login_view(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # Extract username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Get or create token for the authenticated user
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'role': getattr(user, 'role', None),  # Use getattr for safety in case role doesn't exist
            }
            # Return token and user information on successful login
            return Response({
                'token': token.key,
                'message': 'Login Successful',
                'data': data,
            })
        else:
            # Return an error response if authentication fails
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get the Authorization header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return None  # No auth header provided

        try:
            # Split the header into type and token
            auth_type, token = auth_header.split()
            if auth_type.lower() != 'token':
                return None  # Not a Token type
            
            # Validate the token and retrieve the user
            user = self.get_user_from_token(token)
            return (user, token)  # Return user and token

        except ValueError:
            raise AuthenticationFailed('Invalid authorization header.')

    def get_user_from_token(self, token):
        try:
            # Retrieve the user associated with the token
            token_obj = Token.objects.get(key=token)
            return token_obj.user
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    authentication_classes = [CustomTokenAuthentication]  # Use your custom authentication

    def post(self, request):
        try:
            # Get the token from the request header
            token = request.auth
            
            if not token:
                return Response({'error': 'No token provided.'}, status=status.HTTP_400_BAD_REQUEST)

            # Delete the token to log out the user
            Token.objects.filter(key=token).delete()
            
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        user = request.user  # Get the current logged-in user
        serializer = UserSerializer(user)  # Serialize the user data
        return Response(serializer.data)  # Return the serialized data

class UserViewSet(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CourseResourceAPIView(generics.ListAPIView):
    serializer_class = ResourceSerializer
    
    def get_queryset(self):
        course_id = self.kwargs['course_id']  # Get the course ID from the URL parameters
        return Resource.objects.filter(course_id=course_id)  # Filter resources by course ID

class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class AssignmentListAPIView(generics.ListAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

class AssignmentResponseCreateView(generics.CreateAPIView):
    queryset = AssignmentResponse.objects.all()
    serializer_class = AssignmentResponseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication]  # Use your custom authentication

    def perform_create(self, serializer):
        # Get the assignment_id from the URL parameters
        assignment_id = self.kwargs['assignment_id']
        
        # Get the current user from the request
        user = self.request.user
        
        # Create the response with the current user and specified assignment
        serializer.save(user=user, assignment_id=assignment_id)