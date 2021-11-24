from django.urls import path

from todo_list.views import TodoCreateAndListView, CategoryCreateAndListView, CategoryDetailUpdateAndDeleteView, \
    TodoDetailUpdateAndDeleteView

urlpatterns = [
    path('category/', CategoryCreateAndListView.as_view(), name="category_create_and_list"),
    path('category/<int:category_id>/', CategoryDetailUpdateAndDeleteView.as_view(),
         name="category_detail_update_and_delete"),
    # ---------------------------------todo_model endpoints---------------------------------------------
    path('todo/', TodoCreateAndListView.as_view(), name="todo_create_and_list"),
    path('todo/<int:todo_id>/', TodoDetailUpdateAndDeleteView.as_view(), name="todo_detail_update_and_delete")
]