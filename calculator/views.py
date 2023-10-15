from django.shortcuts import render
from django.views.generic import TemplateView

from .ipv4 import get_netinfo
from .ipv6 import get_ipv6_netinfo


class IPCalculatorTemplateView(TemplateView):
    template_name = 'calculator/ip_calculator.html'


def calculate_ip(request):
    ip_with_mask = request.GET['ip_with_mask']
    try:
        netinfo = get_netinfo(ip_with_mask)
    except:
        netinfo = get_ipv6_netinfo(ip_with_mask)
    return render(request,
                  'calculator/ip_calculator.html',
                  {'netinfo': netinfo})
