import datetime
import io
import logging

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import render

from .forms import BillQueryForm, ImportRequestForm
from .imports import AVAILABLE_IMPORT_METHODS
from .models import Bill



def index(request):
    return HttpResponse("Hello, world. You're at the accountancy index.")



@login_required
@permission_required('accountancy.add_bill')
@permission_required('accountancy.add_item')
def import_view(request):
    log = None
    if request.method == 'POST':
        form = ImportRequestForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            method = AVAILABLE_IMPORT_METHODS[form.cleaned_data['method']]
            # TODO: check that the user owns the account !!!
            account = form.cleaned_data['account']
            input_file = form.cleaned_data['input_file']
            
            # TODO: this should be somehow controlled by the settings :-P
            logged = io.StringIO()
            handler = logging.StreamHandler(logged)
            handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-10s | %(indent)s%(message)s"))
            logger = logging.getLogger("accountancy.imports")
            logger.addHandler(handler)
            
            try:
                method.func(input_file, account=account, dont_save=False)
            except:
                # Exceptions should be logged.
                pass
            
            logger.removeHandler(handler)
            log = logged.getvalue()
    else:
        form = ImportRequestForm(request.user)
    return render(request, "accountancy/import.html", {'form': form, 'log': log})



@login_required
def bills_view(request):
    bills = Bill.objects.none()
    if request.method == 'POST':
        query_form = BillQueryForm(request.user, request.POST, request.FILES)
        if query_form.is_valid():
            date_from = query_form.cleaned_data['date_from']
            date_to = query_form.cleaned_data['date_to']
            # TODO: check that the user owns all the account !!!
            accounts = query_form.cleaned_data['accounts']
            
            bills = Bill.objects.filter(
                    date__gt=date_from,
                    date__lte=date_to,
                    account__in=accounts,
                )
    else:
        date_to = datetime.datetime.now()
        if date_to.month <= 1:
            date_from = date_to.replace(year=date_to.year-1, month=12)
        else:
            date_from = date_to.replace(month=date_to.month-1)
        query_form = BillQueryForm(request.user, initial={'date_from': date_from, 'date_to': date_to})
    return render(request, "accountancy/bills.html", {'query_form': query_form, 'bills': bills})


