#url作成のためのやつ
from django.urls import path
# 同じディレクトリーにいるviews.pyをインポートする
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    #''の部分はそのページのホームの部分。urlの追加は無し。名前も付ける。viewファイルのhomeファンクションが使用される
    path('', views.home, name="home"),
    #ホームのurlにroom/を追加で表示
    path('room/<str:pk>/', views.room, name="room"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
]