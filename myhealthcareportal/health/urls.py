from django.urls import path
from . import views

urlpatterns = [
    # Home and authentication views
    path('', views.home, name='home'),  # Home view
    path('login/', views.login_view, name='login'),  # Login view
    path('logout/', views.logout_view, name='logout'),  # Logout view
    path('signup/', views.signup_view, name='signup'),  # Signup view

]
