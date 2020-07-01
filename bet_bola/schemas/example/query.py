import graphene
from graphene import Field
from graphene.types import String, Int
# from .types import (
#     SellerCashierType
# )


class TodoQuery(graphene.ObjectType):
    to = Field()

    def resolve_ (self, info, **kwargs):
        pass
