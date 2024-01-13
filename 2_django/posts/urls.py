from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('hit/', views.hit, name='hit'),
    path('score/', views.score, name='score'),

    path('create/', views.create, name='create'),
    path('create_by_img', views.create_by_img, name='create_by_img'),
    path('detail/<int:post_id>/', views.post_detail, name='post_detail'),
    path('delete/<int:post_id>/', views.post_delete, name='post_delete'),
    path('update/<int:post_id>/', views.post_update, name='post_update'),
    path('<int:post_id>/bookmark/', views.bookmark, name='bookmark'),
    

    path('cate1/1', views.index_cate1_1, name='cate1_1'),
    path('cate1/2', views.index_cate1_2, name='cate1_2'),
    path('cate1/3', views.index_cate1_3, name='cate1_3'),
    path('cate1/4', views.index_cate1_4, name='cate1_4'),
    
    path('cate2/1', views.index_cate2_1, name='cate2_1'),
    path('cate2/2', views.index_cate2_2, name='cate2_2'),
    path('cate2/3', views.index_cate2_3, name='cate2_3'),
    path('cate2/4', views.index_cate2_4, name='cate2_4'),
    path('cate2/5', views.index_cate2_5, name='cate2_5'),
    path('cate2/6', views.index_cate2_6, name='cate2_6'),
    
    path('cate3/1', views.index_cate3_1, name='cate3_1'),
    path('cate3/2', views.index_cate3_2, name='cate3_2'),
    path('cate3/3', views.index_cate3_3, name='cate3_3'),
    path('cate3/4', views.index_cate3_4, name='cate3_4'),
    path('cate3/5', views.index_cate3_5, name='cate3_5'),
    path('cate3/6', views.index_cate3_6, name='cate3_6'),
    path('cate3/7', views.index_cate3_7, name='cate3_7'),
    path('cate3/8', views.index_cate3_8, name='cate3_8'),
    path('cate3/9', views.index_cate3_9, name='cate3_9'),
    path('cate3/10', views.index_cate3_10, name='cate3_10'),
    path('cate3/11', views.index_cate3_11, name='cate3_11'),
    path('cate3/12', views.index_cate3_12, name='cate3_12'),
    path('cate3/13', views.index_cate3_13, name='cate3_13'),
    path('cate3/14', views.index_cate3_14, name='cate3_14'),
    
    path('search/', views.search, name='search'),
    
    path('recommend/', views.recommend, name='recommend'),
    path('rating_create/<int:post_id>/', views.rating_create, name='rating_create'),
    path('imgsearch/', views.imgsearch, name='imgsearch'),
]
