from django.urls import path
from .views import ListAllUsersView

urlpatterns = [
    path('users/', ListAllUsersView.as_view(), name="users-all")
]