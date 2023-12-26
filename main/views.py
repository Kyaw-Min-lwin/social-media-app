from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib import messages
from .models import Post, Like
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
        posts = Post.objects.all()
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
        print(updated_likes_count)
        print("n")
        return JsonResponse({"likes": updated_likes_count})
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)
