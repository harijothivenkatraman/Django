from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('store/', include('store.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Add this line for authentication
    path("logout/", LogoutView.as_view(), name="logout-get"),
    path('', RedirectView.as_view(url='store/')),  # Redirect root URL to /store/
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)