from django.urls import path
from .views import UserView, LandlordView

urlpatterns = [
    path('users/', UserView.as_view(), name="users-all"),
    path('landlords/', LandlordView.as_view(), name="landlords-all")
]