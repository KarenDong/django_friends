# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import re
import bcrypt
import datetime
NAME_REGEX = re.compile(r'^[A-Za-z ]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]*$')

class userManager(models.Manager):
    def register(self,name,alias,email,password,pw_conf,dob):
        error_msg = []
        if not NAME_REGEX.match(name):
            error_msg.append("Name is not valid!")

        if not EMAIL_REGEX.match(email):
            error_msg.append("Email is not valid!")
        else:
            try:
                dupli = self.get(email_iexact=email)
            except:
                dupli = None
            if dupli:
                error_msg.append("Email is registered already!")

        if len(password) < 8:
            error_msg.append("Password should have at least 8 characters!")

        if password != pw_conf:
            error_msg.append("Password do not match the confirmation!")

        if dob == None:
            error_msg.append("Birthday cannot be empty!")

        if error_msg:
            return error_msg
        else:
            pw_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            self.create(name=name, alias=alias, email=email, password=pw_hash, dob=dob)

    def login(self,email,password):
        msg1 = []
        try:
            user = self.get(email=email)
        except:
            user = None
        if not user:
            msg1.append("This email does not exist!")
        elif user.password != bcrypt.hashpw(password.encode(), user.password.encode()):
                msg1.append("Incorect password!")
        return msg1

    def add(self, user_id, friend_id):
        user = self.get(id = user_id)
        friend = self.get(id = friend_id)
        Friend.objects.create(user_friend = user, other_friend = friend)
        Friend.objects.create(user_friend = friend, other_friend = user)

    def remove(self, user_id, friend_id):
        user = self.get(id = user_id)
        friend = self.get(id = friend_id)
        line1 = Friend.objects.get(user_friend = user, other_friend = friend)
        line2 = Friend.objects.get(user_friend = friend, other_friend = user)
        line1.delete()
        line2.delete()

class User(models.Model):
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    dob = models.DateField();
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = userManager()

class Friend(models.Model):
    user_friend = models.ForeignKey(User, related_name='requester')
    other_friend = models.ForeignKey(User, related_name='accepter')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = userManager()
