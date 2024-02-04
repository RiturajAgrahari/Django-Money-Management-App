from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.index, name='expenses'),
    path('add_expense', views.add_expense, name='add_expense'),
    path('edit_expense/<int:id>', views.expense_edit, name='expense_edit'),
    path('expense_delete/<int:id>', views.expense_delete, name='expense_delete'),
    path('search_expenses', csrf_exempt(views.search_expenses), name='search_expenses'),
    path('expense_category_summary', views.expense_category_summary, name='expense_category_summary'),
    path('stats', views.stats_view, name='stats'),
]