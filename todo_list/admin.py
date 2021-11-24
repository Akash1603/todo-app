from django.contrib import admin

from todo_list.models import Category, Todo


@admin.register(Category, Todo)
class UniversalAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]
