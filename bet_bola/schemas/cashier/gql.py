import graphene
from graphene import String, Field, List, Int, Date
from .types import SellerCashierType, SellersCashierType, ManagerCashierType, ManagerOwnerCashierType
from core.models import Game
from decimal import Decimal as dec
import datetime
from .resolvers.seller import SellerResolver
from .resolvers.manager import ManagerResolver


class CashierQuery(graphene.ObjectType):
    seller_cashier = Field(
        SellerCashierType, 
        seller_id=Int(required=True),
        start_date=String(),
        end_date=String()
    )
    manager_cashier = Field(
        ManagerCashierType, 
        manager_id=Int(required=True),
        start_date=String(),
        end_date=String()
    )
    manager_owner_cashier = Field(
        ManagerOwnerCashierType, 
        manager_id=Int(required=True),
        start_date=String(),
        end_date=String()
    )
    sellers_cashier = Field(
        SellersCashierType,
        start_date=String(),
        end_date=String()
    )

    def resolve_seller_cashier(self, info, **kwargs):
        resolver = SellerResolver(info.context, **kwargs)
        return resolver.get_seller_cashier()

    def resolve_manager_cashier(self, info, **kwargs):
        resolver = ManagerResolver(info.context, **kwargs)
        return resolver.get_manager_cashier()

    def resolve_manager_owner_cashier(self, info, **kwargs):
        resolver = ManagerResolver(info.context, **kwargs)
        return resolver.get_manager_owner_cashier()

    def resolve_sellers_cashier(self, info, **kwargs):
        resolver = SellerResolver(info.context, **kwargs)
        return resolver.get_sellers_cashier()