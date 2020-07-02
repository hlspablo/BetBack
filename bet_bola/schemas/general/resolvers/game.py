from schemas.base import BaseResolver
from decimal import Decimal as dec
from core.models import Game, GameModified
from django.db.models import Q, F, Count
from utils import timezone as tzlocal
import datetime

def get_today_games_store(request, **kwargs):
    name = kwargs.get('name')
    
    today_games = Game.objects.filter(start_date__gt=tzlocal.now(),
            start_date__lt=(tzlocal.now().date() + datetime.timedelta(days=1)),
            status__in=[0])\
            .annotate(cotations_count=Count('cotations', filter=Q(cotations__market__name='1X2')))\
            .filter(cotations_count__gte=3)

    today_games = today_games.filter(Q(my_modifications__store=1) | Q(my_modifications__store__isnull=True) )\
        .order_by(F('my_modifications__is_in_zone').desc(nulls_last=True)).values()\
        .values('id','name','start_date','league__name','league__location__name','my_modifications__is_in_zone', 'my_modifications__available')

    if name:
        today_games = today_games.filter(name__icontains=name)
    return today_games

def get_tomorrow_games_store(request, **kwargs):
    name = kwargs.get('name')
    
    tomorrow_games = Game.objects.filter(start_date__date=tzlocal.now().date() + datetime.timedelta(days=1),
            status__in=[0]).annotate(cotations_count=Count('cotations', filter=Q(cotations__market__name='1X2')))\
            .filter(cotations_count__gte=3)

    tomorrow_games = tomorrow_games.filter(Q(my_modifications__store=1) | Q(my_modifications__store__isnull=True) )\
        .order_by(F('my_modifications__is_in_zone').desc(nulls_last=True)).values()\
        .values('id','name','start_date','league__name','league__location__name','my_modifications__is_in_zone', 'my_modifications__available')

    if name:
        tomorrow_games = tomorrow_games.filter(name__icontains=name)
    return tomorrow_games


def get_after_tomorrow_games_store(request, **kwargs):
    name = kwargs.get('name')
    
    after_games = Game.objects.filter(start_date__date=tzlocal.now().date() + datetime.timedelta(days=2),
            status__in=[0]).annotate(cotations_count=Count('cotations', filter=Q(cotations__market__name='1X2')))\
            .filter(cotations_count__gte=3)

    after_games = after_games.filter(Q(my_modifications__store=1) | Q(my_modifications__store__isnull=True) )\
        .order_by(F('my_modifications__is_in_zone').desc(nulls_last=True)).values()\
        .values('id','name','start_date','league__name','league__location__name','my_modifications__is_in_zone', 'my_modifications__available')

    if name:
        after_games = after_games.filter(name__icontains=name)
    return after_games