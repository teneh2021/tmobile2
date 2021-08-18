from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
import datetime

import math
from django.db.models import Avg, Sum, Max, Min
from numpy import mod, sum, min, max, average

# Create your models here.

class UserGender(models.Model):
    user=models.ForeignKey(User, related_name='gender', on_delete=models.CASCADE)
    user_gender=models.CharField(max_length=256)

    def __str__(self):

        return str(self.user.first_name)

    def gender(self):
        return str(self.user_gender)
class Trends(models.Model):
    topic =models.CharField(max_length=250, default = 'Learn more', null=True, blank=True)
    announcement = models.TextField(max_length=400)
    link = models.URLField(null=True, blank=True)
    date_added = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return str(self.topic)

    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=400, verbose_name='Comment or suggestions')

    def __str__(self):
        return str(self.user.first_name)

class Upload(models.Model):
    uploaded_by =models.ForeignKey(User, related_name='uploads', null=True, on_delete=models.CASCADE)
    screenshot = models.ImageField(upload_to='media/', null=True, verbose_name='Upload the screenshot of the payment you made (in T-Mobile app, zelle, or Cash App')
    total_paid = models.FloatField(max_length=50, default=0, null=True)
    comment =models.TextField(verbose_name='Remark or comment', max_length=400, null=True, blank=True )
    date_created = models.DateField(default=datetime.datetime.now(), verbose_name='Upload date')

    def __str__(self):
        return str(self.uploaded_by.first_name)
        


class Totals(models.Model):
    plan_total = models.FloatField(max_length=50, default=0)
    netflix = models.FloatField(max_length=50, default=0)
    num_line =models.PositiveIntegerField(verbose_name='Number of lines', default=1)
    total_bill =models.FloatField(max_length=50, null=True, default=0)
    note = models.TextField(max_length=400, default="""Please visit www.vangarmoh.com to upload screenshot of your payment confirmation page. username is: your phone number. Password is: the first two digits and last two digits of your phone number. Thank you."""
                            )
    bill_date = models.DateField(default=datetime.datetime.now())

    def __str__(self):

        return str('{} Bill: {}'.format(self.bill_date.strftime("%B"), self.total_bill))
    def plan_br(self):

        plan =self.plan_total / self.num_line
        return plan

    def netflix_br(self):
        netflix_1 =self.netflix /self.num_line
        return netflix_1

    @admin.display(boolean=False, ordering='netflix', description='Total paid')
    def add_up(self):
        self.datenow =datetime.datetime.now()
        if self.datenow.day>21:
            self.next_bill_date =datetime.datetime(self.datenow.year, self.datenow.month +1, 22)
            self.sum_total = Upload.objects.all().filter(date_created__gte=self.bill_date,
                                               date_created__lte=self.next_bill_date).aggregate(Sum('total_paid'))
        else:
            self.next_bill_date =datetime.datetime(self.datenow.year, self.datenow.month, 22)
            self.sum_total = Upload.objects.all().filter(date_created__gte=self.bill_date,
                                               date_created__lte=self.next_bill_date).aggregate(Sum('total_paid'))
        return self.sum_total['total_paid__sum']

    
class Equipment(models.Model):
    user = models.ForeignKey(
        User, related_name='equipments', on_delete=models.CASCADE)
    device_name = models.CharField(max_length=256, null=True)
    monthly = models.FloatField(max_length=50,  null=True, default=0)
    original_price = models.FloatField(max_length=50, null=True, default=0)
    down_pay = models.FloatField(max_length=50, null=True, default=0)
    duration = models.IntegerField(default=0, null=True)
    date_created = models.DateField(default=datetime.date(2021, 7, 23))

    def __str__(self):
        return str(self.user.first_name)

    def month_elapsed(self):
        days_diff = datetime.datetime.now().date() - self.date_created
        month = math.ceil(days_diff.days/30)
        return month

    def month_remained(self):
        month_remained = self.duration - self.month_elapsed()
        return month_remained

    def amount_remained(self):
        amount = self.original_price - self.down_pay - \
            (self.month_elapsed() * self.monthly)
        return amount

    def amount_paid(self):
        amount = self.monthly * self.month_elapsed() + self.down_pay
        return amount

class BreakDown(models.Model):
    user_name = models.ForeignKey(User, related_name='breaks', on_delete=models.CASCADE)
    equipment = models.FloatField(max_length=50, default=0, null=True)
    one_charge = models.FloatField(max_length=50, default=0, null=True)
    add_on = models.FloatField(max_length=50, default=0, null=True)
    mid_cycle = models.FloatField(max_length=50, default=0, null=True)
    admin_comment = models.TextField(max_length=1000, blank=True, null= True)

    @admin.display(boolean=False, ordering='mid_cycle', description='User')
    def __str__(self):
        return str(self.user_name.first_name)

    @admin.display(boolean=False, ordering='add_on', description='Plan')
    def plan_br(self):
        total = Totals.objects.order_by("netflix").latest('netflix')
        plan = total.plan_br()
        return round(plan, 2)

    @admin.display(boolean=False, ordering='one_charge', description='Netflix')
    def netflix_br(self):
        total = Totals.objects.order_by("netflix").latest('netflix')
        netflix_1 = total.netflix_br()
        return round(netflix_1, 2)
    

  







