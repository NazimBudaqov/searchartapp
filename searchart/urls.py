from django.contrib import admin
from django.urls import path,include

admin.site.site_header = "SearchArt Admin"
admin.site.site_title = "SearchArt Admin Panel"
admin.site.index_title = "Welcome to SearchArt Admin Panel"

urlpatterns = [
    path('api/', include('apps.searchartapi.urls')),
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
]
