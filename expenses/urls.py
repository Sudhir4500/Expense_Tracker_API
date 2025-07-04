# URL routing for the expenses app
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseIncomeViewSet

router = DefaultRouter()
router.register(r'expenses', ExpenseIncomeViewSet, basename='expenses')  # Register ExpenseIncomeViewSet with explicit basename

urlpatterns = [
    path('', include(router.urls)),  # Include router-generated URLs
]