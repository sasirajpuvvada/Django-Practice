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
from .models import RecommendedArticle, UrlDetails


# Create your views here.

class MainUrl(APIView):

    permission_classes = (IsAuthenticated,)
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
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key},status=HTTP_200_OK)
        else:
            return Response('Invalid credentials')


class Calculate(APIView):

    def get(self, request):
        tf_idf.letsStart()
        return Response('done calculating TF-IDF')

class Search(APIView):

    def post(self, request):
        words = request.data.get('words')
        result = tf_idf.search(words)
        links = []
        for obj in result:
            links.append(obj[0])
        return Response(links)

class Liked(APIView):

    permission_classes = (IsAuthenticated,) 
    def post(self, request):

        curr_user, exists = RecommendedArticle.objects.get_or_create(user = request.user)

        likedArticles = request.data.get('links')
        top_list = tf_idf.liked_articles(likedArticles)
        fav_list = list()
        if  not exists:
            curr_user.delete()
            curr_user = RecommendedArticle.objects.create(user = request.user)
        
        for obj in top_list:
            url = obj['url']
            title = obj['title']
            uid = obj['url_id']
            fav_list.append(url)
            url_obj = UrlDetails(url = url, title = title, uid = uid)
            url_obj.save()
            curr_user.liked_urls.add(url_obj)
            # print(url,title,uid)

        return Response(fav_list)

    def get(self, request):

        curr_user, exists = RecommendedArticle.objects.get_or_create(user = request.user)
        if not exists:
            return Response('No Liked Url Exists')
        sug_urls_data = curr_user.liked_urls.values()
        sug_urls = [obj['url'] for obj in sug_urls_data]
        print(sug_urls)
        return Response(sug_urls)
