from django.contrib import admin
from django.urls import path, include

from user_authentication.views import UserActivationView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('user_authentication/auth/', include('djoser.urls')),
    path('user_authentication/auth/', include('djoser.urls.authtoken')),
    path('user_authentication/auth/', include('djoser.urls.jwt')),
    path('activate/<str:uid>/<str:token>/', UserActivationView.as_view(), name='user_activation'),

    path('booking_system/', include('booking_system.urls')),
    path('report/', include('report.urls')),

]

# urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
