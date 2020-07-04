from graphene_django import DjangoObjectType
from graphene import ObjectType
from graphene.types import String, Decimal, Float, Int, DateTime, Field, List, Boolean

class LocationStoreType(ObjectType):
    name = String()
    my_modifications__priority = Int()
    my_modifications__available = Boolean()

class GameStoreType(ObjectType):
    id = String()
    name = String()
    start_date = DateTime()
    league__name = String()
    league__location__name = String()
    my_modifications__available = Boolean()
    my_modifications__is_in_zone = Boolean()


class MarketStoreType(ObjectType):
    name = String()
    my_modifications__reduction_percentual = Int()
    my_modifications__modification_available = Boolean()
    my_modifications__available = Boolean()


