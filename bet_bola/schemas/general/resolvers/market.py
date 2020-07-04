from schemas.base import BaseResolver
from decimal import Decimal as dec
from core.models import Market
from utils.models import MarketModified
from django.db.models import Q, F


def get_markets_store(request, **kwargs):
    name = kwargs.get('name')
    available = kwargs.get('available')

    markets = Market.objects.filter(Q(my_modifications__store=1) | Q(my_modifications__store__isnull=True) )\
        .order_by(F('name').desc(nulls_last=True)).values('name',
        'my_modifications__reduction_percentual', 'my_modifications__available','my_modifications__modification_available')
    if name:
        markets = markets.filter(name__icontains=name)
    if not available == None:
        markets = markets.filter(my_modifications__modification_available=available)
    return markets