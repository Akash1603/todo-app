from django.db.models import Q
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenMatchesOASRequirements
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from todo_list.models import Category, Todo
from todo_list.serializer import CategoryCreateAndListSerializer, TodoCreateSerializer, TodoListSerializer


class BaseView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenMatchesOASRequirements]
    required_alternate_scopes = {
        "POST": [["create"]],
        "GET": [["read"]],
        "PUT": [["update"]],
        "DELETE": [["delete"]]
    }


class CategoryCreateAndListView(BaseView):
    @staticmethod
    def post(request):
        serial_data = CategoryCreateAndListSerializer(data=request.data)
        if serial_data.is_valid(raise_exception=True):
            category = Category.objects.create(name=serial_data.validated_data.get("name"), user=request.user)
            return Response({"category_name": category.name}, status=status.HTTP_201_CREATED)

    @staticmethod
    def get(request):
        return Response(CategoryCreateAndListSerializer(Category.objects.filter(user=request.user), many=True).data,
                        status=status.HTTP_200_OK)


class CategoryDetailUpdateAndDeleteView(BaseView):
    @staticmethod
    def get(request, category_id):
        try:
            return Response(
                CategoryCreateAndListSerializer(Category.objects.get(id=category_id, user=request.user)).data,
                status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"Error": f"Category does not exist on given id {category_id}"},
                            status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def put(request, category_id):
        try:
            serial_data = CategoryCreateAndListSerializer(data=request.data)
            if serial_data.is_valid(raise_exception=True):
                category = Category.objects.get(id=category_id, user=request.user)
                category.name = serial_data.validated_data.get("name")
                category.save()
                return Response({}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"Error": f"Category does not exist on given id {category_id}"},
                            status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def delete(request, category_id):
        try:
            Category.objects.get(id=category_id, user=request.user).delete()
            return Response({}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"Error": f"Category does not exist on given id {category_id}"},
                            status=status.HTTP_404_NOT_FOUND)


class TodoCreateAndListView(BaseView):
    @staticmethod
    def post(request):
        try:
            serial_data = TodoCreateSerializer(data=request.data)
            if serial_data.is_valid(raise_exception=True):
                category_name = serial_data.validated_data.get("category_name")
                todo = Todo.objects.create(title=serial_data.validated_data.get("title"),
                                           description=serial_data.validated_data.get("description"),
                                           due_date=serial_data.validated_data.get("due_date"),
                                           category=Category.objects.get(
                                               name=category_name, user=request.user))
                return Response({"todo_title": todo.title}, status=status.HTTP_201_CREATED)
        except Category.DoesNotExist:
            return Response({"Error": f"Category does not exist on given name {category_name}"},
                            status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def get(request):
        title, category, due_date = request.GET.get("title"), request.GET.get("category"), request.GET.get("due_date")
        query = Q()
        if title:
            query.add(Q(title__icontains=title), Q.AND)
        if category:
            query.add(Q(category__name=category), Q.AND)
        if due_date:
            query.add(Q(due_date=due_date), Q.AND)
        return Response(TodoListSerializer(Todo.objects.filter(query, category__user=request.user), many=True).data,
                        status=status.HTTP_200_OK)


class TodoDetailUpdateAndDeleteView(BaseView):
    @staticmethod
    def get(request, todo_id):
        try:
            return Response(TodoListSerializer(Todo.objects.get(id=todo_id, category__user=request.user)).data,
                            status=status.HTTP_200_OK)
        except Todo.DoesNotExist:
            return Response({"Error": f"Todo does not exist on given id {todo_id}"},
                            status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def put(request, todo_id):
        try:
            serial_data = TodoCreateSerializer(data=request.data)
            if serial_data.is_valid(raise_exception=True):
                todo_object = Todo.objects.get(id=todo_id, category__user=request.user)
                for key, value in serial_data.validated_data.items():
                    if key == "category_name":
                        category = Category.objects.get(name=value, user=request.user)
                        todo_object.__setattr__("category", category)
                    else:
                        todo_object.__setattr__(key, value)
                todo_object.save()
                return Response({}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"Error": f"Category does not exist on given id {value}"},
                            status=status.HTTP_404_NOT_FOUND)
        except Todo.DoesNotExist:
            return Response({"Error": f"Todo does not exist on given id {todo_id}"},
                            status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def delete(request, todo_id):
        try:
            Todo.objects.get(id=todo_id, category__user=request.user).delete()
            return Response({}, status=status.HTTP_200_OK)
        except Todo.DoesNotExist:
            return Response({"Error": f"Todo does not exist on given id {todo_id}"},
                            status=status.HTTP_404_NOT_FOUND)
