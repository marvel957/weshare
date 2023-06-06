from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.loginPage, name = 'login'),
    path('register/',views.registerPage, name = 'register'),
    path('logout/',views.logoutPage, name = 'logout'),
    path('',views.home, name = 'home'),
    path('room/<str:pk>/',views.room, name = 'room'),
    path('userprofile/<str:pk>/',views.UserProfile, name = 'userprofile'),
    path('create_room/',views.CreateRoom, name = 'create_room'),
    path('update_room/<str:pk>/',views.UpdateRoom, name = 'update_room'),
    path('delete_room/<str:pk>/',views.DeleteRoom, name = 'delete_room'),
    path('delete_message/<str:pk>/',views.DeleteMessage, name = 'deletemessage'),
    path('update_user/',views.updateuser, name = 'update_user'),
    path('topics/',views.topiclist, name = 'topics'),
    path('activity/',views.activityPage, name = 'activity'),
]