from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<slug:category>/', views.post_list, name='post_list_by_category'),
    path('post/<int:id>', views.post_detail, name='post_detail'),
    path('post/<int:id>/comment', views.post_comment, name='post_comment'),
    path('contact-us/', views.ticket, name='ticket'),
    path('posts/search', views.post_search, name='post_search'),
    path('profile/', views.profile_posts, name='profile_posts'),
    path('profile/create_post', views.create_post, name='create_post'),
    path('profile/delete_post/<int:id>', views.delete_post, name='delete_post'),
    path('profile/edit_post/<int:id>', views.edit_post, name='edit_post'),
    path('profile/delete_image/<int:image_id>', views.delete_image, name='delete_image'),
    path('profile/personal_detail', views.personal_detail, name='personal_detail'),
    path('profile/edit_personal_detail', views.edit_personal_detail, name='edit_personal_detail'),
    path('change_password/', views.change_password, name='change_password'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register, name='register'),

]