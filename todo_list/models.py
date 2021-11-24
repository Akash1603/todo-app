from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_verified = models.BooleanField(default=False)


class Otp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_otp")
    otp = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    """
    Model for store categories.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_category")
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "category"
        verbose_name_plural = "category"

    def __str__(self):
        return self.name


class Todo(models.Model):
    """
    Model for store todos.
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_todo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    due_date = models.DateField()

    class Meta:
        db_table = "todo"
        verbose_name_plural = "todo"

    def __str__(self):
        return self.title
