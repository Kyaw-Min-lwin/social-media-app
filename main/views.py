from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib import messages
from .models import Post, Like, CustomUser, Follow
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


# Create your views here.
def index(request):
    posts = Post.objects.all()
    return render(request, "index.html", {"posts": posts})


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"{username} has been registered")
            return redirect("index")
    form = SignUpForm()
    return render(request, "register.html", {"form": form})


def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        user = request.user
        new_post = Post.objects.create(title=title, content=content, user=user)
        new_post.save()
        return redirect("index")
    return render(request, "create.html")


def like_post(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        # Check if the user has already liked the post
        if Like.objects.filter(user=user, post=post).exists():
            return JsonResponse(
                {"error": "You have already liked this post"}, status=400
            )

        # Create a new like
        like = Like(user=user, post=post)
        like.save()
        print(Like.objects.filter(post=post).count())

        # Return the updated like count as JSON
        updated_likes_count = Like.objects.filter(post=post).count()
        return JsonResponse({"likes": updated_likes_count})
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


def profile(request, user):
    user1 = get_object_or_404(CustomUser, username=user)
    posts = Post.objects.filter(user=user1)
    return render(request, "profile.html", {"posts": posts})

def follow_user(request, user_id):
    user_to_follow = get_object_or_404(CustomUser, pk=user_id)

    # Check if the user is not already following the target user
    if not request.user.following.filter(pk=user_id).exists():
        follow = Follow(follower=request.user, following=user_to_follow)
        follow.save()

    return redirect('user_profile', user_id=user_id)  # Redirect to the user's profile

def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(CustomUser, pk=user_id)

    # Check if the user is following the target user
    if request.user.following.filter(pk=user_id).exists():
        request.user.following_set.filter(following=user_to_unfollow).delete()

    return redirect('user_profile', user_id=user_id)
