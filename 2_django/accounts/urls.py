from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('mypage_main/', views.mypage_main, name='mypage_main'),
    path('mypage/', views.mypage, name='mypage'),
    path('bookmark_list/', views.bookmark_list, name='bookmark_list'),
]
    

