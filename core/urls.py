from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.views import login_view, register_view
from .views import stats_page

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", login_view),
    path("login/", login_view),
    path("register/", register_view),

    path("events/", include("events.urls")),          # ✅ FAqat shu
    path("registrations/", include("registrations.urls")),
    path("stats/", stats_page),

    # JWT
    path("api/accounts/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/accounts/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/accounts/", include("accounts.urls")),
]
