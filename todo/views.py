from urllib import request
from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.models import User

from todo.models import Todo
from django.db.models import Q
from todo.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView


class MainView(View):

    template_name = ''

    def get(self, request):
        ctx = {'now': timezone.now()}
        return render(request, 'todo/main.html', ctx)

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

class TodoListView(OwnerListView):

    model = Todo
    template_name = "todo/list.html"

    def get(self, request):
        user = User.objects.get(username=self.request.user)
        mytodo_list = Todo.objects.filter(owner=self.request.user)
        followtodo_list = []
        for f_user in user.following.all():
            followtodo_list.extend(f_user.following_user.todo_owned.all())

        ctx = {"mytodo_list": mytodo_list, "followtodo_list": followtodo_list}
        return render(request, self.template_name, ctx)

class TodoDetailView(OwnerDetailView):

    model = Todo

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(Q(is_public=True) | Q(owner=self.request.user))

class TodoCreateView(OwnerCreateView):

    model = Todo
    fields = [
        "name",
        "detail",
        "due",
        "priority",
        "is_public"
    ]

class TodoUpdateView(OwnerUpdateView):

    model = Todo
    fields = [
        "name",
        "detail",
        "due",
        "priority",
        "is_public"
    ]

class TodoDeleteView(OwnerDeleteView):

    model = Todo
    template_name = "favs/delete.html"
