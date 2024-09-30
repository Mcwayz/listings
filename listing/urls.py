from django.urls import path

from .views import ManageListingView


urlpatterns = [
    path('', ManageListingView.as_view()),
]
