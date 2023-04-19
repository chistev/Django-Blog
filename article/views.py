from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse

from .models import Post, Category
from django.shortcuts import render, redirect

from django.db.models import Q


from django.views.generic import ListView, RedirectView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions


class PostListView(ListView):
    paginate_by = 5
    model = Post
    ordering = ['-date']


# implementing like and unlike functionality
class PostLikeAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, slug=None, format=None):
        obj = get_object_or_404(Post, slug=slug)
        user = self.request.user
        updated = False
        liked = False
        if user.is_authenticated:
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
            else:
                liked = True
                obj.likes.add(user)
            updated = True
            counts = obj.likes.count()
        data = {
            'updated': updated,
            'liked': liked,
            'likes_count': counts
        }
        return Response(data)


def detail(request, slug):
    # the slug from the models.py is = to the slug passed in via the url request
    post = Post.objects.get(slug=slug)

    context = {'post': post}
    return render(request, 'article/read.html', context)


def search_results(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(Q(title__icontains=query) | Q(post__icontains=query))
    context = {
        'query': query,
        'posts': posts
    }
    return render(request, 'article/search_results.html', context)


def category_view(request, categories):
    category = get_object_or_404(Category, name__exact=categories)
    posts = category.posts.all()
    context = {'category': category,
               'posts': posts
               }
    return render(request, 'article/category.html', context)
