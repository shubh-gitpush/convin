from rest_framework import serializers
from .models import Expense, ExpenseParticipant
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ExpenseParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ExpenseParticipant
        fields = ['user', 'split_method', 'amount_owed', 'percentage_owed']

class ExpenseSerializer(serializers.ModelSerializer):
    participants = ExpenseParticipantSerializer(many=True, read_only=True)
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Expense
        fields = ['id', 'creator', 'description', 'total_amount', 'participants', 'date']
