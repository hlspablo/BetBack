from ticket.models import Ticket
from django.db.models import Q
from core.models import CotationCopy

def process_tickets(tickets=None):
    if not tickets:
        tickets = Ticket.objects.filter(status=0)

    for ticket in tickets:
        #print("Processing Ticket: "+ str(ticket.ticket_id))
        ticket.update_ticket_reward()
        excluded_cotations = [cotation_copy.original_cotation.pk for cotation_copy in CotationCopy.objects.filter(ticket=ticket, active=False)]
        valid_cotations = ticket.cotations.filter(game__status__in=[0,1,2,3]).exclude(id__in=excluded_cotations)

        if not valid_cotations.count() > 0:
            ticket.status = 5
            ticket.save()
        else:
            if valid_cotations.filter(settlement=1):
                ticket.status = 1
                ticket.save()
                continue
            if valid_cotations.filter(settlement=0):
                ticket.status = 0
                ticket.save()
                continue
            if not valid_cotations.filter(~Q(settlement=2)):
                if ticket.payment.status == 2:
                    ticket.status = 4
                    ticket.save()
                else:
                    ticket.status = 3
                    ticket.save()

