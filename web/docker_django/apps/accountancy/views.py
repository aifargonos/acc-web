import io
import logging

from django.shortcuts import render
from django.http import HttpResponse

from .forms import ImportRequestForm
from .imports import AVAILABLE_IMPORT_METHODS



def index(request):
    return HttpResponse("Hello, world. You're at the accountancy index.")



def import_view(request):
    log = None
    if request.method == 'POST':
        form = ImportRequestForm(request.POST, request.FILES)
        if form.is_valid():
            method = AVAILABLE_IMPORT_METHODS[form.cleaned_data['method']]
            account = form.cleaned_data['account']
            input_file = form.cleaned_data['input_file']
            
            # TODO: this should be somehow controlled by the settings :-P
            logged = io.StringIO()
            handler = logging.StreamHandler(logged)
            handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-10s | %(indent)s%(message)s"))
            logger = logging.getLogger("accountancy.imports")
            logger.addHandler(handler)
            
            # TODO: the whole input_file should act as a file, input_file.file shouldn't need to be accessed.
            # Update Django to 1.11.7 !!! recent django.core.files.utils.FileProxyMixin has property readable
            try:
                method.func(input_file.file, account=account, dont_save=False)
            except:
                # Exceptions should be logged.
                pass
            
            logger.removeHandler(handler)
            log = logged.getvalue()
    else:
        form = ImportRequestForm()
    return render(request, "accountancy/import.html", {'form': form, 'log': log})


