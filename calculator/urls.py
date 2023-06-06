from django.urls import path

from .views import IPCalculatorTemplateView, calculate_ip

app_name = 'calculator'
urlpatterns = [
    path('', IPCalculatorTemplateView.as_view(), name="ip_calculator"),
    path('calculator/', calculate_ip, name='calculate_ip'),
]