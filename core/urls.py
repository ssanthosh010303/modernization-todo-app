# Author: Sakthi Santhosh
# Created on: 09/01/2024
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("v1/api/", include("api.urls"))
]
