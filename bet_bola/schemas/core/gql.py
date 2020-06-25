import graphene
from graphene import String, Field, List
from .types import GameType
from core.models import Game

class CoreQuery(graphene.ObjectType):
    game = Field(GameType, name=String(required=True))
    all_games = List(GameType, name=String(required=True))

    def resolve_game(self, info, **kwargs):
        return Game.objects.filter(name__icontains=kwargs.get('name')).first()

    def resolve_all_games(self, info, **kwargs):
        return Game.objects.filter(name__icontains=kwargs.get('name'))
