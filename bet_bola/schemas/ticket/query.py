import graphene
from graphene import Field
from graphene.types import String, Int, List
from .types import (
    TicketTypeList
)
from .resolvers.ticket import TicketResolver

class TicketQuery(graphene.ObjectType):
    get_tickets = List(TicketTypeList)

    def resolve_get_tickets(self, info, **kwargs):
        resolver = TicketResolver(info.context, **kwargs)
        return resolver.get_tickets()
