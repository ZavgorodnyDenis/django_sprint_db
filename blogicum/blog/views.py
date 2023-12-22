from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils import timezone
from .models import Post, Category


def index(request):
    recent_posts = Post.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True  # Фильтр для категории
    ).order_by('-pub_date')[:5]
    return render(request, 'blog/index.html', {'post_list': recent_posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id,
                             is_published=True, pub_date__lte=timezone.now())
    if not post.category.is_published:
        raise Http404("Категория не опубликована")
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug,
                                 is_published=True)
    posts_in_category = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')
    return render(request, 'blog/category.html',
                  {'category': category, 'posts': posts_in_category})
