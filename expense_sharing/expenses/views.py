from django.shortcuts import get_object_or_404
from .models import Expense, ExpenseParticipant
from .serializers import ExpenseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
import csv
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http import JsonResponse
import logging


class AddExpenseView(APIView):
    permission_classes = [AllowAny]
      # Allow unauthenticated access (for testing)

    def post(self, request):
        data = request.data
        total_amount = data.get('total_amount')
        description = data.get('description')
        participants = data.get('participants')

        if not total_amount or not description or not participants:
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        # Allow creator to be None or an anonymous user
        creator = request.user if request.user.is_authenticated else None

        # Create the expense without requiring a creator
        expense = Expense.objects.create(creator=creator, total_amount=total_amount, description=description)

        total_percentage = 0
        for participant in participants:
            user = get_object_or_404(User, id=participant['user_id'])
            split_method = participant['split_method']
            amount_owed = participant.get('amount_owed', 0)
            percentage_owed = participant.get('percentage_owed', 0)

            # Validate and calculate amounts based on split method
            if split_method == 'equal':
                num_participants = len(participants)
                amount_owed = total_amount / num_participants
            elif split_method == 'percentage':
                if not percentage_owed:
                    return Response({"error": "Percentage owed is required for percentage split."},
                                    status=status.HTTP_400_BAD_REQUEST)
                total_percentage += percentage_owed
                if total_percentage > 100:
                    return Response({"error": "Total percentage exceeds 100%."}, status=status.HTTP_400_BAD_REQUEST)
                amount_owed = (percentage_owed / 100) * total_amount
            elif split_method == 'exact':
                if not amount_owed:
                    return Response({"error": "Amount owed is required for exact split."},
                                    status=status.HTTP_400_BAD_REQUEST)

            # Create ExpenseParticipant entry
            ExpenseParticipant.objects.create(
                expense=expense,
                user=user,
                split_method=split_method,
                amount_owed=amount_owed,
                percentage_owed=percentage_owed
            )

        return Response({"message": "Expense created successfully!"}, status=status.HTTP_201_CREATED)


def download_balance_sheet(request, user_id):
    user = get_object_or_404(User, id=user_id)
    expenses = user.expenses.all()

    # Create the HttpResponse object with the CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="balance_sheet.csv"'

    writer = csv.writer(response)
    writer.writerow(['Expense', 'Total Amount', 'Amount Owed'])

    for expense in expenses:
        for participant in expense.participants.all():
            if participant.user == user:
                writer.writerow([expense.description, expense.total_amount, participant.amount_owed])

    return response


logger = logging.getLogger(__name__)


def expense_list(request):
    expense_data = []

    # Fetch all ExpenseParticipant instances
    expense_participants = ExpenseParticipant.objects.all()

    # Loop through each ExpenseParticipant
    for participant in expense_participants:
        expense = participant.expense
        expense_data.append({
            "user": participant.user.username,
            "amount_owed": str(participant.amount_owed),
            "expense": {
                "id": expense.id,
                "description": expense.description,
                "total_amount": str(expense.total_amount),
                "creator": expense.creator.username if expense.creator else None,
                "percentage_owed":str(participant.percentage_owed) if participant.percentage_owed is not None else None,
                "split_method":str(participant.split_method) if participant.split_method is not None else None
            }
        })

    return JsonResponse(expense_data, safe=False)
def list(request):
    expensepart = ExpenseParticipant.objects.all()
    expense_data = []
    for expense in expensepart:
        expense_data.append({
            "user": expense.user.username,
            "amount_owed": str(expense.amount_owed),
            "expense": expense.expense.description,
        })


    return JsonResponse(expense_data, safe=False)
