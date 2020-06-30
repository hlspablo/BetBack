import graphene
from graphene import Field
from graphene.types import String, Int, List, Decimal
from .types import (
    TicketTypeListNode
)
from .resolvers.ticket import TicketResolver
from django_filters import FilterSet
from ticket.models import Ticket
from django.db.models import Q
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField



class TicketQuery(graphene.ObjectType):
    get_tickets = DjangoFilterConnectionField(TicketTypeListNode)

    def resolve_get_tickets(self, info, **kwargs):
        resolver = TicketResolver(info.context, **kwargs)
        return resolver.get_tickets()
