from django.urls import path, reverse_lazy
from todo import views

app_name = "todo"

urlpatterns = [
    path('', views.MainView.as_view(template_name='todo/main.html'), name='main'),
    path('todolist/', views.TodoList.as_view(), name='todolist'),
    path('mytodo/', views.TodoListView.as_view(template_name='todo/list.html'), name='mytodo'),
    path('mytodo/<int:pk>', views.TodoDetailView.as_view(template_name='todo/detail.html'), name='detail'),
    path('mytodo/<int:pk>/create', views.TodoCreateView.as_view(template_name='todo/form.html'), name='create'),
    path('mytodo/<int:pk>/update', views.TodoUpdateView.as_view(
        template_name='todo/form.html', success_url=reverse_lazy('todo:mytodo')), name='update'),
    path('mytodo/<int:pk>/delete', views.TodoDeleteView.as_view(
        template_name='todo/delete.html', success_url=reverse_lazy('todo:mytodo')), name='delete'),
]
