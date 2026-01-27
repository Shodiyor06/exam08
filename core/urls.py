from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from accounts.views import login_view, logout_view, register_view

from .views import stats_page

urlpatterns = [
    # ===== ADMIN PANEL =====
    path("admin/", admin.site.urls),

    # ===== AUTHENTICATION (HTML) =====
    path("", login_view, name='home'),
    path("login/", login_view, name='login'),
    path("register/", register_view, name='register'),
    path("logout/", logout_view, name='logout'),

    # ===== HTML VIEWS =====
    path("events/", include("events.urls")),
    path("registrations/", include("registrations.urls")),
    path("stats/", stats_page, name='stats'),

    # ===== JWT AUTHENTICATION =====
    path("api/accounts/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/accounts/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # ===== API ENDPOINTS =====
    path("api/accounts/", include("accounts.urls")),
    path("api/events/", include("events.urls")),
    path("api/registrations/", include("registrations.urls")),
]