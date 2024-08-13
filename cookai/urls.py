from django.contrib import admin
from django.urls import path, include
from .views import health_check
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
api_prefix = 'api/v1'

urlpatterns = [
    path(f"{api_prefix}/admin", admin.site.urls),
    path(f"{api_prefix}/health", health_check, name="health_check"),
    path(f"{api_prefix}/users", include("users.urls")),
    path(f"{api_prefix}/articles", include("articles.urls")),
    path(f"{api_prefix}/ai_process", include("ai_process.urls")),
    path(api_prefix, include(router.urls)),  # Add prefix here
]
