import graphene
from graphene import Field
from graphene.types import Boolean, Int, String
from .mutations.seller import SellerMutations
from .mutations.manager import ManagerMutations

class CloseManagerCashierType(graphene.Mutation):
    success = Boolean() 

    class Arguments:
        close_all = Boolean()
        manager_id = Int()

    def mutate(self, info, **kwargs):
        manager_mutations = ManagerMutations(info.context, **kwargs)
        return_value = manager_mutations.close_manager_cashier()
        return CloseManagerCashierType(
            success = return_value
        )

class CloseSellerCashierType(graphene.Mutation):
    success = Boolean() 

    class Arguments:
        close_all = Boolean()
        seller_id = Int()

    def mutate(self, info, **kwargs):
        seller_mutations = SellerMutations(info.context, **kwargs)
        return_value = seller_mutations.close_seller_cashier()
        return CloseSellerCashierType(
            success = return_value
        )


