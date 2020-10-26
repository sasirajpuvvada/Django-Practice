import json
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated 
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.status import (HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK)
from django.contrib.auth.models import User

# Create your views here.

class RegisterUser(APIView):

    # permission_classes = (AllowAny,)
    def post(self, request):
        username = request.dara.get('username')
        email = request.dara.get('email')
        password = request.dara.get('password')
        user = User.objects.create_user(username = username, email = email, password = password)
    
        try:
            user.save()
            print(user)
            return Response('user created')
        except:
            return Response('user already exists')
            
