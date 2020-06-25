import graphene
from graphene import String, Field, List, Int, Date
from .types import SellerCashierType, SellersCashierType
from core.models import Game
from decimal import Decimal as dec
import datetime
from .resolvers.seller import CashierResolver

class CashierQuery(graphene.ObjectType):
    seller_cashier = Field(
        SellerCashierType, 
        seller_id=Int(required=True),
        start_date=String(),
        end_date=String()
    )
    sellers_cashier = Field(
        SellersCashierType,
        start_date=String(),
        end_date=String()
    )

    def resolve_seller_cashier(self, info, **kwargs):
        resolver = CashierResolver(info.context, **kwargs)
        return resolver.get_seller_cashier()

    def resolve_sellers_cashier(self, info, **kwargs):
        resolver = CashierResolver(info.context, **kwargs)
        return resolver.get_sellers_cashier()