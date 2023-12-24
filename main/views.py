from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib import messages
from .models import Post

# Create your views here.
def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"{username} has been registered")
            return redirect('index')
    form = SignUpForm()
    return render(request, 'register.html',{'form': form})