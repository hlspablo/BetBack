import graphene
from .cashier.query import CashierQuery
from .cashier.mutation import CashierMutation

class Query(
        CashierQuery
    ):
    pass

class Mutation(
        CashierMutation
    ):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)