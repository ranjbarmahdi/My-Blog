from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<slug:category>/', views.post_list, name='post_list_by_category'),
    path('post/<int:id>', views.post_detail, name='post_detail'),
    path('contact-us/', views.ticket, name='ticket'),
]