from django.urls import path
from .views import index, index_table, honeypot_view, basic_post, login, flag_view, index_flag, headers_view, login_2, \
    login_3, about, object_views

urlpatterns = [
    path('', index, name='index'),
    path('basic-post/', basic_post, name='basic_post'),
    path('object/', object_views, name='object_views'),
    path("headers/<page_number>/", headers_view, name="headers_view"),
    path('about.html/', about, name='about'),
    path('login-1/', login, name='login'),
    path('login-2/', login_2, name="login2"),
    path('login-3/', login_3, name='login3'),
    path('bijection/', index_flag, name='index_flag'),
    path('table/', index_table, name='index_table'),
    path('skanerlash/', honeypot_view, name='honeypot'),  # Routes the main honeypot view
    path('skanerlash/<path:path>/', honeypot_view, name='honeypot_files'),
    path('<str:page_name>/', flag_view, name='flag_view')

]
