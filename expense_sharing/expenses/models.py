from django.db import models
from django.contrib.auth.models import User


class Expense(models.Model):
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - {self.total_amount}"


class ExpenseParticipant(models.Model):
    SPLIT_METHOD_CHOICES = [
        ('equal', 'Equal'),
        ('exact', 'Exact'),
        ('percentage', 'Percentage')
    ]

    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    split_method = models.CharField(max_length=10, choices=SPLIT_METHOD_CHOICES)
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    percentage_owed = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user} owes {self.amount_owed} for {self.expense}"
