import graphene
from graphene import Field
from graphene.types import Boolean, Int, String, List
from .mutations.ticket import cancel_ticket_mutation, disable_ticket_mutation

class DisableTicketType(graphene.Mutation):
    success = Boolean()
    errors = List(String)

    class Arguments:
        ticket_id = String()
        disable = Boolean(required=True)

    def mutate(self, info, **kwargs):
        return disable_ticket_mutation(info.context, **kwargs)


class CancelTicketType(graphene.Mutation):
    success = Boolean()
    errors = List(String)

    class Arguments:
        ticket_id = String()

    def mutate(self, info, **kwargs):
        return cancel_ticket_mutation(info.context, **kwargs)

