from django.urls import path
from .views import UserView, UserRatingsView, LandlordView, LandlordIDView, RatingView, PropertyView, PropertyIDView

urlpatterns = [
    path('user/', UserView.as_view(), name="create-user"),
    path('user/ratings/', UserRatingsView.as_view(), name="user-ratings"),
    path('landlord/', LandlordView.as_view(), name="landlords"),
    path('landlord/id/', LandlordIDView.as_view(), name="landlord-id"),
    path('rating/', RatingView.as_view(), name="ratings"),
    path('property/', PropertyView.as_view(), name="properties"),
    path('property/id/', PropertyIDView.as_view(), name="property-id")
]