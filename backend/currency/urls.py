from django.urls import path

from backend.currency import views

urlpatterns = [
    path('register/', views.RegisterUserAPIView.as_view(), name='register'),
    path('currencies/', views.CurrenciesAPIView.as_view(), name='currencies'),
    path('subcribe/', views.SubscribeToCurrencyAPIView.as_view(), name='subscribe-to-currency'),
    path('subscriptions/', views.SubcriptionsAPIView.as_view(), name='subscriptions'),
    path('rates-update/', views.CurrencyRatesUpdateAPIView.as_view(), name='rates-update')
]
