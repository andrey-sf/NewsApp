from django.urls import path
from .views import RegisterView, LoginView, LogoutView, IndexView, upgrade_me

app_name = 'sign'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', RegisterView.as_view(), name='signup'),
]
