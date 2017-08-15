# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.db import models
import uuid


class User(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=120)
    username = models.CharField(max_length=120)
    password = models.CharField(max_length=40)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class SessionToken(models.Model):
    user = models.ForeignKey(User)
    session_token = models.CharField(max_length=255)
    last_request_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def create_token(self):
        self.session_token = uuid.uuid4()



class Post(models.Model):
	user = models.ForeignKey(User)
	image = models.FileField(upload_to='user_images')
	image_url = models.CharField(max_length=255)
	caption = models.CharField(max_length=240)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	has_liked = False


	@property
	def like_count(self):
		return len(Like.objects.filter(post=self))

	@property
	def comments(self):
		return Comment.objects.filter(post=self).order_by('-created_on')

class Like(models.Model):
	user = models.ForeignKey(User)
	post = models.ForeignKey(Post)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)


class Comment(models.Model):
	user = models.ForeignKey(User)
	post = models.ForeignKey(Post)
	comment_text = models.CharField(max_length=555)
	created_on = models.DateTimeField(auto_now_add=True)
updated_on = models.DateTimeField(auto_now=True)