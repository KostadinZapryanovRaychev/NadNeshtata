from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .services.auth_service import register_user, get_user_data
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny


class RegisterUserView(APIView):
    
    permission_classes = [AllowAny]
    def post(self, request):
        """
        Register a new user.
        """
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        if not username or not password or not email:
            return Response({"detail": "Missing fields."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = register_user(username, password, email)
            return Response({"detail": f"User {user.username} created successfully!"}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user_view(request, user_id):
    """
    Get user details.
    """
    try:
        user = get_user_data(user_id)
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
