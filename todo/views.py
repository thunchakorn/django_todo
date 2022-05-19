from time import time
from django.views import View
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.http import JsonResponse
from todo.models import Todo

class TodoList(LoginRequiredMixin, View):

    model = Todo

    def get(self, request):
        due = request.GET.get("due", 'today')
        queryset = self.model.objects.filter(owner=self.request.user).order_by('due')
        if due is None:
            data = queryset.values()
            return JsonResponse({"todo_list": list(data)})
        elif due == 'today':
            queryset = queryset.filter(due__date=timezone.now().date())
            data = queryset.values()
            return JsonResponse({"todo_list": list(data)})
        elif due == 'week':
            today = timezone.now().date()
            delta_day = timezone.timedelta(days=7)
            queryset = queryset.filter(due__range=(today, today+delta_day))
            data = queryset.values()
            return JsonResponse({"todo_list": list(data)})
        else:
            data = queryset.values()
            return JsonResponse({"todo_list": list(queryset)})



class MainView(View):

    template_name = ''

    def get(self, request):
        context = {'now': timezone.now()}
        return render(request, 'todo/main.html', context)
