from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import ExpenseIncome
from .serializers import ExpenseIncomeSerializer,RegisterSerializer
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

class IsSuperUserOrOwner(BasePermission):
    """Custom permission to allow superusers to access all records and users to access only their own."""
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj.user == request.user

class ExpenseIncomeViewSet(viewsets.ModelViewSet):
    """ViewSet for handling CRUD operations on ExpenseIncome model."""
    serializer_class = ExpenseIncomeSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrOwner]  # Require authentication and ownership/superuser status

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ExpenseIncome.objects.all().order_by('-created_at')
        return ExpenseIncome.objects.filter(user=self.request.user).order_by('-created_at')


    def perform_create(self, serializer):
        """Assign the current user to the record during creation."""
        serializer.save(user=self.request.user)



class RegisterView(generics.CreateAPIView):
    """View for user registration."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny] # anyone can register