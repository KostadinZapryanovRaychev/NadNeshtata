from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from .services.auth_service import register_user, get_user_data, login_user
from .services.subscription_service import (
    get_user_subscription,
    subscribe_user,
    unsubscribe_user
)
from .utils import HandleResponseUtils
from knox.auth import TokenAuthentication

class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            user = register_user(
                username=request.data.get("username"),
                password=request.data.get("password"),
                email=request.data.get("email"),
                first_name=request.data.get("first_name"),
                last_name=request.data.get("last_name"),
                confirm_password=request.data.get("confirm_password"),
                request=request
            )
            return HandleResponseUtils.handle_response(
                status_code=201,
                message={"detail": f"User {user.username} created successfully!"}
            )
        except KeyError as e:
            return HandleResponseUtils.handle_response(400, {"detail": f"Missing field: {str(e)}"})
        except ValidationError as e:
            return HandleResponseUtils.handle_response(400, {"detail": str(e)})


class LoginUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            user = login_user(
                request=request,
                username=request.data.get("username"),
                password=request.data.get("password")
            )
            return HandleResponseUtils.handle_response(
                status_code=200,
                message={
                    "detail": f"User {user['username']} logged in successfully!",
                    "token": user["token"]
                }
            )
        except KeyError as e:
            return HandleResponseUtils.handle_response(400, {"detail": f"Missing field: {str(e)}"})
        except ValidationError as e:
            return HandleResponseUtils.handle_response(400, {"detail": str(e)})


class GetUserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, user_id):
        try:
            user_data = get_user_data(user_id)
            return HandleResponseUtils.handle_response(200, user_data)
        except ValidationError as e:
            return HandleResponseUtils.handle_response(404, {"detail": str(e)})


class UserSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, user_id):
        try:
            subscription = get_user_subscription(user_id)
            if subscription:
                return HandleResponseUtils.handle_response(200, subscription)
            return HandleResponseUtils.handle_response(404, {"detail": "No active subscription found."})
        except ValidationError as e:
            return HandleResponseUtils.handle_response(400, {"detail": str(e)})

    def post(self, request, user_id):
        try:
            plan_id = request.data["plan_id"]
            subscription = subscribe_user(user_id, plan_id)
            return HandleResponseUtils.handle_response(201, subscription)
        except KeyError:
            return HandleResponseUtils.handle_response(400, {"detail": "Missing field: plan_id"})
        except ValidationError as e:
            return HandleResponseUtils.handle_response(400, {"detail": str(e)})

    def delete(self, request, user_id):
        try:
            success = unsubscribe_user(user_id)
            if success:
                return HandleResponseUtils.handle_response(204, {"detail": "User unsubscribed successfully."})
            return HandleResponseUtils.handle_response(404, {"detail": "User has no active subscription."})
        except ValidationError as e:
            return HandleResponseUtils.handle_response(400, {"detail": str(e)})
