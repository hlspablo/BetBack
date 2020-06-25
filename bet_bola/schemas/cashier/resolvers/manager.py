from decimal import Decimal as dec
from user.models import Seller, Manager
from core.models import CotationCopy
from ticket.models import Ticket
from django.db.models import Q, Sum
from datetime import  datetime
from utils import timezone as tzlocal
from .base import BaseResolver
from utils.utils import get_last_monay_as_date
from .utils import get_last_closed_cashier_seller

class ManagerResolver(BaseResolver):
    queryset = Manager.objects.filter(is_active=True)

    def get_managers(self):
        return self.get_queryset()

    def get_manager(self):
        return self.get_queryset().get(pk=self.kwargs.get('manager_id'))

    def get_managers_cashier(self):
        ''' GET MANAGERS CASHIER METHOD '''
        self.incoming_total = dec(0)
        self.seller_comission_total = dec(0)
        self.manager_comission_total = dec(0)
        self.outgoing_total = dec(0)
        self.bonus_of_won_total = dec(0)
        self.open_outgoing_total = dec(0)
        self.entry_total = dec(0)
        self.open_tickets_count_total = 0
        self.managers = []

        managers = self.get_managers()
        for manager in managers:
            self.manager_username = manager.username
            manager_comission = manager.comissions
            manager_key = {
                1: manager_comission.simple,
                2: manager_comission.double,
                3: manager_comission.triple,
                4: manager_comission.fourth,
                5: manager_comission.fifth,
                6: manager_comission.sixth
            }

            sellers = Seller.objects.filter(my_manager=manager, is_active=True)
        
            if not sellers:
                continue
            
            self.incoming_sum = dec(0)
            self.seller_comission_sum = dec(0)
            self.manager_comission_sum = dec(0)
            self.outgoing_sum = dec(0)
            self.bonus_of_won_sum = dec(0)
            self.open_outgoing_sum = dec(0)
            self.entry_sum = dec(0)
            self.open_tickets_count_sum = 0

            for seller in sellers:
                self.incoming = dec(0)
                self.seller_comission = dec(0)
                self.manager_comission = dec(0)
                self.outgoing = dec(0)
                self.bonus_of_won = dec(0)
                self.open_outgoing = dec(0)
                self.entry = dec(0)
                self.open_tickets_count = 0

                tickets = Ticket.objects.filter(payment__status=2, payment__who_paid__pk=seller.pk).exclude(Q(status__in=[0,5,6]) | Q(available=False))
                open_tickets = Ticket.objects.filter(status=0, payment__status=2, payment__who_paid__pk=seller.pk).exclude(available=False)
            
                start_date = datetime.strptime(self.kwargs.get('start_date'), '%d/%m/%Y').strftime('%Y-%m-%d') if self.kwargs.get('start_date') else get_last_monay_as_date()
                end_date = datetime.strptime(self.kwargs.get('end_date'), '%d/%m/%Y').strftime('%Y-%m-%d') if self.kwargs.get('end_date') else tzlocal.now()

                tickets = tickets.filter(creation_date__date__gte=start_date, creation_date__date__lte=end_date)
                open_tickets = open_tickets.filter(creation_date__date__gte=start_date, creation_date__date__lte=end_date)
                
                entry = seller.my_entries.filter(creation_date__date__gte=start_date, creation_date__date__lte=end_date)\
                    .aggregate(Sum('value'))['value__sum']

                self.entry += entry if entry else dec(0)
                
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
                    ticket_comission = (seller_key.get(cotations_count, seller_comission.sixth_more) * ticket.bet_value / 100)
                    self.seller_comission += ticket_comission
                    self.manager_comission += (manager_key.get(cotations_count, manager_comission.sixth_more) * ticket.bet_value / 100)

                    self.open_outgoing += ticket.reward.value
        
                # NORMAL TICKETS
                for ticket in tickets:
                    self.incoming += ticket.bet_value

                    cotations_count = CotationCopy.objects.filter(active=True, ticket__pk=ticket.pk).count()
                    ticket_comission = (seller_key.get(cotations_count, seller_comission.sixth_more) * ticket.bet_value / 100)
                    self.seller_comission += ticket_comission
                    self.manager_comission += (manager_key.get(cotations_count, manager_comission.sixth_more) * ticket.bet_value / 100)

                    if ticket.status in [2,4]:
                        self.outgoing += ticket.reward.value                

                    bonus_by_won = dec(0)
                    if won_bonus_enabled:
                        bonus_by_won = ticket.won_bonus()
                        self.bonus_of_won += bonus_by_won
            
                # Acumulate to get Manager Acumulated
                self.incoming_sum += self.incoming
                self.seller_comission_sum += self.seller_comission
                self.manager_comission_sum += self.manager_comission
                self.outgoing_sum += self.outgoing
                self.bonus_of_won_sum += self.bonus_of_won
                self.open_outgoing_sum += self.open_outgoing
                self.entry_sum += self.entry
                self.open_tickets_count_sum += self.open_tickets_count

            #Get Profit Results from Acumulated to the Manager
            self.outgoing_total_sum = self.outgoing_sum + self.seller_comission_sum + self.manager_comission_sum
            self.profit_sum = self.incoming_sum - self.outgoing_total_sum
            self.profit_wost_case_sum = self.profit_sum - self.open_outgoing_sum

            #Create Manager Acumulated
            self.managers.append({
                'manager': self.manager_username,
                'entry': self.entry_sum,
                'incoming': self.incoming_sum,
                'seller_comission':  self.seller_comission_sum,
                'manager_comission':  self.manager_comission_sum,
                'outgoing': self.outgoing_sum,
                'bonus_of_won': self.bonus_of_won_sum,
                'open_outgoing': self.open_outgoing_sum,
                'open_tickets_count': self.open_tickets_count_sum,
                'outgoing_total': self.outgoing_total_sum,
                'profit': self.profit_sum,
                'profit_wost_case': self.profit_wost_case_sum,
                'last_closed_cashier': get_last_closed_cashier_manager(manager)
            })

            #Acumulate Managers to get General Total
            self.incoming_total += self.incoming_sum
            self.seller_comission_total += self.seller_comission_sum
            self.manager_comission_total += self.manager_comission_sum

            self.outgoing_sum_total =+ self.outgoing_sum
            self.outgoing_total_sum_total =+ self.outgoing_total_sum

            self.bonus_of_won_total += self.bonus_of_won_sum
            self.open_outgoing_total += self.open_outgoing_sum
            self.entry_total += self.entry_sum
            self.open_tickets_count_total += self.open_tickets_count_sum
        
        # get profit form Final Acumulations
        self.outgoing_total_final = self.outgoing_total_sum_total + self.seller_comission_total + self.manager_comission_total
        self.profit_final = self.incoming_total - self.outgoing_total_final
        self.profit_wost_case_final = self.profit_final - self.open_outgoing_total

        return {
            'entry_total': self.entry_total,
            'incoming_total': self.incoming_total,
            'seller_comission_total':  self.seller_comission_total,
            'manager_comission_total':  self.manager_comission_total,

            'outgoing_sum_total': self.outgoing_sum_total,
            'outgoing_total_sum_total': self.outgoing_total_sum_total,

            'bonus_of_won_total': self.bonus_of_won_total,
            'open_outgoing_total': self.open_outgoing_total,
            'open_tickets_count_total': self.open_tickets_count_total,

            'profit_final': self.profit_final,
            'profit_wost_case_final': self.profit_wost_case_final,

            'managers': self.managers
        }


    def get_manager_cashier(self):
        ''' GET_MANAGER_CASHIER METHOD '''

        manager = self.get_manager()
        self.username = manager.username
        manager_comission = manager.comissions
        manager_key = {
            1: manager_comission.simple,
            2: manager_comission.double,
            3: manager_comission.triple,
            4: manager_comission.fourth,
            5: manager_comission.fifth,
            6: manager_comission.sixth
        }

        sellers = Seller.objects.filter(my_manager=manager, is_active=True)

        self.incoming_sum = dec(0)
        self.seller_comission_sum = dec(0)
        self.manager_comission_sum = dec(0)
        self.outgoing_sum = dec(0)
        self.outgoing_total_sum = dec(0)
        self.open_outgoing_sum = dec(0)
        self.bonus_of_won_sum = dec(0)
        self.entry_sum = dec(0)
        self.open_tickets_count_sum = 0
        self.open_tickets = []
        self.tickets = []

        for seller in sellers:
            self.incoming = dec(0)
            self.seller_comission = dec(0)
            self.manager_comission = dec(0)
            self.outgoing = dec(0)
            self.outgoing_total = dec(0)
            self.open_outgoing = dec(0)
            self.bonus_of_won = dec(0)
            self.entry = dec(0)
            self.open_tickets_count = 0

            tickets = Ticket.objects.filter(payment__status=2, payment__who_paid__pk=seller.pk).exclude(Q(status__in=[0,5,6]) | Q(available=False))
            open_tickets = Ticket.objects.filter(status=0, payment__status=2, payment__who_paid__pk=seller.pk).exclude(available=False)

            start_date = datetime.strptime(self.kwargs.get('start_date'), '%d/%m/%Y').strftime('%Y-%m-%d') if self.kwargs.get('start_date') else get_last_monay_as_date()
            end_date = datetime.strptime(self.kwargs.get('end_date'), '%d/%m/%Y').strftime('%Y-%m-%d') if self.kwargs.get('end_date') else tzlocal.now()

            tickets = tickets.filter(creation_date__date__gte=start_date, creation_date__date__lte=end_date)
            open_tickets = open_tickets.filter(creation_date__date__gte=start_date, creation_date__date__lte=end_date)
            
            entry = seller.my_entries.filter(creation_date__date__gte=start_date, creation_date__date__lte=end_date)\
                .aggregate(Sum('value'))['value__sum']

            self.entry += entry if entry else dec(0)
            
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
                ticket_comission = (seller_key.get(cotations_count, seller_comission.sixth_more) * ticket.bet_value / 100)
                self.seller_comission += ticket_comission
                self.manager_comission += (manager_key.get(cotations_count, manager_comission.sixth_more) * ticket.bet_value / 100)


                self.open_outgoing += ticket.reward.value

                self.open_tickets.append({
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
                ticket_comission = (seller_key.get(cotations_count, seller_comission.sixth_more) * ticket.bet_value / 100)
                self.seller_comission += ticket_comission
                self.manager_comission += (manager_key.get(cotations_count, manager_comission.sixth_more) * ticket.bet_value / 100)

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
        
            self.incoming_sum += self.incoming
            self.seller_comission_sum += self.seller_comission
            self.manager_comission_sum += self.manager_comission
            self.outgoing_sum += self.outgoing
            self.open_outgoing_sum += self.open_outgoing
            self.bonus_of_won_sum += self.bonus_of_won
            self.entry_sum += self.entry
            self.open_tickets_count_sum += self.open_tickets_count

        self.outgoing_total_sum = self.outgoing_sum + self.seller_comission_sum + self.manager_comission_sum
        self.profit_sum = self.incoming_sum - self.outgoing_total_sum
        self.profit_wost_case_sum = self.profit_sum - self.open_outgoing_sum


        return {
            'username': self.username,
            'entry': self.entry_sum,
            'incoming': self.incoming_sum,
            'seller_comission':  self.seller_comission_sum,
            'manager_comission':  self.manager_comission_sum,
            'outgoing': self.outgoing_sum,
            'outgoing_total': self.outgoing_total_sum,
            'open_outgoing': self.open_outgoing_sum,
            'bonus_of_won': self.bonus_of_won_sum,
            'open_tickets_count': self.open_tickets_count_sum,
            'profit': self.profit_sum,
            'profit_wost_case': self.profit_wost_case_sum,
            'tickets': self.open_tickets + self.tickets,
        }


    def get_manager_owner_cashier(self):
        ''' GET_MANAGER_OWNER_CASHIER METHOD '''

        manager = self.get_manager()
        self.manager_username = manager.username
        manager_comission = manager.comissions
        manager_key = {
            1: manager_comission.simple,
            2: manager_comission.double,
            3: manager_comission.triple,
            4: manager_comission.fourth,
            5: manager_comission.fifth,
            6: manager_comission.sixth
        }

        sellers = Seller.objects.filter(my_manager=manager, is_active=True)

        self.incoming_sum = dec(0)
        self.seller_comission_sum = dec(0)
        self.manager_comission_sum = dec(0)
        self.outgoing_sum = dec(0)
        self.outgoing_total_sum = dec(0)
        self.open_outgoing_sum = dec(0)
        self.bonus_of_won_sum = dec(0)
        self.entry_sum = dec(0)
        self.open_tickets_count_sum = 0
        self.sellers = []

        for seller in sellers:
            self.username = seller.username
            self.incoming = dec(0)
            self.seller_comission = dec(0)
            self.manager_comission = dec(0)
            self.outgoing = dec(0)
            self.outgoing_total = dec(0)
            self.open_outgoing = dec(0)
            self.bonus_of_won = dec(0)
            self.entry = dec(0)
            self.open_tickets_count = 0

            tickets = Ticket.objects.filter(payment__status=2, payment__who_paid__pk=seller.pk).exclude(Q(status__in=[0,5,6]) | Q(available=False))
            open_tickets = Ticket.objects.filter(status=0, payment__status=2, payment__who_paid__pk=seller.pk).exclude(available=False)
        
            start_date = datetime.strptime(self.kwargs.get('start_date'), '%d/%m/%Y').strftime('%Y-%m-%d') if self.kwargs.get('start_date') else get_last_monay_as_date()
            end_date = datetime.strptime(self.kwargs.get('end_date'), '%d/%m/%Y').strftime('%Y-%m-%d') if self.kwargs.get('end_date') else tzlocal.now()

            tickets = tickets.filter(creation_date__date__gte=start_date, creation_date__date__lte=end_date)
            open_tickets = open_tickets.filter(creation_date__date__gte=start_date, creation_date__date__lte=end_date)
            
            entry = seller.my_entries.filter(creation_date__date__gte=start_date, creation_date__date__lte=end_date)\
                .aggregate(Sum('value'))['value__sum']

            self.entry += entry if entry else dec(0)
            
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
                ticket_comission = (seller_key.get(cotations_count, seller_comission.sixth_more) * ticket.bet_value / 100)
                self.seller_comission += ticket_comission
                self.manager_comission += (manager_key.get(cotations_count, manager_comission.sixth_more) * ticket.bet_value / 100)
                self.open_outgoing += ticket.reward.value


            # NORMAL TICKETS
            for ticket in tickets:
                self.incoming += ticket.bet_value

                cotations_count = CotationCopy.objects.filter(active=True, ticket__pk=ticket.pk).count()
                ticket_comission = (seller_key.get(cotations_count, seller_comission.sixth_more) * ticket.bet_value / 100)
                self.seller_comission += ticket_comission
                self.manager_comission += (manager_key.get(cotations_count, manager_comission.sixth_more) * ticket.bet_value / 100)

                if ticket.status in [2,4]:
                    self.outgoing += ticket.reward.value                

                bonus_by_won = dec(0)
                if won_bonus_enabled:
                    bonus_by_won = ticket.won_bonus()
                    self.bonus_of_won += bonus_by_won

            self.incoming_sum += self.incoming
            self.seller_comission_sum += self.seller_comission
            self.manager_comission_sum += self.manager_comission
            self.outgoing_sum += self.outgoing
            self.open_outgoing_sum += self.open_outgoing
            self.bonus_of_won_sum += self.bonus_of_won
            self.entry_sum += self.entry
            self.open_tickets_count_sum += self.open_tickets_count

            self.outgoing_total = self.outgoing + self.seller_comission + self.manager_comission
            self.profit = self.incoming - self.outgoing_total
            self.profit_wost_case = self.profit - self.open_outgoing

            self.sellers.append({
                'username': self.username,
                'entry': self.entry,
                'incoming': self.incoming,
                'comission': self.seller_comission,
                'outgoing': self.outgoing,
                'outgoing_total': self.outgoing_total,
                'open_outgoing': self.open_outgoing,
                'bonus_of_won': self.bonus_of_won,
                'open_tickets_count': self.open_tickets_count,
                'profit': self.profit,
                'profit_wost_case': self.profit_wost_case,
                'last_closed_cashier': get_last_closed_cashier_seller(seller)
            })

        self.outgoing_total_sum = self.outgoing_sum + self.seller_comission_sum + self.manager_comission_sum
        self.profit_sum = self.incoming_sum - self.outgoing_total_sum
        self.profit_wost_case_sum = self.profit_sum - self.open_outgoing_sum


        return {
            'username': self.username,
            'entry': self.entry_sum,
            'incoming': self.incoming_sum,
            'seller_comission':  self.seller_comission_sum,
            'manager_comission':  self.manager_comission_sum,
            'outgoing': self.outgoing_sum,
            'outgoing_total': self.outgoing_total_sum,
            'open_outgoing': self.open_outgoing_sum,
            'bonus_of_won': self.bonus_of_won_sum,
            'open_tickets_count': self.open_tickets_count_sum,
            'profit': self.profit_sum,
            'profit_wost_case': self.profit_wost_case_sum,
            'sellers': self.sellers
        }
