from django.urls import path
from .views import scan_dependencies, list_scans, scan_details

urlpatterns = [
    path('scan/', scan_dependencies),
    path('scans/', list_scans),
    path('scans/<int:scan_id>/', scan_details),
]
