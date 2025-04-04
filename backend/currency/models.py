from django.db import models


class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    notify_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User {self.telegram_id}'


class Currency(models.Model):
    base_currency_code = models.CharField(max_length=10)
    target_currency_code = models.CharField(max_length=10)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    last_updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('base_currency_code', 'target_currency_code')

    def __str__(self):
        return f'{self.base_currency_code} - {self.target_currency_code}'


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='subscriptions')

    class Meta:
        unique_together = ('user', 'currency')

    def __str__(self):
        return f'{self.user.telegram_id} -> {self.currency.base_currency_code}'
