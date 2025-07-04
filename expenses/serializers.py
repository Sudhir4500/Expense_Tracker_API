from rest_framework import serializers
from .models import ExpenseIncome
from django.contrib.auth.models import User

class ExpenseIncomeSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()  # Include calculated total in response

    class Meta:
        model = ExpenseIncome
        fields = ['id', 'title', 'description', 'amount', 'transaction_type', 'tax', 'tax_type', 'total','created_at', 'updated_at']  # Fields to serialize

    def get_total(self, obj):
        """Calculate total amount for serialization."""
        return obj.calculate_total()
    

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        """Create a new user with the provided data."""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user