import graphene
from graphene import Field
from graphene.types import Boolean, Int
from .mutations.seller import SellerMutations



class CloseSellerCashierType(graphene.Mutation):
    success = Boolean() 

    def mutate(self, info, **kwargs):
        seller_mutations = SellerMutations(info.context, **kwargs)
        seller_mutations.close_seller_cashier()
        return CloseSellerCashierType(
            success = False
        )
    class Arguments:
        seller_id = Int()

