from schemas.base import BaseResolver
from decimal import Decimal as dec
from ticket.models import Ticket
from core.models import CotationCopy

def get_ticket_cotations(**kwargs):
    ticket_id = kwargs.get('ticket_id')
    active = kwargs.get('active')
    cotations_list = []

    cotations = CotationCopy.objects.filter(ticket__ticket_id=ticket_id)
    
    if not active == None:
        cotations = cotations.filter(active=active)
    
    for cotation in cotations:
        original_cotation = cotation.original_cotation
        cotations_list.append({
            'game': original_cotation.game.name,
            'data': original_cotation.game.start_date,
            'market': original_cotation.market.name,
            'name': original_cotation.name,
            'price': cotation.price,
            'status': original_cotation.get_settlement_display(),
            'active': cotation.active
        })

    return cotations_list

class TicketResolver(BaseResolver):
    queryset = Ticket.objects.all()

    def get_tickets(self):
        return self.get_queryset()
