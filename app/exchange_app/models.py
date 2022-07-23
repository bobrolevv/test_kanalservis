from django.db import models

class data(models.Model):
    # порядковый номер
    serial_numb = models.DecimalField(max_digits=5, decimal_places=1)

    # номер заказа
    order_numb = models.DecimalField(max_digits=10, decimal_places=1)

    # стоимость в usd
    price_usd = models.DecimalField(max_digits=10, decimal_places=1)

    # стоимость в usd
    price_rub = models.DecimalField(max_digits=10, decimal_places=1)

    # дата поставки
    delivery_date = models.DateField(auto_now=False)


