from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('common.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('documents/', include('documents.urls')),
    path('institution/', include('institution.urls')),
    path('subject/', include('subject.urls'))
]
