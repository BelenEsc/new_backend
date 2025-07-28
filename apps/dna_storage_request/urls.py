from django.urls import path
from .views import HomeView, MensajeView, StorageRequestView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('api/mensaje/', MensajeView.as_view()),
    path('api/storage-requests/', StorageRequestView.as_view()),
]