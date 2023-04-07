from django.urls import path
from . import views
from .views import PostListView, PostLikeAPIToggle

app_name = 'article'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('<slug>/', views.detail, name='detail'),
    path('api/<slug>/like/', PostLikeAPIToggle.as_view(), name='like-api'),
    path('article/search/', views.search_results, name='search_results'),
    path('category/<str:categories>/', views.category_view, name='category'),
]

