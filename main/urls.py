from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="main_home"),
    path('today/',views.today,name="main_today"),
    path('NextSevenDays/',views.week,name="main_week"),
    path('important/', views.showImportanTasks, name="importantTasks"),
    path('add/', views.addNewTask, name="addNewTask"),
    path('<int:pk>/update/', views.update, name="updateTask"),
    path('<int:pk>/Done/', views.taskIsDone, name="taskIsDone"),
    path('Delete/<int:pk>', views.deleteTask, name="deleteTask"),
    path('DoneList/', views.showDoneTasks, name="doneList"),
    path('<int:pk>/is_important/', views.setImportant, name="taskIsImportant")
]
