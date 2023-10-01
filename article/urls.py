from django.urls import path
from . import views
from .views import PostListView, PostLikeAPIToggle, CreatePost

app_name = 'article'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('create_post/', CreatePost.as_view(), name='create_post'),
    path('<slug>/', views.detail, name='detail'),
    path('api/<slug>/like/', PostLikeAPIToggle.as_view(), name='like-api'),
    path('article/search/', views.search_results, name='search_results'),
    path('category/<str:categories>/', views.category_view, name='category'),
    path('article/<str:slug>/delete/', views.delete_post, name='delete_post'),
    path('api/comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('article/edit/<str:slug>/', views.edit_post, name='edit_post'),
    path('article/save/<str:slug>/', views.save_post, name='save_post'),
    path('comment_submit/<str:slug>/', views.comment_submit, name='comment_submit'),
    path('comments/<str:slug>/', views.get_comments, name='get_comments'),
    path('load_more_comments/<slug:slug>/<int:offset>/', views.load_more_comments, name='load_more_comments'),
    path('comment/<int:pk>/like/', views.CommentLikeAPIToggle.as_view(), name='comment-like-api'),

    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('article/save_comment/<int:comment_id>/', views.save_comment, name='save_comment'),
]
