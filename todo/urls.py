from re import template
from django.urls import path
from todo import views

app_name = "todo"

urlpatterns = [
    path('', views.MainView.as_view(template_name='todo/main.html'), name='main'),
    path('todolist/', views.TodoList.as_view(), name='todolist')
]
