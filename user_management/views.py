import random
import requests
from django.contrib.auth import authenticate
from django.db import IntegrityError, transaction
from oauth2_provider.models import Application
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from todo_list.models import User, Otp
from user_management.serializer import SignUpAndLoginSerializer, EmailVerifySerializer
from user_management.utils import send_otp


class SignUpView(APIView):
    @staticmethod
    def post(request):
        try:
            with transaction.atomic():
                serial_data = SignUpAndLoginSerializer(data=request.data)
                if serial_data.is_valid(raise_exception=True):
                    user_data = dict(serial_data.validated_data)
                    user = User.objects.create(
                        username=user_data["email"],
                        email=user_data["email"],
                    )
                    otp = random.randint(1111, 9999)
                    Otp.objects.create(user=user, otp=otp)
                    send_otp(user_data["email"], otp)
                    user.set_password(user_data.get("password"))
                    user.save()
                    Application.objects.create(
                        user=user,
                        authorization_grant_type="password",
                        client_type="confidential",
                        name=user.email,
                    )
                    return Response({"message": "User registered, Please check your email for verification."},
                                    status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"Error": "User already exist!"}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @staticmethod
    def post(request):
        try:
            serial_data = SignUpAndLoginSerializer(data=request.data)
            if serial_data.is_valid(raise_exception=True):
                user_data = dict(serial_data.validated_data)
                user = User.objects.get(username=user_data["email"])
                if not user.is_verified:
                    return Response(
                        {"message": "Please verify your email."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                validate_user = authenticate(
                    username=user_data["email"], password=user_data["password"]
                )
                if validate_user is None:
                    return Response(
                        {"message": "invalid credential"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                app = Application.objects.filter(user=user)
                data = {
                    "username": user_data["email"],
                    "password": user_data["password"],
                    "grant_type": "password",
                    "client_id": app.first().client_id,
                    "client_secret": app.first().client_secret,
                }
                token = requests.post("http://127.0.0.1:8000/" + "o/token/", data=data)
                token_data = {
                    "access_token": token.json().get("access_token"),
                    "expires_in": token.json().get("expires_in"),
                    "token_type": token.json().get("token_type"),
                }
                return Response(token_data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"message": "User login failed."}, status=status.HTTP_404_NOT_FOUND)


class EmailVerifyView(APIView):
    @staticmethod
    def post(request):
        try:
            serial_data = EmailVerifySerializer(data=request.data)
            if serial_data.is_valid(raise_exception=True):
                otp_object = Otp.objects.get(otp=serial_data.validated_data.get("otp"),
                                             user__email=serial_data.validated_data.get("email"))
                if otp_object:
                    otp_object.user.is_verified = True
                    otp_object.user.save()
                    otp_object.delete()
                    return Response({"Message": "verified."})
        except Otp.DoesNotExist:
            return Response({"Error": "Email or Otp did not match, please try again."},
                            status=status.HTTP_400_BAD_REQUEST)
