from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError

from backend.api_logic.services.subscribe_service import (
    subscribe_user, unsubscribe_user, get_user_subscription
)
from .services.auth_service import register_user, get_user_data


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            user = register_user(
                request.data["username"],
                request.data["password"],
                request.data["email"],
                request.data.get("first_name"),
                request.data.get("last_name"),
            )
            return Response({"detail": f"User {user.username} created successfully!"}, status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response({"detail": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        try:
            user_data = get_user_data(user_id)
            return Response(user_data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)


class UserSubscriptionView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        try:
            subscription = get_user_subscription(
                user_id) 
            return Response(subscription, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, user_id):
        try:
            subscription = subscribe_user(
                user_id, request.data["plan_id"])
            return Response(subscription, status=status.HTTP_201_CREATED)
        except KeyError:
            return Response({"detail": "Missing field: plan_id"}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        try:
            unsubscribe_user(user_id) 
            return Response({"detail": "User unsubscribed successfully."}, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
