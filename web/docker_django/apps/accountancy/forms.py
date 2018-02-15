from django import forms

from .models import Account
from .imports import AVAILABLE_IMPORT_METHODS



class ImportRequestForm(forms.Form):
    method = forms.ChoiceField(choices=[(k, AVAILABLE_IMPORT_METHODS[k].name) for k in AVAILABLE_IMPORT_METHODS])
    account = forms.ModelChoiceField(queryset=None)
    input_file = forms.FileField()
    
    def __init__(self, owner, *args, **kwargs):
        super(ImportRequestForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(owner=owner)



class BillQueryForm(forms.Form):
    date_from = forms.DateField()
    date_to = forms.DateField()
    accounts = forms.ModelMultipleChoiceField(queryset=None)
    
    def __init__(self, owner, *args, **kwargs):
        super(BillQueryForm, self).__init__(*args, **kwargs)
        self.fields['accounts'].queryset = Account.objects.filter(owner=owner)
    
    def clean(self):
        super(BillQueryForm, self).clean()
        date_from = self.cleaned_data.get('date_from')
        date_to = self.cleaned_data.get('date_to')
        if date_to and date_from:
            if date_to < date_from:
                # TODO: i18n !!!
                raise forms.ValidationError('The first date cannot be after the second date.')
        pass


