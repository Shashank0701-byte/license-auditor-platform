from django.urls import path
from .views import scan_dependencies, list_scans

urlpatterns = [
    path('scan/', scan_dependencies),
    path('scans/', list_scans),
]
