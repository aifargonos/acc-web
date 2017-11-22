from django import forms

from .models import Account
from .imports import AVAILABLE_IMPORT_METHODS



class ImportRequestForm(forms.Form):
    method = forms.ChoiceField(choices=[(k, AVAILABLE_IMPORT_METHODS[k].name) for k in AVAILABLE_IMPORT_METHODS])
    account = forms.ModelChoiceField(queryset=Account.objects.all())
    input_file = forms.FileField()


