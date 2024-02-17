from django.shortcuts import render, redirect
from django.http import request
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
import json
import datetime
from django.http import JsonResponse
from user_preferences.models import UserPreference

# Create your views here.

def search_expenses(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')

        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)

        data = expenses.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    try:
        currency = UserPreference.objects.get(user=request.user).currency
    except:
        messages.error(request, "Select Your preferred currency first!")
        return render(request, 'preferences.html')

    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency,
    }
    return render(request, "index.html", context)

@login_required(login_url='/authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }

    if request.method == 'GET':
        return render(request, 'add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        date = request.POST['expense_date']
        category = request.POST['category']
        description = request.POST['description']
        if not amount:
            context['values'] = request.POST
            messages.error(request, "Amount is required!")
            return render(request, 'add_expense.html', context)

        if date:
            Expense.objects.create(owner=request.user, amount=amount, date=date, category=category, description=description)
        else:
            Expense.objects.create(owner=request.user, amount=amount, category=category, description=description)
        messages.success(request, "Expense saved successfully!")
        return redirect('expenses')

@login_required(login_url='/authentication/login')
def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    context = {
        'expense': expense,
        'values': expense
    }
    if request.method == 'GET':
        return render(request, "edit_expense.html", context)

    if request.method == 'POST':
        amount = request.POST['amount']
        date = request.POST['expense_date']
        category = request.POST['category']
        description = request.POST['description']
        if not amount:
            context['values'] = request.POST
            messages.error(request, "Amount is required!")
            return render(request, 'edit_expense.html', context)

        if date:
            expense.date = date

        expense.owner = request.user
        expense.amount = amount
        expense.category = category
        expense.description = description

        expense.save()

        messages.success(request, "Expense Updated successfully!")
        return redirect('expenses')


@login_required(login_url='/authentication/login')
def expense_delete(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.warning(request, "Expense Removed!")
    return redirect('expenses')


def expense_category_summary(request):
    today_date = datetime.date.today()
    six_months_ago = today_date - datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(owner=request.user, date__gte=six_months_ago, date_lte=today_date)
    finalrep = {}

    def get_category(expense):
        return expense.category

    category_list = list(set(map(get_category(), expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filter_by_category = expenses.filter(category)
        for item in filter_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def stats_view(request):
    return render(request, 'stats.html')
