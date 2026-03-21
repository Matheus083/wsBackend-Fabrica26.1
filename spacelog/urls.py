from django.urls import path
from .views import APODListView

urlpatterns = [
    path("", APODListView.as_view(), name="apod_list"),
]
