from django.db import models

class Data(models.Model):
    # порядковый номер
    serial_numb = models.CharField(max_length=3)

    # номер заказа
    order_numb = models.CharField(max_length=10)

    # стоимость в usd
    price_usd = models.CharField(max_length=10)

    # стоимость в rub
    price_rub = models.CharField(max_length=10)

    # дата поставки
    delivery_date = models.CharField(max_length=10,
                                     blank=True,
                                     null=True)

    def __str__(self):
        return f'{self.serial_numb, self.order_numb, self.price_usd, self.price_rub, self.delivery_date,}'


