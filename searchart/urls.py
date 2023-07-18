from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('api/', include('apps.searchartapi.urls')),
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
]
