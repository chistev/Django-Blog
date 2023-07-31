from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from requests import post

from .models import Post, Category, Comment
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
            count_str = "likes" if counts != 1 else "like"  # define count_str variable
        data = {
            'updated': updated,
            'liked': liked,
            'likes_count': counts,
            'count_str': count_str
        }
        return Response(data)


def detail(request, slug):
    user_authenticated = request.user.is_authenticated
    # the slug from the models.py is = to the slug passed in via the url request
    post = Post.objects.get(slug=slug)

    # to filter based on category
    category = post.category
    # the category in the models is = to the category value above, and we exclude the current article
    related_articles = Post.objects.filter(category=category).exclude(id=post.id).order_by('-date')[:5]
    if related_articles.count() < 5:
        show_all = False
    else:
        show_all = True
    context = {
                'user_authenticated': user_authenticated,
                'post': post,
                'related_articles': related_articles,
                'show_all': show_all,
               }
    return render(request, 'article/read.html', context=context)


@login_required
# deleting posts
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if not request.user.is_superuser:
        # if the user is not an admin they cannot delete
        return HttpResponseForbidden()
    if request.method == 'POST':
        post.delete()
    return redirect('article:index')


def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    # Check if the current user is the author of the article
    if post.user != request.user:
        # You can customize the error message or redirect to another page
        return HttpResponse("You are not allowed to edit this article.")

    return render(request, 'article/edit_post.html', {'post': post})


def save_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Check if the current user is the author of the article
    if post.user != request.user:
        return HttpResponse("You are not allowed to edit this article.")

    if request.method == 'POST':
        new_content = request.POST.get('new_content')

        # Update the article content
        post.post = new_content

        # Set the edited flag
        post.is_edited = True

        # Save the changes
        post.save()

        # Redirect to the article details page or any other page
        return redirect('article:detail', slug=post.slug)


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

    #category_slugs = categories.split(',')
    #categories = Category.objects.filter(slug__in=category_slugs)
    #articles = Post.objects.filter(category__in=categories)
    context = {'category': category,
               'posts': posts,
               #'category_names': [category.name for category in categories],
               #'articles': articles,
               }
    return render(request, 'article/category.html', context)

# comment functionality


@require_POST
@login_required
def comment_submit(request, slug):
    if request.method == 'POST':
        # Get the comment data from the request and save it to the database
        comment_text = request.POST.get('comment')
        # Assuming you have already authenticated the user
        user = request.user
        post = get_object_or_404(Post, slug=slug)
        comment = Comment.objects.create(post=post, user=user, comment=comment_text)
        comment_data = {
            'user': comment.user.username,
            'date_posted': comment.date_posted.strftime('%Y-%m-%d %H:%M:%S'),
            'comment': comment.comment,
        }
        return JsonResponse(comment_data)
    return JsonResponse({'error': 'Invalid request method'})

# This view is to fetch the comment after a page reload


def get_comments(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comment.objects.filter(post=post)

    comment_list = []
    for comment in comments:
        comment_data = {
            'user': comment.user.username,
            'date_posted': comment.date_posted.strftime('%Y-%m-%d %H:%M:%S'),
            'comment': comment.comment,
        }
        comment_list.append(comment_data)

    return JsonResponse(comment_list, safe=False)