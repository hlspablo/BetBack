from decimal import Decimal as dec
from user.models import Seller
from core.models import CotationCopy
from ticket.models import Ticket
from django.db.models import Q, Sum
from datetime import datetime
from utils import timezone as tzlocal
from schemas.base import BaseResolver
from utils.utils import get_last_monay_as_date
from .utils import get_last_closed_cashier_seller

class SellerResolver(BaseResolver):
    queryset = Seller.objects.filter(is_active=True)

    def get_seller(self):
        return self.get_queryset().get(pk=self.kwargs.get('seller_id'))

    def get_sellers_cashier(self):
        ''' GET SELLERS CASHIER METHOD '''

        self.entry_total = dec(0)
        self.incoming_total = dec(0)
        self.comission_total = dec(0)
        self.outgoing_sum_total = dec(0)
        self.outgoing_total_sum_total = dec(0)
        self.bonus_of_won_total = dec(0)
        self.open_outgoing_total = dec(0)
        self.open_tickets_count_total = 0
        self.profit_total = dec(0)
        self.profit_wost_case_total = dec(0)

        sellers = self.get_queryset()
        self.sellers = []

        for seller in sellers:
            self.username = seller.username
            self.incoming = dec(0)
            self.comission = dec(0)
            self.outgoing = dec(0)
            self.outgoing_total = dec(0)
            self.open_outgoing = dec(0)
            self.open_tickets_count = 0
            self.bonus_of_won = dec(0)
            self.entry = dec(0)

            tickets = Ticket.objects.filter(payment__status=2, payment__who_paid__pk=seller.pk).exclude(Q(status__in=[0,5,6]) | Q(available=False))
            open_tickets = Ticket.objects.filter(status=0, payment__status=2, payment__who_paid__pk=seller.pk).exclude(available=False)
        
            start_date = datetime.strptime(self.kwargs.get('start_date'), '%d/%m/%Y').strftime('%Y-%m-%d') if self.kwargs.get('start_date') else get_last_monay_as_date()
            end_date = datetime.strptime(self.kwargs.get('end_date'), '%d/%m/%Y').strftime('%Y-%m-%d') if self.kwargs.get('end_date') else tzlocal.now()

            tickets = tickets.filter(creation_date__date__gte=start_date, creation_date__date__lte=end_date)
            open_tickets = open_tickets.filter(creation_date__date__gte=start_date, creation_date__date__lte=end_date)
            
            entry = seller.my_entries.filter(creation_date__date__gte=start_date, creation_date__date__lte=end_date)\
                .aggregate(Sum('value'))['value__sum']
            
            self.entry = entry if entry else dec(0)
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
                ticket_comission = seller_key.get(cotations_count, seller_comission.sixth_more) * ticket.bet_value / 100
                self.comission += ticket_comission

                self.open_outgoing += ticket.reward.value

            # NORMAL TICKETS
            for ticket in tickets:
                self.incoming += ticket.bet_value

                cotations_count = CotationCopy.objects.filter(active=True, ticket__pk=ticket.pk).count()
                ticket_comission = seller_key.get(cotations_count, seller_comission.sixth_more) * ticket.bet_value / 100
                self.comission += ticket_comission

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
                'username': self.username,
                'entry': self.entry if self.entry else dec(0),
                'incoming': self.incoming,
                'comission':  self.comission,
                'outgoing': self.outgoing,
                'outgoing_total': self.outgoing_total,
                'open_outgoing': self.open_outgoing,
                'bonus_of_won': self.bonus_of_won,
                'open_tickets_count': self.open_tickets_count,
                'profit': self.profit,
                'profit_wost_case': self.profit_wost_case,
                'last_closed_cashier': get_last_closed_cashier_seller(seller)
            })
            
            # All total Calculations
            self.entry_total += self.entry
            self.incoming_total += self.incoming
            self.comission_total += self.comission
            self.outgoing_sum_total += self.outgoing
            self.outgoing_total_sum_total += self.outgoing_total
            self.open_tickets_count_total += self.open_tickets_count
            self.open_outgoing_total += self.open_outgoing
            self.bonus_of_won_total += self.bonus_of_won
            self.profit_total += self.profit
            self.profit_wost_case_total += self.profit_wost_case


        return {
            'entry_total': self.entry_total,
            'incoming_total': self.incoming_total,
            'comission_total': self.comission_total,
            'outgoing_sum_total': self.outgoing_sum_total,
            'outgoing_total_sum_total': self.outgoing_total_sum_total,
            'open_outgoing_total': self.open_outgoing_total,
            'bonus_of_won_total': self.bonus_of_won_total,
            'open_tickets_count_total': self.open_tickets_count_total,
            'profit_total': self.profit_total,
            'profit_wost_case_total': self.profit_wost_case_total,
            'sellers': self.sellers
        }


    def get_seller_cashier(self):
        ''' GET_SELLER_CASHIER METHOD '''

        seller = self.get_seller()
        self.username = seller.username
        self.incoming = dec(0)
        self.comission = dec(0)
        self.outgoing = dec(0)
        self.outgoing_total = dec(0)
        self.open_outgoing = dec(0)
        self.open_tickets_count = 0
        self.bonus_of_won = dec(0)
        self.entry = dec(0)
        self.tickets = []

        tickets = Ticket.objects.filter(payment__status=2, payment__who_paid__pk=seller.pk).exclude(Q(status__in=[0,5,6]) | Q(available=False))
        open_tickets = Ticket.objects.filter(status=0, payment__status=2, payment__who_paid__pk=seller.pk).exclude(available=False)
        
        start_date = datetime.strptime(self.kwargs.get('start_date'), '%d/%m/%Y').strftime('%Y-%m-%d') if self.kwargs.get('start_date') else get_last_monay_as_date()
        end_date = datetime.strptime(self.kwargs.get('end_date'), '%d/%m/%Y').strftime('%Y-%m-%d') if self.kwargs.get('end_date') else tzlocal.now()

        tickets = tickets.filter(creation_date__date__gte=start_date, creation_date__date__lte=end_date)
        open_tickets = open_tickets.filter(creation_date__date__gte=start_date, creation_date__date__lte=end_date)
        
        entry = seller.my_entries.filter(creation_date__date__gte=start_date, creation_date__date__lte=end_date)\
            .aggregate(Sum('value'))['value__sum']
        
        self.entry = entry if entry else dec(0)
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
            ticket_comission = seller_key.get(cotations_count, seller_comission.sixth_more) * ticket.bet_value / 100
            self.comission += ticket_comission

            self.open_outgoing += ticket.reward.value

            self.tickets.append({
                'ticket_id': ticket.ticket_id,
                'status': ticket.get_status_display(),
                'comission': ticket_comission,
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
            ticket_comission = seller_key.get(cotations_count, seller_comission.sixth_more) * ticket.bet_value / 100
            self.comission += ticket_comission

            if ticket.status in [2,4]:
                self.outgoing += ticket.reward.value                

            bonus_by_won = dec(0)
            if won_bonus_enabled:
                bonus_by_won = ticket.won_bonus()
                self.bonus_of_won += bonus_by_won
            
            self.tickets.append({
                'ticket_id': ticket.ticket_id,
                'status': ticket.get_status_display(),
                'comission': ticket_comission,
                'bonus_of_won': bonus_by_won,
                'bet_value': ticket.bet_value,
                'cotations_count': cotations_count,
                'reward': ticket.reward.value,
                'creation_date': ticket.creation_date.strftime("%d/%m/%Y %H:%M:%S")
            })
        
        self.outgoing_total = self.outgoing + self.comission
        self.profit = self.incoming - self.outgoing_total
        self.profit_wost_case = self.profit - self.open_outgoing

        return {
            'username': self.username,
            'entry': self.entry,
            'incoming': self.incoming,
            'comission':  self.comission,
            'outgoing': self.outgoing,
            'outgoing_total': self.outgoing_total,
            'open_outgoing': self.open_outgoing,
            'bonus_of_won': self.bonus_of_won,
            'open_tickets_count': self.open_tickets_count,
            'profit': self.profit,
            'profit_wost_case': self.profit_wost_case,
            'tickets': self.tickets
        }
