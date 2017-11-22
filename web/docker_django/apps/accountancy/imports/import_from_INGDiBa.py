#!/usr/bin/python3
'''
Import bills from csv files exported form ING-DiBa
'''

# 
# TODO .:
#	don't reinsert data ..!
# 	timezone
# 

import os
import io
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

from argparse import ArgumentParser
from importlib import import_module
from datetime import datetime
from decimal import Decimal

import csv

from django.core.exceptions import ValidationError

# from .models import Account, Bill, Item
from docker_django.apps.accountancy.models import Account, Bill, Item, BalanceCheck

import logging
from docker_django.apps.accountancy import trace_logging
LOG = trace_logging.getTraceLogger("accountancy.imports.import_from_INGDiBa", trace_level=logging.INFO)

__all__ = ['import_from_INGDiBa']



DEFAULT_ACCOUNT = "ING-DiBa 5416711150"



def _ignore_file_header(csv_reader, empty_lines):
	for i in range(empty_lines):
		for line in csv_reader:
			if len(line) == 0:
				break

def _ignore_table_header(csv_reader):
	next(csv_reader)

def _string2number(s):
	return Decimal(s.replace('.', '').replace(',', '.'))

@LOG
def import_from_INGDiBa(input_file, account, dont_save=True):
	
	input_wrap = io.TextIOWrapper(input_file, newline='', encoding='latin_1')
	
	csv_reader = csv.reader(input_wrap, delimiter=';')
	
	_ignore_file_header(csv_reader, 2)
	
	_ignore_table_header(csv_reader)
	
	balance = None
	last_date = None
	last_balance = None
	for line in csv_reader:
		if len(line) == 0:
			LOG.debug("END")
			break
		
		LOG.debug("line, %s", line)
		data = {
			'date': datetime.strptime(line[0], '%d.%m.%Y'),
			'name': line[3],
			'comment': line[4],
			'counterparty': line[2],
			'unit_price': _string2number(line[5]),
			'balance': _string2number(line[7]),
		}
		
		if not last_date:
			last_date = data['date']
			last_balance = data['balance']
		
		# checking actual balance
		if not balance:
			balance = data['balance'] - data['unit_price']
		else:
			LOG.info("computed balance: %s", balance)
			LOG.info("written  balance: %s", data["balance"])
			LOG.info("price: %s", data["unit_price"])
			balance -= data["unit_price"]
		
		try:
			bill = Bill(account=account, date=data['date'], counterparty=data['counterparty'])
			bill.full_clean()
			if not dont_save:
				bill.save(force_insert=True)
			item = Item(bill=bill, name=data['name'], comment=data['comment'], unit_price=data["unit_price"])
			item.full_clean()
			if not dont_save:
				item.save(force_insert=True)
		except ValidationError as e:
			LOG.info("%r", data)
			LOG.info("%r", bill)
			LOG.info("%r, %s, %r", bill.account, bill.date, bill.counterparty)
			LOG.info("%r", item)
			LOG.info("%r, %r, %r, %r, %r, %r, %r", item.category, item.product, item.name, item.comment, item.amount, item.unit, item.unit_price)
			LOG.info("%s", e.message_dict)
		
	LOG.info("FINAL BALANCE: %s", last_balance)
	bc = BalanceCheck(account=account, date=last_date.replace(hour=1), real=last_balance)
	LOG.info("%r %s", bc, bc.real)
	if not dont_save:
		bc.save(force_insert=True)
	
	pass
	


if __name__ == "__main__":
	
	desc = import_module('__main__').__doc__.split("\n")[1]
	parser = ArgumentParser(description=desc)
	
	parser.add_argument("-a", "--account", default=DEFAULT_ACCOUNT, help="account to which the bills should be imported [default: %(default)s]")
	parser.add_argument("-s", "--save", action='store_true', help="when present, the bills will actually be saved. Default is a dry run.")
	parser.add_argument(dest="files", metavar="file", nargs='+', help="input file(s)")
	
	args = parser.parse_args()
	
	LOG.info("account=%r", args.account)
	LOG.info("do_save=%r", args.save)
	LOG.info("files=%r", args.files)
	
	account = Account.objects.get(name=args.account)
	
	for input_file in args.files:
		with open(input_file, 'b') as fd:
			import_from_INGDiBa(fd, account, not args.save)
	
	pass


