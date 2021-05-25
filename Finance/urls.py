"""Expense URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
	path('',views.USERLOGIN,name='login'),
	path('signup',views.SIGNUP,name="signup"),
	path('logout', views.USERLOGOUT, name="logout"),
    path('expenses', views.expenses, name="expenses"),
    path('category', views.category, name="category"),
    path('add-expense', views.add_expense, name="add-expenses"),
    path('edit-expense/<int:id>', views.expense_edit, name="expense-edit"),
    path('expense-delete/<int:id>', views.delete_expense, name="expense-delete"),
    path('search-expenses', csrf_exempt(views.search_expenses),
         name="search_expenses"),
    path('expense_category_summary', views.expense_category_summary,
         name="expense_category_summary"),
    path('stats', views.stats_view,
         name="stats"),
    path('income', views.income, name="income"),
    path('add-income', views.add_income, name="add-income"),
    path('edit-income/<int:id>', views.income_edit, name="income-edit"),
    path('income-delete/<int:id>', views.delete_income, name="income-delete"),
    path('search-income', csrf_exempt(views.search_income),
         name="search_income"),
    path('preferences', views.preferences, name="preferences"),
    path('Accounts', views.Accounts, name="Accounts"),
    path('add_account', views.add_account, name="add_account"),
    path('edit-account/<int:id>', views.account_edit, name="edit-account"),
    path('account-delete/<int:id>', views.delete_account, name="account-delete"),
    path('income-goal', views.income_goal, name="income-goal"),
    path('add-income-goal', views.add_income_goal, name="add-income-goal"),
    path('edit-income-goal/<int:id>', views.income_edit_goal, name="income-edit-goal"),
    path('income-goal-delete/<int:id>', views.delete_income_goal, name="income-delete-goal"),
    path('transfer', views.transfer, name="transfer"),
    path('add_transfer', views.add_transfer, name="add_transfer"),
    path('edit-transfer/<int:id>', views.transfer_edit, name="edit-transfer"),
    path('transfer-delete/<int:id>', views.delete_transfer, name="transfer-delete"),
    path("sms", views.sms, name="sms"),
    path("add_sms", views.add_sms, name="add_sms"),

]
