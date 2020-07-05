import graphene
from graphene import Field
from graphene.types import String, Int, List, Decimal, Boolean
from graphene_django.filter import DjangoFilterConnectionField
from .types import (
    TicketTypeListNode,
    TicketCotationsType
)
from .resolvers.ticket import TicketResolver, get_ticket_cotations


class TicketQuery(graphene.ObjectType):
    get_ticket_cotations = List(TicketCotationsType, ticket_id=String(required=True), active=Boolean())
    get_tickets = DjangoFilterConnectionField(TicketTypeListNode)

    def resolve_get_ticket_cotations(self, info, **kwargs):
        return get_ticket_cotations(info, **kwargs)


    def resolve_get_tickets(self, info, **kwargs):
        resolver = TicketResolver(info.context, **kwargs)
        return resolver.get_tickets()
