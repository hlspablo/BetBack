import graphene
from graphene.types import String, Int, List, Field
from .types import (
    LocationStoreType
)
from .resolvers.location import get_locations_store

class GeneralQuery(graphene.ObjectType):
    get_store_locations = List(LocationStoreType, name=String())

    def resolve_get_store_locations(self, info, **kwargs):
        return get_locations_store(info, **kwargs)