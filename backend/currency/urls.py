from django.urls import path

import currency.views as views

urlpatterns = [
    path('register/', views.RegisterUserAPIView.as_view(), name='register'),
    path('currencies/', views.CurrenciesAPIView.as_view(), name='currencies'),
    path('subscribe/', views.SubscribeToCurrencyAPIView.as_view(), name='subscribe'),
    path('subscriptions/', views.SubscriptionsAPIView.as_view(), name='subscriptions'),
    path('rates_update/', views.CurrencyRatesUpdateAPIView.as_view(), name='rates-update'),
    path('change_notification_time/', views.ChangeNotificationTimeAPIView.as_view(), name='change-notification-time'),
    path('delete_subscription/', views.DeleteSubscriptionAPIView.as_view(), name='delete-subscription')
]
