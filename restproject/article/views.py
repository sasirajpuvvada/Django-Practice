from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Article
from .serializers import ArticleSerializer
# Create your views here.

class ArticleView(APIView):

    def post(self,request):

        article = request.data.get('article')

        serialize = ArticleSerializer(data = article)
        if serialize.is_valid(raise_exception=True):
            article_saved = serialize.save()
        
        return Response({"success": "Article '{}'  created successfully ".format(article_saved.title)})

    def get(self, request):
        articles = Article.objects.all()
        serializers = ArticleSerializer(articles, many = True)
        return Response({"articles":serializers.data})


