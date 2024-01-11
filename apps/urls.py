from django.urls import path

from apps.views import index, login_register, login_page, register, blog_detail_page, blog_list_page

urlpatterns = [
    path('', index, name='index'),
    path('blog-list', blog_list_page, name='blog_list_page'),
    path('blog-detail', blog_detail_page, name='blog_detail_page'),
    path('login', login_page, name='login'),
    path('register', register, name='register'),
    path('login_register', login_register, name="login_register"),

]
