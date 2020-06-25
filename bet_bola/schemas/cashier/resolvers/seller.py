from decimal import Decimal as dec
from user.models import Seller
from core.models import CotationCopy
from ticket.models import Ticket
from django.db.models import Q, Sum
import datetime
from utils import timezone as tzlocal
from history.models import CashierCloseSeller

class CashierResolver():
    def __init__(self, request, **kwargs):
        self.request = request
        self.kwargs = kwargs

    def get_queryset(self):
        self.queryset = Seller.objects.filter(is_active=True)
        return self.queryset

    def get_sellers_cashier(self):

        self.entry_total = dec(0)
        self.incoming_total = dec(0)
        self.comission_total = dec(0)
        self.outgoing_total = dec(0)
        self.bonus_of_won_total = dec(0)
        self.open_outgoing_total = dec(0)
        self.open_tickets_count_total = 0
        self.outgoing_total_total = dec(0)
        self.profit_total = dec(0)
        self.profit_wost_case_total = dec(0)

        sellers = self.get_queryset()
        self.sellers = []

        for seller in sellers:
            self.incoming = dec(0)
            self.comission = dec(0)
            self.outgoing = dec(0)
            self.bonus_of_won = dec(0)
            self.open_outgoing = dec(0)
            self.entry = dec(0)
            self.open_tickets_count = 0

            tickets = Ticket.objects.filter(payment__status=2, payment__who_paid__pk=seller.pk).exclude(Q(status__in=[0,5,6]) | Q(available=False))
            open_tickets = Ticket.objects.filter(status=0, payment__status=2, payment__who_paid__pk=seller.pk).exclude(available=False)
        
            start_creation_date = self.kwargs.get('start_date') if self.kwargs.get('start_date') else None
            end_creation_date = self.kwargs.get('end_date') if self.kwargs.get('end_date') else None

            if start_creation_date:
                start_creation_date = datetime.datetime.strptime(start_creation_date, '%d/%m/%Y').strftime('%Y-%m-%d')
                tickets = tickets.filter(creation_date__date__gte=start_creation_date)
                open_tickets = open_tickets.filter(creation_date__date__gte=start_creation_date)
            else:
                last_monday = get_last_monay_as_date()
                tickets = tickets.filter(creation_date__date__gte=last_monday)
                open_tickets = open_tickets.filter(creation_date__date__gte=last_monday)
            
            if end_creation_date:
                end_creation_date = datetime.datetime.strptime(end_creation_date, '%d/%m/%Y').strftime('%Y-%m-%d')
                tickets = tickets.filter(creation_date__date__lte=end_creation_date)
                open_tickets = open_tickets.filter(creation_date__date__lte=end_creation_date)
            else:
                end_creation_date = tzlocal.now()
            
            self.entry = seller.my_entries.filter(creation_date__date__gte=start_creation_date, creation_date__date__lte=end_creation_date)\
                .aggregate(Sum('value'))['value__sum']
            
            self.open_tickets_count = open_tickets.count()
            
            won_bonus_enabled = seller.my_store.my_configuration.bonus_won_ticket
            seller_comission = seller.seller.comissions
            seller_key = {
                1:seller_comission.simple,
                2:seller_comission.double,
                3:seller_comission.triple,
                4:seller_comission.fourth,
                5:seller_comission.fifth,
                6:seller_comission.sixth
            }

            # OPEN TICKETS
            for ticket in open_tickets:
                self.incoming += ticket.bet_value

                cotations_count = CotationCopy.objects.filter(active=True, ticket__pk=ticket.pk).count()
                comission_temp = seller_key.get(cotations_count, seller_comission.sixth_more) * ticket.bet_value / 100
                self.comission += comission_temp

                self.open_outgoing += ticket.reward.value

            # NORMAL TICKETS
            for ticket in tickets:
                self.incoming += ticket.bet_value

                cotations_count = CotationCopy.objects.filter(active=True, ticket__pk=ticket.pk).count()
                comission_temp = seller_key.get(cotations_count, seller_comission.sixth_more) * ticket.bet_value / 100
                self.comission += comission_temp

                if ticket.status in [2,4]:
                    self.outgoing += ticket.reward.value                

                bonus_by_won = None
                if won_bonus_enabled:
                    bonus_by_won = ticket.won_bonus()
                    self.bonus_of_won += bonus_by_won

            self.outgoing_total = self.outgoing + self.comission
            self.profit = self.incoming - self.outgoing_total
            self.profit_wost_case = self.profit - self.open_outgoing


            self.sellers.append({
                'entry': self.entry if self.entry else dec(0),
                'incoming': self.incoming,
                'comission':  self.comission,
                'outgoing': self.outgoing,
                'bonus_of_won': self.bonus_of_won,
                'open_outgoing': self.open_outgoing,
                'open_tickets_count': self.open_tickets_count,
                'outgoing_total': self.outgoing_total,
                'profit': self.profit,
                'profit_wost_case': self.profit_wost_case,
                'last_closed_cashier': CashierCloseSeller.objects.filter(seller=seller).order_by('-date')\
                    .first().date.strftime("%d/%m/%Y %H:%M:%S") if CashierCloseSeller\
                    .objects.filter(seller=seller).count() > 0 else "Sem Registro"
            })
            
            # All total Calculations
            self.entry_total += self.entry if self.entry else dec(0)
            self.incoming_total += self.incoming
            self.comission_total += self.comission
            self.bonus_of_won_total += self.bonus_of_won
            self.open_outgoing_total += self.open_outgoing
            self.open_tickets_count_total += self.open_tickets_count
            self.outgoing_total_total += self.outgoing_total
            self.profit_total += self.profit
            self.profit_wost_case_total += self.profit_wost_case


        return {
            'entry_total': self.entry_total,
            'incoming_total': self.incoming_total,
            'comission_total': self.comission_total,
            'bonus_of_won_total': self.bonus_of_won_total,
            'open_outgoing_total': self.open_outgoing_total,
            'open_tickets_count_total': self.open_tickets_count_total,
            'outgoing_total_total': self.outgoing_total_total,
            'profit_total': self.profit_total,
            'profit_wost_case_total': self.profit_wost_case_total,
            'sellers': self.sellers
        }


    def get_seller_cashier(self):
        seller = self.get_queryset()

        self.incoming = dec(0)
        self.comission = dec(0)
        self.outgoing = dec(0)
        self.bonus_of_won = dec(0)
        self.open_outgoing = dec(0)
        self.entry = dec(0)
        self.open_tickets_count = 0
        self.tickets = []

        tickets = Ticket.objects.filter(payment__status=2, payment__who_paid__pk=seller.pk).exclude(Q(status__in=[0,5,6]) | Q(available=False))
        open_tickets = Ticket.objects.filter(status=0, payment__status=2, payment__who_paid__pk=seller.pk).exclude(available=False)
    
        start_creation_date = self.kwargs.get('start_date') if self.kwargs.get('start_date') else None
        end_creation_date = self.kwargs.get('end_date') if self.kwargs.get('end_date') else None

        if start_creation_date:
            start_creation_date = datetime.datetime.strptime(start_creation_date, '%d/%m/%Y').strftime('%Y-%m-%d')
            tickets = tickets.filter(creation_date__date__gte=start_creation_date)
            open_tickets = open_tickets.filter(creation_date__date__gte=start_creation_date)
        else:
            last_monday = get_last_monay_as_date()
            tickets = tickets.filter(creation_date__date__gte=last_monday)
            open_tickets = open_tickets.filter(creation_date__date__gte=last_monday)
        
        if end_creation_date:
            end_creation_date = datetime.datetime.strptime(end_creation_date, '%d/%m/%Y').strftime('%Y-%m-%d')
            tickets = tickets.filter(creation_date__date__lte=end_creation_date)
            open_tickets = open_tickets.filter(creation_date__date__lte=end_creation_date)
        else:
            end_creation_date = tzlocal.now()
        
        self.entry = seller.my_entries.filter(creation_date__date__gte=start_creation_date, creation_date__date__lte=end_creation_date)\
            .aggregate(Sum('value'))['value__sum']
        
        self.open_tickets_count = open_tickets.count()
        
        won_bonus_enabled = seller.my_store.my_configuration.bonus_won_ticket
        seller_comission = seller.seller.comissions
        seller_key = {
            1:seller_comission.simple,
            2:seller_comission.double,
            3:seller_comission.triple,
            4:seller_comission.fourth,
            5:seller_comission.fifth,
            6:seller_comission.sixth
        }

        # OPEN TICKETS
        for ticket in open_tickets:
            self.incoming += ticket.bet_value

            cotations_count = CotationCopy.objects.filter(active=True, ticket__pk=ticket.pk).count()
            comission_temp = seller_key.get(cotations_count, seller_comission.sixth_more) * ticket.bet_value / 100
            self.comission += comission_temp

            self.open_outgoing += ticket.reward.value

            self.tickets.append({
                'ticket_id': ticket.ticket_id,
                'status': ticket.get_status_display(),
                'comission': comission_temp,
                'bonus_of_won': dec(0),
                'bet_value': ticket.bet_value,
                'cotations_count': cotations_count,
                'reward': ticket.reward.value,
                'creation_date': ticket.creation_date.strftime("%d/%m/%Y %H:%M:%S")
            })

        # NORMAL TICKETS
        for ticket in tickets:
            self.incoming += ticket.bet_value

            cotations_count = CotationCopy.objects.filter(active=True, ticket__pk=ticket.pk).count()
            comission_temp = seller_key.get(cotations_count, seller_comission.sixth_more) * ticket.bet_value / 100
            self.comission += comission_temp

            if ticket.status in [2,4]:
                self.outgoing += ticket.reward.value                

            bonus_by_won = None
            if won_bonus_enabled:
                bonus_by_won = ticket.won_bonus()
                self.bonus_of_won += bonus_by_won
            
            self.tickets.append({
                'ticket_id': ticket.ticket_id,
                'status': ticket.get_status_display(),
                'comission': comission_temp,
                'bonus_of_won': bonus_by_won if bonus_by_won else dec(0),
                'bet_value': ticket.bet_value,
                'cotations_count': cotations_count,
                'reward': ticket.reward.value,
                'creation_date': ticket.creation_date.strftime("%d/%m/%Y %H:%M:%S")
            })
        
        self.outgoing_total = self.outgoing + self.comission
        self.profit = self.incoming - self.outgoing_total
        self.profit_wost_case = self.profit - self.open_outgoing

        return {
            'entry': self.entry if self.entry else dec(0),
            'incoming': self.incoming,
            'comission':  self.comission,
            'outgoing': self.outgoing,
            'bonus_of_won': self.bonus_of_won,
            'tickets': self.tickets,
            'open_outgoing': self.open_outgoing,
            'open_tickets_count': self.open_tickets_count,
            'outgoing_total': self.outgoing_total,
            'profit': self.profit,
            'profit_wost_case': self.profit_wost_case
        }
