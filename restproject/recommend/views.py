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
from .scripts import scrapping
from .scripts import tf_idf

# Create your views here.

class MainUrl(APIView):

    permission_classes = (AllowAny,)
    def get(self, request):
        urls = scrapping.display()
        return Response(urls)
    
    def post(self, request):
        scrap = request.data.get('scrap')
        return Response(scrapping.addNews())




class RegisterUser(APIView):

    permission_classes = (AllowAny,)
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.create_user(username = username, email = email, password = password)
        try:
            user.save()
            print(user)
            return Response('user created')
        except:
            return Response('user already exists')

class Login(APIView):

    permission_classes = (AllowAny,)
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({'error':'enter both username and password'},status = HTTP_400_BAD_REQUEST)

        user = authenticate(username = username, password = password)
        print(user)
        if user is not None:
            return Response('welcome',user)
        else:
            return Response('Invalid credentials')


class Temp(APIView):

    def get(self, request):
        tf_idf.letsStart()
        return Response('done')

