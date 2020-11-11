from django.contrib import admin
from .models import RecommendedArticle, UrlDetails
# Register your models here.

admin.site.register(UrlDetails)
admin.site.register(RecommendedArticle)
