from django.urls import path

from . import views
from .views import (
    PostListView,PostDetailView,UserPostListView
)
urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),    
    path('post/new/', views.post_new, name='post-create'),
    path('post/<int:pk>/update/',views.post_edit, name='post-update'),
    path('post/<int:pk>/delete/', views.post_delete, name='post-delete'),
    path('post/<int:pk>/likes/',views.post_like, name="post-like"),
    path('comment/<int:pk>/',views.add_comment_to_post, name='comment'),
    path('comment/<int:pk>/edit/',views.comment_edit, name='comment-edit'),
    path('comment/<int:pk>/delete/',views.comment_delete, name='comment-delete'),
    path('post/<int:pk>/comments/',views.comment_list, name='comments'),
    # path('user/<int:pk>/posts/',views.user_post_list, name='user-posts'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('about/', views.about, name='about'),
]