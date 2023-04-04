from bal.models import CompayUser
from authr.emailtoken import send_token
from authr.serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from bal.models import CompayUser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from authr.serializers import UserSearch
from django.contrib.auth.models import User
from authr.models import ResetToken

UserModel = get_user_model()


# This function is for creating a new account
@api_view(["post"])
@permission_classes([AllowAny])
def usercreateview(request):
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")
        last_name = request.data.get("last_name")
        first_name = request.data.get("first_name")
        email = request.data.get("email")
        if (
            UserModel.objects.filter(username__icontains=username).first()
            or UserModel.objects.filter(email=email).first()
        ):
            return Response(
                {
                    "status": False,
                    "message": "username or email address already taken by another user ",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        else:
            data = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "username": username,
                "password": password,
            }
            serializer_class = UserSerializer(data=data)
            serializer_class.is_valid(raise_exception=True)
            data = serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)


# This request function is for authenicating of users
@api_view(["post"])
def authrtoken(request):
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")
        try:
            log = authenticate(username=username, password=password)
            login = str(Token.objects.get(user_id=log.id))
            try:
                check = CompayUser.objects.get(user=log)
                profile = check.blank
                p_status = status.HTTP_202_ACCEPTED

            except CompayUser.DoesNotExist:
                profile = True
                p_status = status.HTTP_200_OK

            return Response(
                {"status": True, "token": login, "profile_empty": profile},
                status=p_status,
            )

        except AttributeError:
            return Response(
                {
                    "status": False,
                    "message": "Please enter the correct username and password",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )


# This request function is to check if the user have completed he/she profile register
@api_view(["get"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def p_status(request):
    try:
        user = request.user
        check = CompayUser.objects.get(user=user)
        p_value = check.blank
    except CompayUser.DoesNotExist:
        p_value = True
    return Response(
        {"status": True, "user": user.username, "profile_empty": p_value},
        status=status.HTTP_200_OK,
    )


# This function is for searching for certain user
@api_view(["post"])
@permission_classes([AllowAny])
def user_searching(request):
    if request.method == "POST":
        username_search = request.data.get("search")  # get username
        data = User.objects.filter(username__icontains=username_search)
        serializer_class = UserSearch(data, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)


# This function is for password reset
@api_view(["post"])
@permission_classes([AllowAny])
def reset_passwords(request):
    if request.method == "POST":
        username = request.data.get("username")
        try:
            user = User.objects.get(username=username)
            if user:
                print(True)
                send_token(user.email, user.username)
                return Response(
                    {
                        "status": True,
                        "message": "otp sent to your email address",
                    },
                    status=status.HTTP_200_OK,
                )
        except user.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "username does not exist",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


# This function ask for token and new password,
# verify if token sent to your email is valid and change your password
@api_view(["post"])
@permission_classes([AllowAny])
def verify_token(request):
    if request.method == "POST":
        token = int(request.data.get("token"))
        password = request.data.get("password")
        try:
            verify = ResetToken.objects.get(token=token)
            if verify:
                print(True)
                auth_del = Token.objects.get(user_id=verify.user.id)
                auth_del.delete()
                user = User.objects.get(username=verify.user.username)
                user.set_password(password)
                user.save()
                new_token = Token.objects.create(user=user)
                verify.delete()
                return Response(
                    {
                        "status": True,
                        "message": "your account password have been changed",
                    },
                    status=status.HTTP_201_CREATED,
                )
        except ResetToken.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "invalid token",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
