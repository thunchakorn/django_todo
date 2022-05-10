from django.contrib import admin

from todo.models import Priority, Todo, Comment, Following, Participant

# Register your models here.
admin.site.register(Priority)
admin.site.register(Todo)
admin.site.register(Comment)
admin.site.register(Following)
admin.site.register(Participant)
