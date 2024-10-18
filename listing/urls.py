from django.urls import path

from .views import ManageListingView, ListingDetailView


urlpatterns = [
    path('manage', ManageListingView.as_view()),
    path('detail', ListingDetailView.as_view()),
]
