from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now

# Create your models here.

class Signup(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    contact = models.CharField(max_length=10,null=True)
    
    def __str__(self):
        return self.user.username

class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=266)
    bank_account = models.CharField(max_length=266,default='SOME STRING')
    recurring = models.CharField(max_length=266,default='SOME STRING')

    class Meta:
        ordering: ['-date']
        

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class UserIncome(models.Model):
    amount = models.FloatField()  # DECIMAL
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    source = models.CharField(max_length=266)
    bank_account = models.CharField(max_length=266,default='SOME STRING')
    recurring = models.CharField(max_length=266,default='SOME STRING')

    def __str__(self):
        return self.source

    class Meta:
        ordering: ['-date']


class Source(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class UserPreference(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.user)+'s' + 'preferences'

class Account(models.Model):
    name = models.CharField(max_length=266)
    opening_balance = models.CharField(max_length=266)
    account_number = models.CharField(max_length=266)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    description = models.CharField(max_length=266)
    bank_account = models.CharField(max_length=266,default='SOME STRING')

class IncomeGoal(models.Model):
    name = models.CharField(max_length=266)
    opening_balance = models.CharField(max_length=266)
    target = models.CharField(max_length=266)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField(default=now)

class Transfer(models.Model):
    account_from = models.CharField(max_length=266)
    account_to = models.CharField(max_length=266)
    date = models.DateField(default=now)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    note = models.CharField(max_length=266)
    amount = models.CharField(max_length=266,default='SOME Amount')

class SMS(models.Model):
    to =  models.CharField(max_length=266)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    msg =  models.CharField(max_length=266)
    date = models.DateField(default=now) 




    