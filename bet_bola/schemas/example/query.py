import graphene
from graphene import Field
from graphene.types import String, Int
# from .types import (
#     SellerCashierType
# )
#from .resolvers.seller import SellerCashierResolver

class TodoQuery(graphene.ObjectType):
    # seller_cashier = Field(
    #     SellerCashierType, seller_id=Int(required=True), start_date=String(), end_date=String()
    # )

    # def resolve_seller_cashier(self, info, **kwargs):
    #     resolver = SellerCashierResolver(info.context, **kwargs)
    #     return resolver.get_seller_cashier()
