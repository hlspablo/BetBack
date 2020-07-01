from graphene_django import DjangoObjectType
from graphene import ObjectType
from graphene.types import String, Decimal, Float, Int, DateTime, Field, List, Boolean

class LocationStoreType(ObjectType):
    name = String()
    my_modifications__priority = Int()
    my_modifications__available = Boolean()

