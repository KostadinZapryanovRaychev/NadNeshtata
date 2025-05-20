from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from backend.api_logic.services.subscribe_service import subscribe_user, unsubscribe_user, get_user_subscription
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
            user = register_user(username, password, email,
                                 first_name, last_name)
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


class UserProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        """
        Get user profile by user_id.
        """
        try:
            user = get_user_data(user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, user_id):
        """
        Update user profile by user_id.
        """
        try:
            user = get_user_data(user_id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, user_id):
        """
        Delete user profile by user_id.
        """
        try:
            user = get_user_data(user_id)
            user.delete()
            return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)


class UserSubscriptionView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        """
        Get user subscription details by user_id.
        """
        try:
            subscription = get_user_subscription(user_id)
            if subscription:
                return Response(subscription, status=status.HTTP_200_OK)
            return Response({"detail": "No subscription found."}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, user_id):
        """
        Subscribe a user to a plan.
        """
        plan_id = request.data.get("plan_id")
        if not plan_id:
            return Response({"detail": "Missing plan_id."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            subscription = subscribe_user(user_id, plan_id)
            return Response(subscription, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        """
        Unsubscribe a user from their current plan.
        """
        try:
            unsubscribe_user(user_id)
            return Response({"detail": "User unsubscribed successfully."}, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
