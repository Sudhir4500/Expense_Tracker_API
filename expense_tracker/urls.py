
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from expenses.views import RegisterView  # Import custom registration view

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin interface
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT login endpoint
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT token refresh endpoint
    path('api/auth/register/', RegisterView.as_view(), name='register'),  # Custom user registration endpoint
    path('api/', include('expenses.urls')),  # Expense/Income API endpoints
]