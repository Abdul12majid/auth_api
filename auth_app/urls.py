from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='sign_up'),
    path('signup2', views.signup2, name='sign_up2'),
    path('login', views.login_user, name='login'),
    path('change_password', views.change_password, name='change-password'),
    path('auth', views.login_auth, name='auth'),
    path('all', views.get_all, name='all'),

]
