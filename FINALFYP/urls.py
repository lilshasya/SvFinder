from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # <-- ADD this
from django.conf.urls.static import static  # <-- ADD this

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('SVFINDER.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
