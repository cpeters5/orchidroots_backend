from django.shortcuts import render
from rest_framework import status, generics, request
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from django.contrib import auth
from django.contrib.auth.models import update_last_login
from helpers._mails import Mail
from helpers._numbers import Numbers
import re
from .auth import Auth
from random import randint
from django.urls import reverse

# Create your views here.


class Logout(APIView):

    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class Signup(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        context = dict()
        serializer = SignupSerializer(data=request.data)
        serializer.initial_data['email'] = serializer.initial_data['email'].lower(
        ).strip()
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(
                serializer.initial_data['password'])
            serializer.validated_data['verify_mail_code'] = Numbers.generate_random_number(
                5)
            serializer.validated_data.pop('confirm_password', None)
            user = serializer.save()
            # Uncomment this line if you want to recive emails
            Mail.verify_email(user, user.verify_mail_code)
            context['detail'] = "Signup Succsesfuly"
            return Response(context, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# we can install Sentry


class VerifyEmailCode(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        context = dict()
        serializer = VerifyEmailCodeApiSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(
                    email=serializer.data['email'].lower().strip())
                code = serializer.data['code']
                if user.verify_mail_code == code:
                    context['detail'] = "Email Verified"
                    if not user.email_verified:
                        user.email_verified = True
                        user.save()
                else:
                    context['error'] = "Wrong code"
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                context['error'] = "Something went wrong"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(context, status=status.HTTP_200_OK)


class ResendVerificationEmail(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        context = dict()
        serializer = ResendVerifyEmailCodeApiSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(
                    email=serializer.data['email'])
                if user.email_verified:
                    context['detail'] = "Email is already verified"
                else:
                    user.verify_mail_code = Numbers.generate_random_number(5)
                    user.save()
                    # Uncomment this line if you want to recive emails
                    Mail.verify_email(user, user.verify_mail_code)
                    context['detail'] = "Verification E-mail sent"
            except User.DoesNotExist:
                context['error'] = "Email doesn't exist."
                Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(context, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgetPasswordSendEmailCodeView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        context = dict()
        serializer = ForgetPasswordSendEmailCodeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
                username = serializer.data['username']
                if(re.search(regex, username)):
                    user = User.objects.get(email=username)
                else:
                    user = User.objects.get(username=username)
                user.reset_pass_code = Numbers.generate_random_number(5)
                user.reset_pass_code_attemps = 0
                user.save()
                # Uncomment this line if you want to recive emails
                Mail.forget_password_email(user, user.reset_pass_code)
                context['detail'] = "Reset password code E-mail sent"
            except User.DoesNotExist:
                context['detail'] = "Reset password code E-mail sent"
            return Response(context, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordVerifyCodeApi(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        context = dict()
        serializer = ResetPasswordVerifyCodeApiSerializer(data=request.data)
        if serializer.is_valid():
            try:
                regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
                username = serializer.data['username']
                if(re.search(regex, username)):
                    user = User.objects.get(email=username)
                else:
                    user = User.objects.get(username=username)
                if user.reset_pass_code_attemps == -1 or user.reset_pass_code == None:
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
                elif user.reset_pass_code_attemps >= 10:
                    context['detail'] = "Too much trials, please generate new code."
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user.reset_pass_code_attemps += 1
                    user.save()
                    if user.reset_pass_code == serializer.data['code']:
                        context['detail'] = "Correct code"
                        context['attemps'] = user.reset_pass_code_attemps
                    else:
                        context['detail'] = "Wrong code"
                        context['attemps'] = user.reset_pass_code_attemps
                        return Response(context, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                context['error'] = "Something went wrong"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(context, status=status.HTTP_200_OK)


class RestPasswordApi(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        context = dict()
        serializer = RestPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
                username = serializer.data['username']
                if(re.search(regex, username)):
                    user = User.objects.get(email=username)
                else:
                    user = User.objects.get(username=username)
                if user.reset_pass_code_attemps >= 10:
                    context['detail'] = "Too much trials, please generate new code."
                else:
                    user.reset_pass_code_attemps += 1
                    if user.reset_pass_code == serializer.data['code']:
                        user.set_password(serializer.data['new_password'])
                        user.reset_pass_code = None
                        user.email_verified = True
                        user.reset_pass_code_attemps = -1
                        context['detail'] = "password reseted successfuly"
                    else:
                        context['detail'] = "Wrong code"
                        context['attemps'] = user.reset_pass_code_attemps
                    user.save()
            except User.DoesNotExist:
                context['error'] = "Something went wrong"
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(context, status=status.HTTP_200_OK)


class Login(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        context = dict()
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        username = serializer.data['username']
        password = serializer.data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            context['error'] = "Please enter the correct email and password."
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        if user.email_verified:
            context['token'] = token.key
            context['email_verified'] = user.email_verified
            update_last_login(None, user)
            return Response(context, status=status.HTTP_200_OK)
        context['error'] = "Please verify your email."
        return Response(context, status=status.HTTP_400_BAD_REQUEST)


class CountryView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        serializer = CountrySerializer(
            Country.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PhotographerView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        serializer = PhotographerSerializer(
            Photographer.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SocialLogin(APIView):
    '''
    social_id will be saved in the email by this format social_id@social_type.com
    social_token will be saved in the password
    '''
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        social_token = request.data.get('social_token')
        social_type = request.data.get('social_type')
        social_id = request.data.get('social_id')
        context = dict()
        serializer = SocialLoginSerializer(data=request.data)
        if serializer.is_valid():
            if social_type == 'facebook':
                auth = Auth.facebook_auth(social_token, social_id)
            else:
                return Response({"detail": 'Social type not supported'}, status=status.HTTP_400_BAD_REQUEST)
            if auth['Valid'] == True:
                email = auth['userdata']['email']
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    if social_type == 'facebook':
                        user = User.objects.create_user(social_type=User.FACEBOOK,
                                                        username=email, email=email, password=social_token, email_verified=True, fullname=auth['userdata']['name'])
                        if auth['userdata']['image']:
                            user.photo.save(
                                user.name+'.jpg', auth['userdata']['image'], save=True)
                    user.save()
                token, created = Token.objects.get_or_create(user=user)
                context = dict()
                context['token'] = token.key
                return Response(context)
            else:
                return Response({"detail": 'Social Auth Failed'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
