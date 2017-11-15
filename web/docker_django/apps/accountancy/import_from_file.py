#!/usr/bin/python3
'''
Import bills from text files with rows of the form: "31.12.2011.23:59who/what3*-1.5"
'''

import os
import sys

# as a standalone script
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "docker_django.settings")
sys.path.append('/usr/src/app')

import re
from argparse import ArgumentParser
from importlib import import_module
from decimal import Decimal
from datetime import datetime
from collections import defaultdict

# from .models import Account, Bill, Item
from docker_django.apps.accountancy.models import Account, Bill, Item

import logging
from docker_django.apps.accountancy import trace_logging
LOG = trace_logging.getTraceLogger("accountancy.imports.import_from_file", trace_level=logging.INFO)

__all__ = ['import_from_file']



DEFAULT_ACCOUNT = 'pocket EUR'# TODO: Maybe put this somewhere global
DEFAULT_ITEM_COMMENT = 'import_from_file'
DEFAULT_ENCODING = 'utf-8'

RE_DATE_FIELD = re.compile(r"(\d+)\.")
RE_HOUR_FIELD = re.compile(r"(\d\d):")
RE_MINUTE_FIELD = re.compile(r"(\d\d)")
RE_CPARTY = re.compile(r"([^/]*)/")
RE_STUFF = re.compile(r"([^-\d]+)")
RE_AMOUNT = re.compile(r"(\d+\.?\d*)\*")



class _Data():
	'''
Data from a parsed line.
'''
	def __repr__(self):
		strings = defaultdict(lambda: None, self.__dict__)
		strings['class'] = self.__class__.__name__
		return '%(class)s(day=%(day)r, month=%(month)r, year=%(year)r, hour=%(hour)r, minute=%(minute)r, cparty=%(cparty)r, stuff=%(stuff)r, amount=%(amount)r, price=%(price)r)'\
				% strings
	
	pass



@LOG
def _parse_line(string, data):
	
	string = string.strip()
	
	pos = 0
	
	# day
	mo = RE_DATE_FIELD.match(string[pos:])
	LOG.info("day: %r -> %r" % (string[pos:], mo))
	if mo:
		data.day = int(mo.group(1))
		pos += mo.end()
	
	# month
	mo = RE_DATE_FIELD.match(string[pos:])
	LOG.info("month: %r -> %r" % (string[pos:], mo))
	if mo:
		data.month = int(mo.group(1))
		pos += mo.end()
	
	# year
	mo = RE_DATE_FIELD.match(string[pos:])
	LOG.info("year: %r -> %r" % (string[pos:], mo))
	if mo:
		data.year = int(mo.group(1))
		pos += mo.end()
	
	# hour
	data.hour = 0
	mo = RE_HOUR_FIELD.match(string[pos:])
	LOG.info("hour: %r -> %r" % (string[pos:], mo))
	if mo:
		data.hour = int(mo.group(1))
		pos += mo.end()
	
	# minute
	data.minute = 0
	mo = RE_MINUTE_FIELD.match(string[pos:])
	LOG.info("minute: %r -> %r" % (string[pos:], mo))
	if mo:
		data.minute = int(mo.group(1))
		pos += mo.end()
	
	# cparty
	mo = RE_CPARTY.match(string[pos:])
	LOG.info("cparty: %r -> %r" % (string[pos:], mo))
	if mo:
		cparty = mo.group(1)
		if cparty:
			data.cparty = cparty
		else:
			data.cparty = None
		pos += mo.end()
	
	# stuff
	mo = RE_STUFF.match(string[pos:])
	LOG.info("stuff: %r -> %r" % (string[pos:], mo))
	if mo:
		data.stuff = mo.group(1)
		pos += mo.end()
	
	# amount
	data.amount = Decimal('1')
	mo = RE_AMOUNT.match(string[pos:])
	LOG.info("amount: %r -> %r" % (string[pos:], mo))
	if mo:
		data.amount = mo.group(1)
		pos += mo.end()
	
	# price
	try:
		data.price = Decimal(string[pos:])
		LOG.info("price: %r -> %r" % (string[pos:], data.price))
	except:
		LOG.info("price: %r -> %r" % (string[pos:], None))
	
	return data

@LOG
def import_from_file(input_file, account_name=DEFAULT_ACCOUNT):
	
	account = Account.objects.get(name=account_name)
	
	with open(input_file, encoding=DEFAULT_ENCODING) as fd:
		
		time = datetime.now()
		
		data = _Data()
		data.cparty = None
		data.day = time.day
		data.month = time.month
		data.year = time.year
		
		# Skip header
		next(fd)
		
		bill = None
		
		for line in fd:
			
			data = _parse_line(line, data)
			
			time = time.replace(year=data.year, month=data.month, day=data.day, hour=data.hour, minute=data.minute)
			
			# create bill if needed
			if (
					bill is None or
					not data.cparty or
					bill.date != time or
					bill.counterparty != data.cparty
				):
				bill = Bill.objects.create(account=account, date=time, counterparty=data.cparty)
				LOG.info('%r %s %s %s' % (bill, bill.account, bill.date, bill.counterparty))
			
			# create item
			item = Item.objects.create(bill=bill, name=data.stuff, comment=DEFAULT_ITEM_COMMENT, amount=data.amount, unit_price=data.price)
			LOG.info('%r %s %s %s %s %s %s %s' % (item, item.category, item.product, item.name, item.comment, item.amount, item.unit, item.unit_price))
		
		pass
	
	pass



if __name__ == "__main__":
	
	desc = import_module('__main__').__doc__.split("\n")[1]
	parser = ArgumentParser(description=desc)
	
	parser.add_argument("-a", "--account", default=DEFAULT_ACCOUNT, help="account to which the bills should be imported [default: %(default)s]")
	parser.add_argument(dest="files", metavar="file", nargs='+', help="input file(s)")
	
	args = parser.parse_args()
	
	import django
	django.setup()
	
	LOG.info("account=%r" % args.account)
	LOG.info("files=%r" % (args.files, ))
	
	for input_file in args.files:
		import_from_file(input_file, args.account)
	
