from django.urls import path
from .views import AddExpenseView
from .views import expense_list,list

urlpatterns = [
    path('add-expense/', AddExpenseView.as_view(), name='add-expense'),
    path('expenses/', expense_list, name='expense_list'),
    path('list/', list, name='list'),
]
