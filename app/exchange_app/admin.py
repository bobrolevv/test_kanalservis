from django.contrib import admin

from .models import Data


class DataAdmin(admin.ModelAdmin):
    list_display = ("serial_numb", "order_numb",
                    "price_usd", "price_rub", "delivery_date")
    search_fields = ("order_numb",)
    list_filter = ("order_numb", "price_usd", "delivery_date")
    empty_value_display = "-пусто-"


admin.site.register(Data, DataAdmin)
