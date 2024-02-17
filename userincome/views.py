from django.shortcuts import render, redirect
from .models import Source, UserIncome
from django.core.paginator import Paginator
from user_preferences.models import UserPreference
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse

# Create your views here.


def search_income(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')

        income = UserIncome.objects.filter(
            amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)

        data = income.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    sources = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    try:
        currency = UserPreference.objects.get(user=request.user).currency
    except:
        messages.error(request, "Select Your preferred currency first!")
        return redirect('preferences')

    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency,
    }
    return render(request, "income.html", context)

@login_required(login_url='/authentication/login')
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
    }

    if request.method == 'GET':
        return render(request, 'add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        date = request.POST['income_date']
        source = request.POST['source']
        description = request.POST['description']
        if not amount:
            context['values'] = request.POST
            messages.error(request, "Amount is required!")
            return render(request, 'add_income.html', context)

        if date:
            UserIncome.objects.create(owner=request.user, amount=amount, date=date, source=source, description=description)
        else:
            UserIncome.objects.create(owner=request.user, amount=amount, source=source, description=description)
        messages.success(request, "Record saved successfully!")
        return redirect('income')

@login_required(login_url='/authentication/login')
def income_edit(request, id):
    income = UserIncome.objects.get(pk=id)
    context = {
        'income': income,
        'values': income
    }
    if request.method == 'GET':
        return render(request, "edit_income.html", context)

    if request.method == 'POST':
        amount = request.POST['amount']
        date = request.POST['income_date']
        source = request.POST['source']
        description = request.POST['description']
        if not amount:
            context['values'] = request.POST
            messages.error(request, "Amount is required!")
            return render(request, 'edit_income.html', context)

        if date:
            income.date = date

        income.amount = amount
        income.source = source
        income.description = description

        income.save()

        messages.success(request, "Income Updated successfully!")
        return redirect('income')


@login_required(login_url='/authentication/login')
def income_delete(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.warning(request, "Income Removed!")
    return redirect('income')
