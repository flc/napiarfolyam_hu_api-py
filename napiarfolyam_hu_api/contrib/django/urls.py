from django.urls import path

from . import views


urlpatterns = [
    path('', views.CurrencyConverterView.as_view(), name='currency_converter'),
]
