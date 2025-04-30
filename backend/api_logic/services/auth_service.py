# api_logic/services/auth_service.py

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class AuthService:
    @staticmethod
    def register_user(username, password):
        if not username or not password:
            return {'error': 'Username and password are required'}, 400
        if User.objects.filter(username=username).exists():
            return {'error': 'Username already exists'}, 400
        User.objects.create_user(username=username, password=password)
        return {'message': 'User registered successfully'}, 201

    @staticmethod
    def login_user(request, username, password):
        if not username or not password:
            return {'error': 'Username and password are required'}, 400
        user = authenticate(request, username=username, password=password)
        if user is not None:
            from django.contrib.auth import login
            login(request, user)
            return {'message': 'Login successful'}, 200
        else:
            return {'error': 'Invalid credentials'}, 401
