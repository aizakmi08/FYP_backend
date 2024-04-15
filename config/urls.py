from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', include('rest_framework.urls')),
    path('user_authentication/auth/', include('djoser.urls')),
    path('user_authentication/auth/', include('djoser.urls.authtoken')),
    path('user_authentication/auth/', include('djoser.urls.jwt')),

    path('booking_system/', include('booking_system.urls')),
    path('report/', include('report.urls')),
]

# urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
