# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.db import models
from models import User, Friend
from django.contrib import messages
import datetime
import re
import bcrypt

def index(request):
    return render(request,'first_app/index.html')

def register(request):
    if request.method == "POST":
        name = request.POST['name']
        alias = request.POST['alias']
        email = request.POST['email']
        password = request.POST['password']
        pw_conf = request.POST['pw_conf']
        dob = request.POST['dob']
        print "checking information..."
        error1 = User.objects.register(name,alias,email,password,pw_conf,dob)
        if error1:
            for error in error1:
                messages.error(request, error)
            return redirect('/')
        else:
            print "User is being created..."
            messages.success(request, 'You Just registered an account!')
            return redirect('/')

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        print "checking information..."
        error2 = User.objects.login(email,password)
        if error2:
            for error in error2:
                messages.error(request, error)
            return redirect('/')
        else:
            print "Login to the account..."
            request.session['id'] = User.objects.get(email=request.POST['email']).id
            return redirect('/friends')

def friends(request):
    me = User.objects.get(id=request.session['id'])
    all_user = User.objects.all()
    friendship = Friend.objects.filter(user_friend=me)
    other_user = []
    for each_other in all_user:
        if(each_other.id != request.session['id']):
            other_user.append(each_other)
    try:
        my_friends = []
        others = []
        for each_friendship in friendship:
            my_friends.append(each_friendship.other_friend)
        for each_user in other_user:
            if (each_user not in my_friends):
                others.append(each_user)
    except:
        friendship = None

    context = {
        "me":me,
        "friends": my_friends,
        "users":others
    }
    return render(request, "first_app/friends.html", context)

def info(request, id):
    friend_info = User.objects.get(id=id)
    context ={
        "user": friend_info
    }
    return render(request, "first_app/user.html", context)

def add(request, id):
    User.objects.add(request.session['id'],id)
    return redirect('/friends')

def remove(request, id):
    User.objects.remove(request.session['id'],id)
    return redirect('/friends')

def logout(request):
    request.session['id'] = 0
    return redirect('/')
