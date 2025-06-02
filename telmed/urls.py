from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from rest_framework_simplejwt.views import TokenVerifyView


admin.site.site_header = 'TelMed'

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path('dashboard/', dashboard ,name='dashboard' ),
    path('',home_page, name='home_page'),
    path('privacy_policy/',privacy_policy, name='privacy_policy'),
    path('delete_account/',delete_account, name='delete_account'),
    path('auth_login/',auth_login, name='login_page'),
    path('logout/', logoutPage, name='logout'),
    path('',include('user.urls')),
    path('',include('prescription.urls')),
    path('',include('conference.urls')),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
