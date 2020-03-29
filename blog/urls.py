from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.home, name='home'),
    path('<int:user_id>/', views.profile, name='profile'),
    path('<int:user_id>/<int:blog_id>/', views.personalblog, name='personalblog'),
    path('<int:user_id>/<int:blog_id>/edit/', views.editblog, name='editblog'),
    path('<int:user_id>/<int:blog_id>/delete/', views.deleteblog, name='deleteblog'),
    path('<int:user_id>/createblog/', views.createblog, name='createblog'),
    path('blogs/', views.allblogs, name='allblogs'),
    path('blogs/<int:blog_id>/', views.getblog, name='getblog'),
]
