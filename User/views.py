from cProfile import Profile
from datetime import time
import json
import random
from django.http import HttpResponse, JsonResponse

from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.

def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        emailid = request.POST.get('emailid')
        pwd = request.POST.get('pwd')

        # Optional: Validate inputs here

        try:
            myuser = User.objects.create_user(username=fnm, email=emailid, password=pwd)
            Profile.objects.create(user=myuser, id_user=myuser.id)

            login(request, myuser)
            return redirect('/')
        
        except:
            # Likely a duplicate username
            invalid = "User already exists."
            return render(request, 'signup.html', {'invalid': invalid})

    # GET request
    return render(request, 'signup.html')

def loginn(request):
    if request.method == 'POST':
        username = request.POST.get('fnm')
        password = request.POST.get('pwd')

        # Avoid printing passwords
        print("Login attempt for:", username)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # Or use 'home' if you have named URLs

        # Invalid login
        invalid = "Invalid Credentials."
        return render(request, 'loginn.html', {'invalid': invalid})
    
    # Show the login form on GET request
    return render(request, 'loginn.html')


def logoutt(request):
    logout(request)
    return redirect('/loginn/')

from django.shortcuts import render
from django.db.models import Q

@login_required(login_url='/loginn/')
def home(request):
    # Get the users the current user is following
    following_users = Followers.objects.filter(follower=request.user).values_list('user', flat=True)

    # Get posts by current user and followed users
    post = Post.objects.filter(
        Q(user=request.user) | Q(user__in=following_users)
    ).order_by('-created_at')

    # Get profile of current user
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None  # or handle it differently

    context = {
        'post': post,
        'profile': profile,
    }
    print(request.user.username)

    return render(request, 'main.html', context)


def upload(request):

    if request.method == 'POST':
        user = request.user
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')
 
 

def likes(request, id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=id)
        user = request.user

        liked = LikesPost.objects.filter(post=post, user=user).first()

        if liked:
            liked.delete()
            post.no_of_likes = max(0, post.no_of_likes - 1)  # prevent negative likes
        else:
            LikesPost.objects.create(post=post, user=user)
            post.no_of_likes += 1

        post.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


def explore(request):
    post = Post.objects.all().order_by('-created_at')
    profile = Profile.objects.get(user=request.user)
    
    context = {
        'post':post,
        'profile':profile
    }
    return render(request,'explore.html',context)


def profile(request, username):
    try:
        user_object = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('/')  # or show a 404 page

    try:
        user_profile = Profile.objects.get(user=user_object)
    except Profile.DoesNotExist:
        return redirect('/')  # or create a profile

    user_posts = Post.objects.filter(user=user_object).order_by('-created_at')
    user_post_length = user_posts.count()

    # Current logged-in user
    current_user = request.user

    # Check if current user follows the profile user
    is_following = Followers.objects.filter(follower=current_user, user=user_object).exists()
    follow_unfollow = 'Unfollow' if is_following else 'Follow'

    user_followers = Followers.objects.filter(user=user_object).count()
    user_following = Followers.objects.filter(follower=user_object).count()

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'follow_unfollow': follow_unfollow,
        'user_followers': user_followers,
        'user_following': user_following,
    }

    # Profile editing only allowed for the profile owner
    if current_user == user_object:
        if request.method == 'POST':
            image = request.FILES.get('image')
            bio = request.POST.get('bio', '')
            location = request.POST.get('location', '')

            if image:
                user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

            return redirect('/profile/' + username)

    return render(request, 'profile.html', context)



def delete(request,id):
    post = Post.objects.get(id=id)
    post.delete()
    
    return redirect('/profile/'+request.user.username)

from django.shortcuts import render
from .models import Profile, Post

def search_result(request):
    query = request.GET.get('q', '').strip()  # Prevent errors if q is missing

    profiles = Profile.objects.filter(user__username__icontains=query) if query else []
    posts = Post.objects.filter(caption__icontains=query) if query else []

    context = {
        'query': query,
        'profiles': profiles,
        'profile' : Profile.objects.get(user=request.user),
        'posts': posts
    }
    return render(request, 'search.html', context)


from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Followers

User = get_user_model()


def follow(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        follower_username = request.POST.get('follower')

        # Convert usernames to User objects
        user = get_object_or_404(User, username=username)
        follower = get_object_or_404(User, username=follower_username)

        # Check if the follower already exists
        existing_follow = Followers.objects.filter(user=user, follower=follower).first()

        if existing_follow:
            existing_follow.delete()
        else:
            Followers.objects.create(user=user, follower=follower)

        return redirect('/profile/' + username)

    return redirect('/')



def home_post(request,id):
    post = Post.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    
    context = {
        'post':post,
        'profile':profile
    }
    
    return render(request,'main.html',context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('-created_at')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                post=post,
                user=request.user,
                content=content
            )
            return redirect('post_detail', post_id=post_id)

    return render(request, 'post_detail.html', {
        'profile':Profile.objects.get(user=request.user),
        'post': post,
        'comments': comments,
    })
    
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()


def send_message(request, receiver_username):  # ✅ Make sure this matches your URL
    receiver = get_object_or_404(User, username=receiver_username)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=receiver, content=content)

    messages = Message.objects.filter(
        Q(sender=request.user, receiver=receiver) | 
        Q(sender=receiver, receiver=request.user)
    ).order_by('-timestamp')

    return render(request, 'send_message.html', {
        'receiver': receiver,
        'receiver_username': receiver_username,
        'messages': messages,
        'profile': Profile.objects.get(user=request.user)
    })
    
def user_messages(request):
    if request.method=='POST':
        receiver_name = request.POST.get('receiver')
        content = request.POST.get('content')
        receiver = get_object_or_404(User, username=receiver_name)
        print(receiver_name,content)
        Message.objects.create(sender=request.user, receiver=receiver, content=content)
    user = request.user
    profile = Profile.objects.get(user=user)
    to = User.objects.all()
    print(profile)
    sent_messages = Message.objects.filter(sender=user).order_by('-timestamp')
    received_messages = Message.objects.filter(receiver=user).order_by('-timestamp')
    
    return render(request,'messages.html',context = {
        'to':to,
        'profile': profile,
        'sent_messages':sent_messages,
        'received_messages':received_messages
    })


