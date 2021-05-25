from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Expense)
admin.site.register(Category)
admin.site.register(UserIncome)
admin.site.register(Source)
admin.site.register(Account)
admin.site.register(UserPreference)
admin.site.register(IncomeGoal)
admin.site.register(Transfer)
admin.site.register(SMS)

