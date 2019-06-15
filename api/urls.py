from django.urls import path
from .views import UserView, LandlordView, RatingView, PropertyView

urlpatterns = [
    path('users/', UserView.as_view(), name="users-all"),
    path('landlords/', LandlordView.as_view(), name="landlords-all"),
    path('ratings/', RatingView.as_view(), name="ratings-all"),
    path('properties/', PropertyView.as_view(), name="properties-all")
]