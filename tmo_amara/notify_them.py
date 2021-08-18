import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tmobile.settings')
import django
django.setup()
from tmo_amara.models import Upload
from django.contrib.auth.models import User
from datetime import datetime
from tmo_amara.views import email_alert, ReusableFuncs

all_func =ReusableFuncs()
class CronClass():
    def not_yet_paid(self):
        upload_date = 0
        datenow = datetime.now()
        for entry in User.objects.all():
            users = entry.username
            for upload in Upload.objects.filter(uploaded_by=entry):
                upload_date = upload.date_created
                if all_func.billdate1() > upload_date and datenow > datetime(datenow.year, datenow.month, 1):
                    total, _ = all_func.sum_total(entry)
                    message_body = f"Your bill is due {datenow.strftime('%B')} 5 ( in two days time ) and the total amount {total} has not being paid"
                    email_alert('Tmobile Bill payment notification',
                                        message_body, f'{users}@tmomail.net')

cron =CronClass()
cron.not_yet_paid()



