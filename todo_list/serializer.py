from rest_framework import serializers

from todo_list.models import Category


class CategoryCreateAndListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class TodoCreateSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(max_length=255)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    due_date = serializers.DateField()

    class Meta:
        model = Category
        fields = ["category_name", "title", "description", "due_date"]


class TodoListSerializer(serializers.ModelSerializer):
    category = CategoryCreateAndListSerializer()
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    due_date = serializers.DateField()

    class Meta:
        model = Category
        fields = ["id", "title", "description", "due_date", "category"]
