from django.contrib import admin
from .models import *


# Register your models here.

#admin.site.register(Upload)
#admin.site.register(Equipment)
#admin.site.register(BreakDown)
#admin.site.register(Totals)
admin.site.register(UserGender)


class TrendsAdmin(admin.ModelAdmin):
    list_display =['topic',  'date_added']

admin.site.register(Trends, TrendsAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display =['__str__', 'message']

    def user_first_name(self, obj):
        return obj.__str__()

admin.site.register(Message, MessageAdmin)


class UploadAdmin(admin.ModelAdmin):
    list_display =['__str__', 'total_paid', 'screenshot', 'date_created']
    list_filter =['date_created', 'uploaded_by__first_name']
    def user_first_name(self, obj):
        return obj.__str__()

admin.site.register(Upload, UploadAdmin)


class TotalAdmin(admin.ModelAdmin):
    list_display =['__str__', 'plan_total', 'netflix', 'total_bill', 'add_up', 'bill_date']
    def user_first_name(self, obj):
        return obj.__str__(), obj.add_up()

admin.site.register(Totals, TotalAdmin)

class EquipmentAdmin(admin.ModelAdmin):
    fieldsets=[('Device name and owner', {'fields': ['user', 'device_name']}),
                ('Device detail', {'fields': ['original_price','down_pay', 'date_created','duration', 'monthly', 'amount_remained', 'month_remained', 
                'month_elapsed', 'amount_paid']}),
    ]
    readonly_fields=('amount_remained','month_remained', 'month_elapsed', 'amount_paid',)
    list_display = ['__str__', 'device_name', 'original_price', 'down_pay', 'date_created', 'duration', 'monthly', 'amount_remained',
                    'month_remained', 'month_elapsed', 'amount_paid',
                    ]
    def amount_remaineds(self, obj):
        return obj.amount_remained(), obj.month_remained(), obj.month_elapsed(), obj.amount_paid(), obj.__str__()

admin.site.register(Equipment, EquipmentAdmin)


class UploadInline(admin.StackedInline):
    model = Upload
    extra = 2


class BreakDownAdmin(admin.ModelAdmin):
    fieldsets=[('The user', {'fields':['user_name',]}),
                ('Plan charges', {'fields': ['plan_br', 'netflix_br']}),
                ('Equipment charges', {'fields':['equipment']}),
                ('Others charges', {'fields':['one_charge', 'add_on', 'mid_cycle', 'admin_comment',], }),

    ]
    list_display =['__str__', 'plan_br', 'netflix_br', 'equipment', 'one_charge', 'add_on', 'mid_cycle',]
    list_filter =['user_name__first_name']
    search_fields = [ 'equipment','add_on', 'user_name__first_name']
    readonly_fields =('plan_br', 'netflix_br', )

    def plan_charge(self, obj):
        return obj.plan_br(), obj.netflix_br(), obj.__str__()

admin.site.register(BreakDown, BreakDownAdmin)
        


#admin.site.register(User_manager)
