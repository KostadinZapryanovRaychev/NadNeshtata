from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError

from .services.auth_service import register_user, get_user_data
from .serializers import UserSerializer


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Register a new user.
        """
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")

        if not username or not password or not email:
            return Response({"detail": "Missing fields."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = register_user(username, password, email , first_name, last_name)
            return Response({"detail": f"User {user.username} created successfully!"}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, user_id):
        """
        Get user details by user_id.
        """
        try:
            user = get_user_data(user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
