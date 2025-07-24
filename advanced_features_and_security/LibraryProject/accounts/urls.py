# advanced_features_and_security/urls.py

from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # ... your app urls (e.g., path('admin/', admin.site.urls))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
