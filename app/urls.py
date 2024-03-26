from django.urls import path
from . import views

urlpatterns = [
     path('', views.index, name='index'),
     path('single/', views.single, name='single'),
     path('login/', views.login_view, name='login'),
     path('register/', views.register, name='register'),
     path('single/<int:post_id>/', views.post_detail, name='single'),
     path('review/', views.review_posts, name='review_posts'),
     path('approve/<int:post_id>/', views.approve_post, name='approve_post'),
     path('createpost/', views.create_post, name='createpost'),
     path('logout/', views.logout_view, name='logout'),

]
