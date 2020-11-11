from django.db import models

# Create your models here.

class UrlDetails(models.Model):

	url = models.CharField(max_length=200)
	title = models.CharField(max_length=200)
	uid = models.CharField(max_length=200, primary_key=True)

	class Meta:
		ordering = ['url','title','uid']

	
	def __str__(self):
		return self.title


class RecommendedArticle(models.Model):

	user = models.CharField(max_length=20)
	liked_urls = models.ManyToManyField(UrlDetails)


	def __str__(self):
		return self.user