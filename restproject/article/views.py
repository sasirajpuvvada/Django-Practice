from django.shortcuts import render, get_object_or_404
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

    def put(self, request, pk):
        # saved_article = Article.objects.get(pk = pk)
        saved_article = get_object_or_404(Article,pk = pk)
        data = request.data.get('article')
        serializer = ArticleSerializer(instance = saved_article, data = data)

        if serializer.is_valid():
            article_saved = serializer.save()
        
        return Response({"success": "Article '{}' updated successfully".format(article_saved.title)})

    def delete(self,request, pk):

        article = get_object_or_404(Article.objects.all(), pk=pk)
        article.delete()

        return Response({"success": "Article of id '{}' deleted successfully".format(pk)})

