import re
from datetime import date
from ipaddress import ip_address

from django.core.urlresolvers import reverse
from ipware.ip import get_real_ip
from ocflib.infra.net import is_ocf_ip
from ocflib.lab.hours import Day

from ocfweb.component.lab_status import get_lab_status
from ocfweb.environment import ocfweb_version


def get_base_css_classes(request):
    if request.resolver_match.url_name:
        page_class = 'page-' + request.resolver_match.url_name
        yield page_class

        for arg in request.resolver_match.args:
            page_class += '-' + re.sub(r'[^a-zA-Z_\-]', '-', arg)
            yield page_class


def ocf_template_processor(request):
    hours = Day.from_date(date.today())
    real_ip = get_real_ip(request)
    return {
        'lab_is_open': hours.is_open(),
        'current_lab_hours': hours,
        'lab_status': get_lab_status(),
        'base_css_classes': ' '.join(get_base_css_classes(request)),
        'is_ocf_ip': is_ocf_ip(ip_address(real_ip)) if real_ip else True,
        'join_staff_url': request.build_absolute_uri(reverse('about-staff')),
        'ocfweb_version': ocfweb_version(),
    }
