from django.urls import path, include

urlpatterns = [
    path('api/', include('scanner_api.urls')),
]
