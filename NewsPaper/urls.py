from django.urls import path
from .views import PostsList, PostDetail, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, \
    SearchList, PostCategoryView, unsubscribe_to_category_view, subscribe_to_category

app_name = 'news'
urlpatterns = [
    path('', PostsList.as_view(), name='posts'),
    path('search/', SearchList.as_view(), name='search'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('add/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('category/<int:pk>/', PostCategoryView.as_view(), name='category'),
    path('subscribe/<int:pk>/', subscribe_to_category, name='subscribe'),
    path('unsubscribe/<int:pk>/', unsubscribe_to_category_view, name='unsubscribe'),
]
