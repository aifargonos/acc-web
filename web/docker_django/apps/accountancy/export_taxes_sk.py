#!/usr/bin/python3

import os
import sys

# as a standalone script
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "docker_django.settings")
sys.path.append('/usr/src/app')
# 
# The following two lines only initialize the apps,
# so that the translations can be initialized.
# Translations are used when printing the errors.
# TODO: Use this only from the server and this shouldn't be a problem.
# 
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import datetime

# from .models import Account, Bill, Item
from docker_django.apps.accountancy.models import Item



def _get_query():
	return Item.objects.filter(
			category__name = u'garsónka Žilina',
			bill__date__range = (datetime.date(2016, 1, 1), datetime.date(2017, 1, 1))
		).order_by('bill__date')

def _get_header():
	return 'date,counterparty,name,comment,income,expense'

def _format_item(item):
	price = item.price()
	income = ""
	expence = ""
	if price < 0:
		expence = "%.2f" % price
	else:
		income = "%.2f" % price
	return '"%s","%s","%s","%s", %s, %s' % (
			item.bill.date.strftime("%Y-%m-%d"),
			item.bill.counterparty,
			item.name,
			item.comment,
			income,
			expence
		)



def main():
	
	query = _get_query()
	
	print(_get_header())
	
	for item in query:
		print(_format_item(item))
	
	pass



if __name__ == '__main__':
	
	main()


