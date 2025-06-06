from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('common.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('documents/', include('document.urls')),
    path('institution/', include('institution.urls')),
    path('subject/', include('subject.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
