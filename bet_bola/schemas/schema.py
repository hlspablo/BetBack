import graphene
from .cashier.query import CashierQuery
from .cashier.mutation import CashierMutation
from .auth.mutation import AuthMutation
from .ticket.query import TicketQuery
from .general.query import GeneralQuery

class Query(
        CashierQuery,
        TicketQuery,
        GeneralQuery
    ):
    pass

class Mutation(
        AuthMutation,
        CashierMutation
    ):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)