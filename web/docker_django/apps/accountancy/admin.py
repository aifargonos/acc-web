
from . import models
from django.contrib import admin



admin.site.register(models.Currency)

admin.site.register(models.Category)

admin.site.register(models.Unit)



admin.site.register(models.Account)



# TODO ???
admin.site.register(models.Product)



class ItemInline(admin.TabularInline):# TODO try .: StackedInline
    model = models.Item
    fk_name = 'bill'
    extra = 3
    list_display = ("category", "product", "name", "comment", "amount", "unit", "unit_price")



class BillAdmin(admin.ModelAdmin):
#    list_display = ("date", "time", "account", "counterparty", "total", "currency")
    list_display = ("date", "account", "counterparty", "total", "currency")
#    list_display_links = ("date", "time", "account")
    list_display_links = ("date", "account")
#    list_editable = ["counterparty"]
#    list_filter = ['account', 'date', 'counterparty']
    list_filter = ['account', 'date']
    date_hierarchy = 'date'
#    fields = ("account", "counterparty", "date", "time")
    fields = ("account", "counterparty", "date")
    inlines = [ItemInline]
    save_on_top = True

admin.site.register(models.Bill, BillAdmin)



class BalanceCheckAdmin(admin.ModelAdmin):
#    list_display = ("date", "time", "real", "theoretical", "error", "currency")
    list_display = ("date", "account", "real", "theoretical", "error", "currency")
#    list_display = ("date", "real", "theoretical")
#    list_display_links = ("date", "time")
    list_display_links = ("date", "account")
    list_per_page = 20
    list_filter = ['account', 'date']
    date_hierarchy = 'date'

admin.site.register(models.BalanceCheck, BalanceCheckAdmin)


