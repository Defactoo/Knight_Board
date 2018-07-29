from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator

# Create your models here.

class Board(models.Model):
	name = models.CharField(max_length=30, unique=True)
	descriptions = models.CharField(max_length=100)

	def __str__(self):
		return self.name
	def get_posts_count(self):
		return Post.objects.filter(topic__board=self).count()
	def get_last_post(self):
		return Post.objects.filter(topic__board=self).order_by('-create_at').first()

class Topic(models.Model):
	subject = models.CharField(max_length=255)
	last_updated = models.DateTimeField(auto_now_add=True)
	board = models.ForeignKey(Board, models.CASCADE, related_name='topics')
	starter = models.ForeignKey(User, models.CASCADE, related_name='topics')
	def __str__(self):
		return self.subject

class Post(models.Model):
	message = models.TextField(max_length=4000)
	topic = models.ForeignKey(Topic,models.CASCADE, related_name='posts')
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(null=True)
	create_by = models.ForeignKey(User, models.CASCADE, related_name='posts')
	updated_by = models.ForeignKey(User, models.CASCADE, null=True, related_name='+')

	def __str__(self):
		truncated_message = Truncator(self.message)
		return truncated_message.chars(30)
