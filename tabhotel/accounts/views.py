from django.shortcuts import render
import jwt
from django.conf import settings
# Create your views here.
from rest_framework import generics, permissions, views, status
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .models import User
from django.http import HttpResponsePermanentRedirect
import os
# Register API

class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+user.username + \
            ' Please Use the link below to verify your email. \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Please verify your EMAIL.. Thank You :)'}
        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)
       # return Response({
        #"user": UserSerializer(user, context=self.get_serializer_context()).data,
        #"token": AuthToken.objects.create(user)[1],
        
        #})

#Logi class
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user) #login
        return super(LoginAPI, self).post(request, format=None)

class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token=request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user=User.objects.get(id=payload['user_id'])
            if not user.is_verified:

                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'Error': 'NOT activated'}, status=status.HTTP_400_BAD_REQUEST)
