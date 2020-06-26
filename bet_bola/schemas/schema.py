import graphene
from .cashier.query import CashierQuery
from .cashier.mutation import CashierMutation
from .auth.mutation import AuthMutation

class Query(
        CashierQuery
    ):
    pass

class Mutation(
        AuthMutation,
        CashierMutation
    ):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)