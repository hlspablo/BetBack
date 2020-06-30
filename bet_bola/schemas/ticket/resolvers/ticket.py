from schemas.base import BaseResolver
from decimal import Decimal as dec
from ticket.models import Ticket


class TicketResolver(BaseResolver):
    queryset = Ticket.objects.all()

    def get_tickets(self):
        return self.get_queryset()
