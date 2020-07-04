import graphene
from graphene.types import String, Int, List, Field, Boolean
from .types import (
    LocationStoreType,
    GameStoreType,
    MarketStoreType
)
from .resolvers.market import get_markets_store
from .resolvers.location import get_locations_store
from .resolvers.game import (
    get_today_games_store, 
    get_tomorrow_games_store, 
    get_after_tomorrow_games_store
)

class GeneralQuery(graphene.ObjectType):
    get_locations_store = List(LocationStoreType, name=String())
    get_today_games_store = List(GameStoreType, name=String())
    get_tomorrow_games_store = List(GameStoreType, name=String())
    get_after_tomorrow_games_store = List(GameStoreType, name=String())
    get_markets_store = List(MarketStoreType, name=String(), available=Boolean())

    def resolve_get_markets_store(self, info, **kwargs):
        return get_markets_store(info.context, **kwargs)

    def resolve_get_locations_store(self, info, **kwargs):
        return get_locations_store(info.context, **kwargs)
    
    def resolve_get_today_games_store(self, info, **kwargs):
        return get_today_games_store(info.context, **kwargs)

    def resolve_get_tomorrow_games_store(self, info, **kwargs):
        return get_tomorrow_games_store(info.context, **kwargs)

    def resolve_get_after_tomorrow_games_store(self, info, **kwargs):
        return get_after_tomorrow_games_store(info.context, **kwargs)
