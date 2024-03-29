import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST, require_http_methods
from requests import post

from .forms import PostForm
from .models import Post, Category, Comment
from django.shortcuts import render, redirect

from django.db.models import Q


from django.views.generic import ListView, RedirectView, CreateView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from django.http import JsonResponse
from .models import Comment


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


class CommentLikeAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        comment = get_object_or_404(Comment, pk=pk)
        user = self.request.user
        updated = False
        liked = False
        if user.is_authenticated:
            if user in comment.likes.all():
                liked = False
                comment.likes.remove(user)
            else:
                liked = True
                comment.likes.add(user)
            updated = True
            counts = comment.likes.count()
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
    post = get_object_or_404(Post, slug=slug)

    # to filter based on category
    category = post.category
    # the category in the models is = to the category value above, and we exclude the current article
    related_articles = Post.objects.filter(category=category).exclude(id=post.id).order_by('-date')[:5]
    if related_articles.count() < 5:
        show_all = False
    else:
        show_all = True

    # Load comments for the post
    comments = post.comments.order_by('-date_posted')
    batch_size = 10  # Set the number of comments to load per batch
    total_comments = comments.count()

    # Get the 'offset' parameter from the request's query string
    offset = int(request.GET.get('offset', 0))

    # Check if there are more comments to load
    if total_comments > batch_size + offset:
        show_load_more = True
        comments = comments[offset: offset + batch_size]
    else:
        show_load_more = False
        comments = comments[offset:]

    context = {
        'user_authenticated': user_authenticated,
        'post': post,
        'related_articles': related_articles,
        'show_all': show_all,
        'comments': enumerate(comments),
        'show_load_more': show_load_more,
        'batch_size': batch_size,
        'total_comments': total_comments,
    }

    return render(request, 'article/read.html', context=context)


def load_more_comments(request, slug, offset):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.order_by('-date_posted')
    batch_size = 10

    offset = int(offset)  # Convert the offset to an integer

    if offset > 0:
        comments = comments[offset:offset + batch_size]
    else:
        comments = comments[:batch_size]

    data = []
    for comment in comments:
        data.append({
            'user': comment.user.username,
            'date_posted': comment.date_posted.strftime('%Y-%m-%d %H:%M:%S'),
            'comment': comment.comment,
        })

    return JsonResponse(data, safe=False)


@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if not request.user.is_superuser:
        # if the user is not an admin they cannot delete
        return HttpResponseForbidden()
    if request.method == 'POST':
        post.delete()
    return redirect('article:index')


@login_required
@require_http_methods(["DELETE"])
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    # Check if the current user is the author of the comment
    if comment.user != request.user:
        return JsonResponse({'error': 'You are not allowed to delete this comment.'}, status=403)

    # Store the comment ID for reference in the JSON response
    deleted_comment_id = comment.id

    comment.delete()

    # Include the deleted comment ID in the response
    return JsonResponse({'message': 'Comment deleted successfully', 'deleted_comment_id': deleted_comment_id})


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


def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Check if the current user is the author of the comment
    if comment.user != request.user:
        return HttpResponse("You are not allowed to edit this comment.")

    return render(request, 'article/edit_comment.html', {'comment': comment})


def save_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    # Check if the current user is the author of the comment
    if comment.user != request.user:
        return HttpResponse("You are not allowed to edit this comment.")

    if request.method == 'POST':
        new_content = request.POST.get('new_content')

        # Update the comment content
        comment.comment = new_content

        # Set the edited flag
        comment.is_edited = True

        # Save the changes
        comment.save()

        # Redirect to the post detail page or any other appropriate page
        return redirect('article:detail', slug=comment.post.slug)


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


def is_superuser(user):
    return user.is_superuser


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'article/create_post.html'

    def form_valid(self, form):
        # Set the user field to the current logged-in user
        form.instance.user = self.request.user

        # Check if an image was uploaded
        if 'image' in self.request.FILES:
            uploaded_image = self.request.FILES['image']

            # Define the path where the image should be saved in MEDIA_ROOT
            image_path = os.path.join(uploaded_image.name)

            # Save the uploaded image to the defined path
            with open(os.path.join(settings.MEDIA_ROOT, image_path), 'wb') as destination:
                for chunk in uploaded_image.chunks():
                    destination.write(chunk)

            # Set the image field to the relative path of the saved image
            form.instance.image = image_path

        else:
            # Handle the case where no image was uploaded (optional)
            messages.warning(self.request, 'No image uploaded.')

        # Continue with the form validation
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the detail page of the newly created post
        return reverse('article:detail', kwargs={'slug': self.object.slug})

    @classmethod
    def as_view(cls, **kwargs):
        view = super(CreatePost, cls).as_view(**kwargs)
        return login_required(user_passes_test(lambda u: u.is_superuser)(view))
