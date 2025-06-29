from django.shortcuts import render, get_object_or_404
from .models import Category, BlogPage

def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = BlogPage.objects.live().filter(category=category).order_by('-date')
    return render(request, "home/category_posts.html", {
        "category": category,
        "posts": posts
    })