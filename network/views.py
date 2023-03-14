import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, UserLikesPosts
from .forms import PostForm
import logging


def index(request):

    post_form = PostForm()

    # TODO: Fetch Posts with pagination
    if request.method == "GET":
        
        post_objects = json.loads(posts(request).content)

        return render(request, "network/index.html", {
            "post_form": post_form,
            "posts": post_objects,
        })


def view_post(request, post_id):

    # TODO: Open page that shows the post itself
    if request.method == "GET":
        pass


def posts(request):

    if request.method == "GET":
        posts = Post.objects.all()
        posts = posts.order_by("-date_created").all()

        return JsonResponse([post.serialize() for post in posts],
                            safe=False)

    elif request.method == "POST":

        if not request.user.is_authenticated:
            return JsonResponse({
                "message": "Must be logged in to make a post"
            })

    data = json.loads(request.body)

    post = Post(
        poster=request.user,
        message=data['message'],
    )
    
    post.save()
    return JsonResponse({"message": "Post successfully created"}, safe=False)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
