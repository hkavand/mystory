from django.contrib import admin
from .models import Todo
from .models import AboutUser
from .models import Comment

class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


admin.site.register(Todo,TodoAdmin)
admin.site.register(AboutUser)
admin.site.register(Comment)
