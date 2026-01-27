from django.urls import path
from .views import scan_dependencies

urlpatterns = [
    path('scan/', scan_dependencies),
]
