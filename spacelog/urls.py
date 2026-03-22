from django.urls import path
from .views import APODListView, APODDetailView, APODCreateView, APODUpdateView, APODDeleteView

app_name = "spacelog"

urlpatterns = [
    path("", APODListView.as_view(), name="apod_list"),
    path("novo/", APODCreateView.as_view(), name="create"), 
    path("<int:pk>/", APODDetailView.as_view(), name="apod_detail"),
    path("<int:pk>/editar/", APODUpdateView.as_view(), name="update"), # <--- Tem que ser 'update'
    path("<int:pk>/deletar/", APODDeleteView.as_view(), name="delete"), # <--- Tem que ser 'delete'
]

