from . import views
from django.contrib import admin
from django.urls import path, re_path
urlpatterns = [
    path('signup',views.signup,name="signup"),
    path('login',views.login,name="login"),
    path('logout',views.logout,name="logut"),
    path('select',views.select,name='select'),
    path('confirm_signup',views.confirm_signup,name='confirm_signup'),
    path('confirm_signup/', views.confirm_signup, name='confirm_signup'),
    re_path(r'^(?P<remaining_url>.*)$', views.handle_enter_url, name='handle_enter_url'),

]
