from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense,Account
# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from .models import UserPreference
import datetime
from .models import Source, UserIncome,IncomeGoal,Transfer
from django.conf import settings
import os
from django.contrib import auth
from django.contrib.auth import authenticate,logout,login
from datetime import datetime, date
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta
from twilio.rest import Client


def SIGNUP(request):
    error = ""
    if request.method == "POST":
        f = request.POST['fname']
        l = request.POST['lname']
        c = request.POST['contact']
        e = request.POST['emailid'] 
        ps = request.POST['pwd']
        try:
            user = User.objects.create_user(username=e,password=ps,first_name=f,last_name=l)
            Signup.objects.create(user=user,contact=c)
            error="no"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'signup.html',d)

def USERLOGIN(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['emailid']
        p = request.POST['pwd']
        user = authenticate(username=u,password=p)
        try:
            if user:
                login(request,user)
                error = "no"
        except:
            error = "yes"
    d = {'error':error}
    return render(request,'login.html',d)

def USERLOGOUT(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('login')

def category(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error=""
    if request.method == "POST":
        c1= request.POST['category']
        u1 = User.objects.filter(username = request.user.username).first()
        try:
            Category.objects.create(name=c1)
            error="no"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'expenses/Category.html',d)

def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)



def expenses(request):
    if not request.user.is_authenticated:
        return redirect('login')
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'expenses/index.html', context)


def add_expense(request):
    if not request.user.is_authenticated:
        return redirect('login')
    categories = Category.objects.all()
    accounts = Account.objects.all()
    context = {
        'categories': categories,
        'accounts': accounts,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']
        account = request.POST['acc']
        recurring = request.POST['rec']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(owner=request.user, amount=amount, date=date,
                               category=category, description=description,bank_account=account,recurring=recurring)
        messages.success(request, 'Expense saved successfully')

        return redirect('expenses')



def expense_edit(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    accounts = Account.objects.all()
    context = {
        'expense': expense,
        'accounts': accounts,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']
        account = request.POST['acc']
        recurring =request.POST['rec']
        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/edit-expense.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense. date = date
        expense.category = category
        expense.description = description
        expense.bank_account=account
        expense.recurring=recurring

        expense.save()
        messages.success(request, 'Expense updated  successfully')

        return redirect('expenses')


def delete_expense(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses')


def expense_category_summary(request):
    if not request.user.is_authenticated:
        return redirect('login')
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}

    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def stats_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'expenses/stats.html')

def search_income(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(
            amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)



def income(request):
    if not request.user.is_authenticated:
        return redirect('login')
    categories = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'income/index.html', context)



def add_income(request):
    if not request.user.is_authenticated:
        return redirect('login')
    sources = Source.objects.all()
    accounts = Account.objects.all()
    context = {
        'sources': sources,
        'accounts': accounts,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context)
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']
        account = request.POST['acc']
        recurring = request.POST['rec']
        if not description:
            messages.error(request, 'description is required')
            return render(request, 'income/add_income.html', context)

        UserIncome.objects.create(owner=request.user, amount=amount, date=date,
                                  source=source, description=description,bank_account=account,recurring=recurring)
        messages.success(request, 'Record saved successfully')

        return redirect('income')



def income_edit(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    accounts = Account.objects.all()
    context = {
        'income': income,
        'values': income,
        'accounts': accounts,
        'sources': sources
    }
    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/edit_income.html', context)
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']
        account = request.POST['acc']
        recurring = request.POST['rec']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'income/edit_income.html', context)
        income.amount = amount
        income. date = date
        income.source = source
        income.description = description
        income.bank_account=account
        income.recurring= recurring

        income.save()
        messages.success(request, 'Record updated  successfully')

        return redirect('income')


def delete_income(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'record removed')
    return redirect('income')

def preferences(request):
    if not request.user.is_authenticated:
        return redirect('login')
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})

    exists = UserPreference.objects.filter(user=request.user).exists()
    user_preferences = None
    if exists:
        user_preferences = UserPreference.objects.get(user=request.user)
    if request.method == 'GET':

        return render(request, 'preferences/index.html', {'currencies': currency_data,
                                                          'user_preferences': user_preferences})
    else:

        currency = request.POST['currency']
        if exists:
            user_preferences.currency = currency
            user_preferences.save()
        else:
            UserPreference.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes saved')
        return render(request, 'preferences/index.html', {'currencies': currency_data, 'user_preferences': user_preferences})

def Accounts(request):
    if not request.user.is_authenticated:
        return redirect('login')
    accounts = Account.objects.filter(owner=request.user)
    paginator = Paginator(accounts, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'accounts': accounts,
        'page_obj': page_obj,
    }
    return render(request, 'accounts/index.html', context)

def add_account(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'accounts/add_account.html', context)

    if request.method == 'POST':
        name = request.POST['name']
        bank_account = request.POST['B_A']
        opening_balance = request.POST['O_B']
        account_number = request.POST['A_N']
        description = request.POST['des']

        Account.objects.create(owner=request.user, opening_balance=opening_balance, account_number=account_number,
                               description=description,name=name,bank_account=bank_account)
        messages.success(request, 'Account saved successfully')

        return redirect('Accounts')

def account_edit(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    accounts = Account.objects.get(pk=id)
    context = {
        'accounts': accounts,
        'values': accounts,
    }
    if request.method == 'GET':
        return render(request, 'accounts/edit-account.html', context)
    if request.method == 'POST':
        name = request.POST['name']
        bank_account = request.POST['B_A']
        opening_balance = request.POST['O_B']
        account_number = request.POST['A_N']
        description = request.POST['des']

        accounts.owner = request.user
        accounts.name = name
        accounts.bank_account = bank_account
        accounts.opening_balance = opening_balance
        accounts.account_number = account_number
        accounts.description = description

        accounts.save()
        messages.success(request, 'Accounts updated  successfully')

        return redirect('Accounts')

def delete_account(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    accounts = Account.objects.get(pk=id)
    accounts.delete()
    messages.success(request, 'record removed')
    return redirect('Accounts')

def income_goal(request):
    if not request.user.is_authenticated:
        return redirect('login')
    income_goal = IncomeGoal.objects.filter(owner=request.user)
    paginator = Paginator(income_goal, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'income_goal': income_goal,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'income-goal/index.html', context)



def add_income_goal(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'income-goal/add_income_goal.html', context)

    if request.method == 'POST':
        name = request.POST['name']
        opening_balance = request.POST['opening_balance']
        target = request.POST['target']
        date = request.POST['date']

        IncomeGoal.objects.create(owner=request.user, name=name, date=date,
                                  opening_balance=opening_balance, target=target)
        messages.success(request, 'Record saved successfully')

        return redirect('income-goal')



def income_edit_goal(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    income_goal = IncomeGoal.objects.get(pk=id)
    context = {
        'income_goal': income_goal,
        'values': income_goal,
        
    }
    if request.method == 'GET':
        return render(request, 'income-goal/edit_income_goal.html', context)
    if request.method == 'POST':
        name = request.POST['name']
        opening_balance = request.POST['opening_balance']
        target = request.POST['target']
        date = request.POST['date']

        income_goal.name = name
        income_goal.date = date
        income_goal.opening_balance = opening_balance
        income_goal.target = target

        income_goal.save()
        messages.success(request, 'Record updated  successfully')

        return redirect('income-goal')


def delete_income_goal(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    income_goal = IncomeGoal.objects.get(pk=id)
    income_goal.delete()
    messages.success(request, 'record removed')
    return redirect('income-goal')

def transfer(request):
    if not request.user.is_authenticated:
        return redirect('login')
    transfer = Transfer.objects.filter(owner=request.user)
    paginator = Paginator(transfer, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'transfer': transfer,
        'page_obj': page_obj,
    }
    return render(request, 'transfer/index.html', context)

def add_transfer(request):
    if not request.user.is_authenticated:
        return redirect('login')
    accounts = Account.objects.all()
    context = {
        'accounts':accounts,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'transfer/add_transfer.html', context)

    if request.method == 'POST':
        account_from = request.POST['account_from']
        account_to = request.POST['account_to']
        amount = request.POST['amount']
        note = request.POST['note']
        date = request.POST['date']

        Transfer.objects.create(owner=request.user, account_from=account_from, account_to=account_to,
                               note=note,date=date,amount=amount)
        messages.success(request, 'Account saved successfully')

        return redirect('transfer')

def transfer_edit(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    transfer = Transfer.objects.get(pk=id)
    accounts = Account.objects.all()
    context = {
        'transfer':transfer,
        'accounts': accounts,
        'values': accounts,
    }
    if request.method == 'GET':
        return render(request, 'transfer/edit-transfer.html', context)
    if request.method == 'POST':
        account_from = request.POST['account_from']
        account_to = request.POST['account_to']
        amount = request.POST['amount']
        note = request.POST['note']
        date = request.POST['date']

        transfer.owner = request.user
        transfer.account_from = account_from
        transfer.account_to = account_to
        transfer.amount = amount
        transfer.note = note
        transfer.date = date

        accounts.save()
        messages.success(request, 'Accounts updated  successfully')

        return redirect('transfer')

def delete_transfer(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    transfer = Transfer.objects.get(pk=id)
    transfer.delete()
    messages.success(request, 'record removed')
    return redirect('transfer')

def sms(request):
    if not request.user.is_authenticated:
        return redirect('login')
    sms = SMS.objects.filter(owner=request.user)
    paginator = Paginator(sms, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'sms': sms,
        'page_obj': page_obj,
        
    }
    return render(request, 'sms/index.html', context)

def add_sms(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error=""
    if request.method == "POST":
        p = request.POST['phone']
        m = request.POST['msg']
        try:
            account_sid = 'AC2cc2cf7fdc6d4957482c32f6d6900398'
            auth_token = 'f93440cc4048ae974482bc92b27724f1'
            client = Client(account_sid,auth_token)
            message = client.messages.create(body=m,from_='+14248887992',to=p)
            print(message.sid)
            SMS.objects.create(owner=request.user,to=p,msg=m)
            error="no"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'sms/add_msg.html',d)



