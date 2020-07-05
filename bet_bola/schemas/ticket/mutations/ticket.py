
import graphene
from graphene.types import Int, Boolean
from django.db import transaction
from utils.utils import tzlocal
from ticket.models import Ticket


@transaction.atomic
def cancel_ticket_mutation(request, **kwargs):
    # Verify if the user is from the same store
    # Verify is the seller or manager has cancel permission
    # Validate if the ticket os  status 0 (Open)
    # Validate if the ticket is Paid\
    # Validate if the game time to validate of seller and manager still valid
    # Validate if the seller canceling is the same as the creator of if the manager is
    # the manager of the seller

    ticket_id = kwargs.get('ticket_id')
    ticket = Ticket.objects.get(ticket_id=ticket_id)

    # who_paid.user_type == 2 verify with admin can pay tickets
    who_paid = ticket.payment.who_paid.seller
    if not who_paid.can_sell_unlimited:
        who_paid.credit_limit += ticket.bet_value
        who_paid.save()        

    ticket.status = 5
    ticket.payment.status = 3
    ticket.payment.save()
    ticket.save()

    from history.models import TicketCancelationHistory

    TicketCancelationHistory.objects.create(
        who_cancelled=request.user,
        ticket=ticket,
        date=tzlocal.now(),
        who_paid=who_paid,
        store=ticket.store
    )

    return {
        'success':True
    }

@transaction.atomic
def disable_ticket_mutation(request, **kwargs):
    ticket_id = kwargs.get('ticket_id')
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    ticket.available = kwargs.get('disable')
    ticket.save()

    return {
        'success': True
    }