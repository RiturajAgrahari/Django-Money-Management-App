from django.shortcuts import render, redirect
from django.http import request
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.

@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'expenses': expenses,
        'page_obj': page_obj
    }
    return render(request, "index.html", context)


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

def expense_delete(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.warning(request, "Expense Removed!")
    return redirect('expenses')

