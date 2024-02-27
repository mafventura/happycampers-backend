from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.HomeView.as_view(), name ='home'),
    path('logout/', views.LogoutView.as_view(), name ='auth_logout'),
    path('signup/', views.SignupView.as_view(), name='auth_register'),
    path('staff/add', views.AddStaffView.as_view(), name='add_staff'),
]