
import decimal

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _



class Currency(models.Model):
    
    class Meta:
        verbose_name = _("currency")
        verbose_name_plural = _("currencies")
        ordering = ["code"]
    
    code = models.CharField(_("code"), max_length=3, unique=True)
    
    def __str__(self):
        return self.code



class Category(models.Model):
    
    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ["name"]
    
    name = models.CharField(_("name"), max_length=64, unique=True)
    
    def __str__(self):
        return self.name



class Unit(models.Model):
    
    class Meta:
        verbose_name = _("unit")
        verbose_name_plural = _("units")
        ordering = ["abbr"]
    
    abbr = models.CharField(_("abbreviation"), max_length=16, unique=True)
    
    def __str__(self):
        return self.abbr



class Account(models.Model):
    
    class Meta:
        verbose_name = _("account")
        verbose_name_plural = _("accounts")
        ordering = ["name"]
    
    owner = models.ForeignKey(User, to_field="username", verbose_name=_("owner"))
    name = models.CharField(_("name"), max_length=64, unique=True)
    currency = models.ForeignKey(Currency, verbose_name=_("currency"))
    
    def __str__(self):
        return self.name



class Product(models.Model):
    
    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")
        ordering = ["name"]
    
    clazz = models.CharField(_("class"), max_length=64)
    brand = models.CharField(_("brand"), max_length=64, blank=True, null=True)
    name = models.CharField(_("name"), max_length=64)
    comment = models.CharField(_("comment"), max_length=128, blank=True, null=True)
    size = models.DecimalField(_("size"), max_digits=12, decimal_places=3, blank=True, null=True)
    unit = models.ForeignKey(Unit, verbose_name=_("unit"), blank=True, null=True)
    # TODO anything else ??
    
    def __str__(self):
        if self.brand:
            return u'%s by %s' % (self.name, self.brand)# TODO ..: texts !!!
        else:
            return self.name



class Bill(models.Model):
    
    class Meta:
        verbose_name = _("bill")
        verbose_name_plural = _("bills")
        ordering = ["-date"]
    
    account = models.ForeignKey(Account, verbose_name=_("account"))
    date = models.DateTimeField(_("date"), default=timezone.now)
    counterparty = models.CharField(_("counterparty"), max_length=64, blank=True, null=True)
    
    def total(self):
        return sum([i.price() for i in self.item_set.all()])# TODO .: aren't there aggragations ??
    
    def currency(self):
        return self.account.currency.code
    
    def __str__(self):
        if self.counterparty:
            return "%s %s" % (self.date, self.counterparty)
        else:
            return "%s" % self.date



class Item(models.Model):
    
    class Meta:
        verbose_name = _("item")
        verbose_name_plural = _("items")
    
    bill = models.ForeignKey(Bill, verbose_name=_("bill"))
    category = models.ForeignKey(Category, verbose_name=_("category"), blank=True, null=True)
    product = models.ForeignKey(Product, verbose_name=_("product"), blank=True, null=True)
    name = models.CharField(_("name"), max_length=64)
    comment = models.CharField(_("comment"), max_length=128, blank=True, null=True)
    amount = models.DecimalField(_("amount"), max_digits=12, decimal_places=3, default=1)
    unit = models.ForeignKey(Unit, verbose_name=_("unit"), blank=True, null=True)
    unit_price = models.DecimalField(_("unit price"), max_digits=12, decimal_places=3)
    
    def price(self):
#        oldprec = decimal.getcontext().prec
#        decimal.getcontext().prec = 3
        ret = self.amount * self.unit_price
#        decimal.getcontext().prec = oldprec
#        ret.quantize(decimal.Decimal('1.000'))
#        ret.normalize()
        return ret
    
    def __str__(self):
        return self.name



class BalanceCheck(models.Model):
    
    class Meta:
        ordering = ["-date"]
    
    account = models.ForeignKey(Account, verbose_name=_("account"))
    date = models.DateTimeField(_("date"), default=timezone.now)
    real = models.DecimalField(_("real balance"), max_digits=12, decimal_places=3)
    
    # TODO ..: tu je nejaky bug ... okolo polnoci ... 
    # ... lebo ked si pisem ucty do mobilu, nepisem tam cas ..
    # .. takze je to akoze o polnoci .. a ked urobim ucty po BC, tak su zapisane pred BC
    # riesenie .: pri importe z mobilu davat aktualny/zmysluplny cas
    def theoretical(self):
        prev = BalanceCheck.objects.filter(account = self.account, date__lt = self.date).latest('date')
        bills = Bill.objects.filter(account = self.account, date__gt = prev.date).filter(date__lt = self.date)
        return prev.real + sum([b.total() for b in bills])
    
    def error(self):
        return self.real - self.theoretical()
    
    def currency(self):
        return self.account.currency.code
    
    def __str__(self):
        return "%s %s" % (self.account, self.date)

