from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from tmo_amara.forms import UploadForm, MessageForm
from tmo_amara.models import Equipment, Totals, Trends, Upload, UserGender, BreakDown
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from bootstrap_modal_forms.generic import BSModalFormView, BSModalCreateView
from django.contrib.auth.models import User 
from django.utils import timezone
from django.urls import reverse_lazy
import datetime
from datetime import timedelta
import smtplib
from email.message import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your views here.

def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = 'tenehsheriff@gmail.com'
    msg['from'] = user
    password = 'ikzwywldplguhtad'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    #server.connect('smtp.gmail.com', 587)

    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()


class ReusableFuncs():
	def __init__(self):
		self.date_now =datetime.datetime.now()
		self.note = ''
		
	def deadline(self):
		self.date_now = datetime.datetime.now()
		if self.date_now.day < 22:
			p = self.date_now
		else:

			p = self.date_now + timedelta(days=28)
		return p.strftime("%B")

	def billdate1(self):
		datenow = datetime.datetime.now()
		if datenow.day > 21:
			self.billdate = datetime.datetime(datenow.year, datenow.month, 22)
		else:
			self.billdate = datetime.datetime(datenow.year, datenow.month - 1, 22)
		return self.billdate.date()
	
	def pay_hist(self, user):
		list_paid = []
		list_screenshot = []
		list_date = []
		user1 = Upload.objects.filter(uploaded_by=user)
		for ee in user1:
			list_paid.append(ee.total_paid)
			list_screenshot.append(ee.screenshot)
			list_date.append(ee.date_created)
		return list_date[-10:], list_paid[-10:], list_screenshot[-10:]

	def plans(self):
		plan =0
		humanized_time =0
		for entry in Totals.objects.all():
			plan =entry.plan_br()
			humanized_time = entry.bill_date
		return round(plan, 2), humanized_time
	def neflixs(self):
		netflix =0
		for entry in Totals.objects.all():
			netflix =entry.netflix_br()
		return round(netflix, 2)

	def pay_confirmed(self, user):
		screenshot =''
		if Upload.objects.filter(uploaded_by =user):
			for up in Upload.objects.filter(uploaded_by=user):
				upload_date = up.date_created
				screenshot = up.screenshot
				
				days_diff = abs(self.billdate1() - upload_date)
				if days_diff.days<=30:
					current_upload =upload_date		
		else:
			current_upload =datetime.datetime(1999, 6, 1).date()
		flag = False
		if current_upload >= self.billdate1():
			flag = True
		return flag, screenshot
	
	def sum_total(self, user):
		one_charge = 0
		add_on = 0
		mid_cycle = 0
		self.equipment2 = 0
		self.total =0
		if Equipment.objects.filter(user=user):
			for equip in Equipment.objects.filter(user=user):
				self.equipment2 =equip.monthly
			
		if BreakDown.objects.filter(user_name=user):
			for latest_bill in BreakDown.objects.filter(user_name=user):
				latest_bill.equipment =self.equipment2
				
				
				one_charge = latest_bill.one_charge
				add_on = latest_bill.add_on
				mid_cycle = latest_bill.mid_cycle
		else:
			latest_bill =0
		plan, _ = self.plans()
		self.total = plan + self.neflixs() + self.equipment2 + one_charge + add_on + mid_cycle
		return round(self.total, 2), latest_bill
		
	def sms(self):
		for entry in Totals.objects.all():
			self.note = entry.note
		for entery in User.objects.all():
			user = entery.username
			first_name = entery.first_name
		
			

			total, _ = self.sum_total(entery)
		
			message_body = f"Your bill for this month is {total} due before {self.billdate1().strftime('%B')} 5. {self.note}"
			email_alert(f'{first_name}', message_body, f'{user}@tmomail.net')

all_func = ReusableFuncs()



@receiver(post_save, sender=Totals)
def smsdispatch(sender, instance, created, *args, **kwargs):
	if created:
		all_func.sms()



@login_required
def user_home(request):
	"""Paginator here"""
	user_list = Trends.objects.order_by("-date_added")
	page = request.GET.get('page', 1)

	paginator = Paginator(user_list, 1)
	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator.page(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)

	"""Payment confirmation and screenshot"""
	listed =list(all_func.pay_confirmed(request.user))
	flag, photo =all_func.pay_confirmed(request.user)

	""" total monthly bill and break down"""
	total, latest_bill=all_func.sum_total(request.user)
	
	"""Gives equipment break down"""
	if Equipment.objects.filter(user=request.user):
		equipment=request.user.equipments.latest('user')
	else:
		equipment =0

	"""Gender"""
	gender =UserGender.objects.filter(user=request.user)

	

	context ={'deadline':all_func, 'listed':listed,	'flag':flag, 'gender':gender, 'dday':latest_bill, 
	 'total':round(total, 2), 'equipment':equipment, 'photo':photo, 'users':users}
	return render(request, 'index.html', context)


def user_login(request):
	
	if request.user.is_authenticated:
		return redirect('index')

	if request.method == "POST":

		USER = request.POST.get('username')
		PASSWORD = request.POST.get('password')

		user = authenticate(request, username=USER, password = PASSWORD)
		if user is not None:
			#request.session.set_expiry(3)

			login(request, user)
			
			#return render(request=request, template_name='index.html')
			return redirect('user_home')
		else:
			messages.info(request, 'Username OR Password is incorrect')
		
	return render(request=request, template_name='login.html')


@login_required
def user_logout(request):
	logout(request)
	return redirect('/login')
"""
@login_required
def user_logout(request):
	if request.SESSION_COOKIE_AGE==18:

		try:
			del request.session['member_id']
		except KeyError:
			pass
	return HttpResponse("You're logged out.")
"""  
class Uploadw(BSModalCreateView):
	template_name = 'upload.html'
	form_class = UploadForm
	success_url = reverse_lazy('user_home')

	def form_valid(self, form):
		if not self.request.is_ajax():
			obj = form.save(commit=False)
			obj.uploaded_by = self.request.user
			obj.save()
		return redirect(self.success_url)


class Messagew(BSModalCreateView):
	template_name = 'message.html'
	form_class = MessageForm
	success_url = reverse_lazy('user_home')

	def form_valid(self, form):
		if not self.request.is_ajax():
			msg = form.save(commit=False)
			msgs = form.cleaned_data.get('message')
			
			msg.user = self.request.user
			email_alert(f'Message from {msg.user.first_name}',msgs, 'svangarmoh@gmail.com')
			msg.save()
		return redirect(self.success_url)

def make_payment(request):
	total, _  =all_func.sum_total(request.user)
	
	my_dict = {'total1':total}
	return render(request, 'make_payment.html', context=my_dict)



def payment_history(request):
	# dates, paid, screenshot, equipment =all_func.pay_hist(request.user)
	users = Upload.objects.filter(uploaded_by=request.user).order_by("-date_created")
	my_dict = { 'users':users}
	
	return render(request, 'payment_history.html', context=my_dict)


def ussd_code(request):
    my_dict = {'insert_me': "Hello I amm from views.py!"}
    return render(request, 'ussd_code.html', context=my_dict)


def welcome(request):
    my_dict = {'insert_me': "Hello I amm from views.py!"}
    return render(request, 'welcome.html', context=my_dict)


def game(request):
	gamer =" AlienInvasion()"
	my_dict = {'insert_me': gamer}
	return render(request, 'index.html', context=my_dict)

