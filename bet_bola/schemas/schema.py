import graphene

from .cashier.query import CashierQuery
from .cashier.mutation import CashierMutation
from .auth.mutation import AuthMutation
from .ticket.query import TicketQuery
from .ticket.mutation import TicketMutation
from .general.query import GeneralQuery
from .users.mutation import UserMutation
from .users.query import UserQuery

class Query(
        CashierQuery,
        TicketQuery,
        GeneralQuery,
        UserQuery
    ):
    pass

class Mutation(
        AuthMutation,
        CashierMutation,
        TicketMutation,
        UserMutation
    ):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)