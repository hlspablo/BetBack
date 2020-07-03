import graphene
from graphene import  Field
from .mutationTypes import CancelTicketType, DisableTicketType

class TicketMutation(graphene.ObjectType):
    cancel_ticket = CancelTicketType.Field()
    disable_ticket = DisableTicketType.Field()