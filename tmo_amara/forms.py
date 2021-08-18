

from django.db.models import fields
from django.http import request
from .models import Upload, Message
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



# Create your forms here.

from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


class BSModalModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    pass


class UploadForm(BSModalModelForm):
	#comment1 = forms.CharField(max_length=400,     widget=forms.Textarea( attrs={'placeholder': 'This field is optional. \nWhich other line did you paid for? \n Did you paid through T-Mobile, or zelle, Cash App'}))
	class Meta:
		model = Upload
		
		fields = ['total_paid', 'screenshot', 'date_created' , 'comment']


class MessageForm(BSModalModelForm):
	class Meta:
		model = Message
		fields = ['message']



		
	

