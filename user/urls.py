from django.urls import path
from .views.views import RegisterView, RetrieveUserView


urlpatterns = [
    path('register', RegisterView.as_view()),
    path('me', RetrieveUserView.as_view()),
]