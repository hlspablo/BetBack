from graphene_django import DjangoObjectType
from core.models import Game

class GameType(DjangoObjectType):
    class Meta:
        model = Game