from graphene_django import DjangoObjectType
from core.models import Game
from graphene import ObjectType
from graphene.types import String, Decimal, Float, Int, DateTime, Field, List, Boolean

class D(ObjectType):
    pass
