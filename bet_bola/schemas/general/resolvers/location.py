from schemas.base import BaseResolver
from decimal import Decimal as dec
from core.models import Location, LocationModified
from django.db.models import Q, F


def get_locations_store(request, **kwargs):
    name = kwargs.get('name')
    locations = Location.objects.filter(Q(my_modifications__store=1) | Q(my_modifications__store__isnull=True) )\
        .order_by(F('my_modifications__priority').desc(nulls_last=True)).values('name','my_modifications__priority', 'my_modifications__available')
    if name:
        locations = locations.filter(name__icontains=name)
    return locations