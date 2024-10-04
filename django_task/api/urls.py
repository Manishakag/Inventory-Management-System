from django.urls import path

from .views import *

urlpatterns = [
    path("create", CreateItem.as_view(), name="create-item"),
    path("items", ReadItem.as_view(), name="item-list"),
    path("update/<str:pk>", UpdateItem.as_view(), name="update-item"),
    path("delete/<str:pk>", DeleteItem.as_view(), name="delete-item"),
]
