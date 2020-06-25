from django.db.models import Q, Count
from rest_framework import serializers
from rest_framework.response import Response
from ticket.serializers.reward import RewardSerializer, RewardSerializer
from ticket.serializers.payment import PaymentSerializerWithSeller, PaymentSerializer
from core.serializers.cotation import CotationTicketSerializer
from user.serializers.owner import OwnerSerializer
from ticket.paginations import TicketPagination
from utils.models import TicketCustomMessage
from utils import timezone as tzlocal
from ticket.models import Ticket
from user.models import TicketOwner
from user.models import CustomUser, Seller, Manager
from core.models import Store, Cotation, CotationCopy
from decimal import Decimal
import datetime
import json
from utils.utils import get_last_monay_as_date
from django.db.models import Sum


class ManagerCashierSerializer(serializers.HyperlinkedModelSerializer):
    initialization_field = serializers.SerializerMethodField()
    entry = serializers.SerializerMethodField()
    manager_comission = serializers.SerializerMethodField()
    seller_comission = serializers.SerializerMethodField()
    out = serializers.SerializerMethodField()
    open_out = serializers.SerializerMethodField()
    won_bonus = serializers.SerializerMethodField()
    total_out = serializers.SerializerMethodField()
    profit = serializers.SerializerMethodField()
    profit_wc = serializers.SerializerMethodField()
    open_tickets = serializers.SerializerMethodField()
    tickets = serializers.SerializerMethodField()
    

    entry_value_init = 0
    manager_comission_init = 0
    seller_comission_init = 0
    out_value_init = 0
    open_out_init = 0
    won_bonus_init = 0
    total_out_init = 0
    open_tickets_count = 0
    tickets_init = []

    def get_initialization_field(self, manager):
        self.entry_value_init = 0
        self.manager_comission_init = 0
        self.seller_comission_init = 0
        self.out_value_init = 0
        self.open_out_init = 0
        self.won_bonus_init = 0
        self.total_out_init = 0
        self.open_tickets_count = 0
        self.tickets_init = []

        manager_comission = manager.comissions
        
        manager_key = {
            1:manager_comission.simple,
            2:manager_comission.double,
            3:manager_comission.triple,
            4:manager_comission.fourth,
            5:manager_comission.fifth,
            6:manager_comission.sixth
        }
        won_bonus_enabled = manager.my_store.my_configuration.bonus_won_ticket

        sellers = Seller.objects.filter(my_manager__pk=manager.pk).exclude(is_active=False)

        for seller in sellers:
            tickets = Ticket.objects.filter(payment__status=2, payment__who_paid__pk=seller.pk).exclude(Q(status__in=[0,5,6]) | Q(available=False))
            open_tickets = Ticket.objects.filter(status=0, payment__status=2, payment__who_paid__pk=seller.pk).exclude(available=False)

            get_data = self.context['request'].GET
            start_creation_date = None
            end_creation_date = None

            if get_data:
                start_creation_date = get_data.get('start_creation_date')
                end_creation_date = get_data.get('end_creation_date')

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

            self.open_tickets_count = open_tickets.count()
         

            seller_comission = seller.comissions

            seller_key = {
                1:seller_comission.simple,
                2:seller_comission.double,
                3:seller_comission.triple,
                4:seller_comission.fourth,
                5:seller_comission.fifth,
                6:seller_comission.sixth
            }

            for ticket in open_tickets:
                cotations_count = CotationCopy.objects.filter(active=True, ticket__pk=ticket.pk).count()
                # manager comissions
                self.manager_comission_init += manager_key.get(cotations_count, manager_comission.sixth_more) * ticket.bet_value / 100

                # seller comissions
                self.seller_comission_init += seller_key.get(cotations_count, seller_comission.sixth_more) * ticket.bet_value / 100

                # entry value
                self.entry_value_init += ticket.bet_value

                # calculating out value
                self.open_out_init += ticket.reward.value

                # calculating won bonus
                if won_bonus_enabled:
                    self.won_bonus_init += ticket.won_bonus()

                self.tickets_init.append({
                    'ticket_id':ticket.ticket_id,
                    'status':ticket.get_status_display(),
                    'won_bonus':ticket.won_bonus(),
                    'bet_value': ticket.bet_value,
                    'cotations_count': CotationCopy.objects.filter(active=True, ticket__pk=ticket.pk).count(),
                    'seller': ticket.payment.who_paid.username,
                    'reward_value':ticket.reward.value,
                    'creation_date':ticket.creation_date.strftime("%d/%m/%Y %H:%M:%S")
                })

            for ticket in tickets:
                cotations_count = CotationCopy.objects.filter(active=True, ticket__pk=ticket.pk).count()
                # manager comissions
                self.manager_comission_init += manager_key.get(cotations_count, manager_comission.sixth_more) * ticket.bet_value / 100

                # seller comissions
                self.seller_comission_init += seller_key.get(cotations_count, seller_comission.sixth_more) * ticket.bet_value / 100

                # entry value
                self.entry_value_init += ticket.bet_value

                # calculating out value
                if ticket.status in [2,4]:
                    self.out_value_init += ticket.reward.value

                # calculating won bonus
                if won_bonus_enabled:
                    self.won_bonus_init += ticket.won_bonus()

                self.tickets_init.append({
                    'ticket_id':ticket.ticket_id,
                    'status':ticket.get_status_display(),
                    'won_bonus':ticket.won_bonus(),
                    'bet_value': ticket.bet_value,
                    'cotations_count': CotationCopy.objects.filter(active=True, ticket__pk=ticket.pk).count(),
                    'seller': ticket.payment.who_paid.username,
                    'reward_value':ticket.reward.value,
                    'creation_date':ticket.creation_date.strftime("%d/%m/%Y %H:%M:%S")
                })

            # defining total out
            self.total_out_init = self.out_value_init + self.seller_comission_init + self.manager_comission_init




            
    def get_entry(self, user):
        return self.entry_value_init

    def get_out(self, user):
        return self.out_value_init

    def get_open_out(self, user):
        return self.open_out_init

    def get_total_out(self, user):
        return self.total_out_init

    def get_won_bonus(self, user):
        return self.won_bonus_init
        
    def get_manager_comission(self, user):
        return self.manager_comission_init
    
    def get_seller_comission(self, user):
        return self.seller_comission_init

    def get_profit(self, user):
        return self.entry_value_init - self.total_out_init

    def get_open_tickets(self, user):
        return self.open_tickets_count

    def get_profit_wc(self, user):
        return self.entry_value_init - (self.total_out_init + self.open_out_init)
    
    def get_tickets(self, user):
        return self.tickets_init

    class Meta:
        model = CustomUser
        fields = ('id','initialization_field','entry','out',
        'open_out','total_out','won_bonus','manager_comission',
        'seller_comission','profit','profit_wc','tickets','open_tickets'
    )


class SellerCashierSerializer(serializers.HyperlinkedModelSerializer):
    initialization_field = serializers.SerializerMethodField()
    entry = serializers.SerializerMethodField()
    entry_lan = serializers.SerializerMethodField()
    comission = serializers.SerializerMethodField()
    out = serializers.SerializerMethodField()
    won_bonus = serializers.SerializerMethodField()
    total_out = serializers.SerializerMethodField()
    profit = serializers.SerializerMethodField()
    tickets = serializers.SerializerMethodField()
    open_out = serializers.SerializerMethodField()
    open_tickets_count = serializers.SerializerMethodField()
    profit_wc = serializers.SerializerMethodField()

    entry_value_init = 0
    comission_init = 0
    out_value_init = 0
    won_bonus_init = 0
    tickets_init = []
    open_out_init = 0
    open_tickets_count_init = 0
    entry_init = 0

    def get_initialization_field(self, seller):    
        self.entry_value_init = 0
        self.comission_init = 0
        self.out_value_init = 0
        self.won_bonus_init = 0
        self.open_out_init = 0
        self.entry_init = 0
        self.open_tickets_count = 0
        self.tickets_init = []

        tickets = Ticket.objects.filter(payment__status=2, payment__who_paid__pk=seller.pk).exclude(Q(status__in=[0,5,6]) | Q(available=False))
        open_tickets = Ticket.objects.filter(status=0, payment__status=2, payment__who_paid__pk=seller.pk).exclude(available=False)
    
        get_data = self.context['request'].GET
        start_creation_date = None
        end_creation_date = None

        if get_data:
            start_creation_date = get_data.get('start_creation_date')
            end_creation_date = get_data.get('end_creation_date')

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
        
        entry_init = seller.my_entries.filter(creation_date__date__gte=start_creation_date, creation_date__date__lte=end_creation_date)\
            .aggregate(Sum('value'))['value__sum']
        
        if entry_init:
            self.entry_init = entry_init   

        self.open_tickets_count_init = open_tickets.count()
        
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

        for ticket in open_tickets:
            # entry value
            self.entry_value_init += ticket.bet_value

            # seller comissions
            cotations_count = CotationCopy.objects.filter(active=True, ticket__pk=ticket.pk).count()
            comission_temp = seller_key.get(cotations_count, seller_comission.sixth_more) * ticket.bet_value / 100
            self.comission_init += comission_temp

            self.open_out_init += ticket.reward.value

            self.tickets_init.append({
                'ticket_id': ticket.ticket_id,
                'status': ticket.get_status_display(),
                'comission': comission_temp,
                'won_bonus': ticket.won_bonus(),
                'bet_value': ticket.bet_value,
                'cotations_count': cotations_count,
                'reward':{'value': ticket.reward.value},
                'creation_date': ticket.creation_date.strftime("%d/%m/%Y %H:%M:%S")
            })
            
        for ticket in tickets:
            # entry value
            self.entry_value_init += ticket.bet_value

            # seller comissions
            cotations_count = CotationCopy.objects.filter(active=True, ticket__pk=ticket.pk).count()
            comission_temp = seller_key.get(cotations_count, seller_comission.sixth_more) * ticket.bet_value / 100
            self.comission_init += comission_temp

            if ticket.status in [2,4]:
                self.out_value_init += ticket.reward.value                

            # calculating won bonus
            if won_bonus_enabled:
                self.won_bonus_init += ticket.won_bonus()
            
            self.tickets_init.append({
                'ticket_id': ticket.ticket_id,
                'status': ticket.get_status_display(),
                'comission': comission_temp,
                'won_bonus': ticket.won_bonus(),
                'bet_value': ticket.bet_value,
                'cotations_count': cotations_count,
                'reward':{'value': ticket.reward.value},
                'creation_date': ticket.creation_date.strftime("%d/%m/%Y %H:%M:%S")
            })

        #self.total_out_init = self.out_value_init + self.comission_init
        #self.profit_init = self.entry_value_init - self.total_out_init

        
    def get_entry(self, seller):
        return self.entry_value_init
    def get_entry_lan(self, seller):
        return self.entry_init
    def get_out(self, seller):
        return self.out_value_init - self.entry_init

    def get_total_out(self, seller):
        return (self.out_value_init + self.comission_init) - self.entry_init

    def get_won_bonus(self, seller):
        return self.won_bonus_init
    def get_comission(self, seller):
        return self.comission_init
    def get_tickets(self, seller):        
        return self.tickets_init
    def get_open_entry(self, seller):
        return self.open_entry_init
    def get_open_comission(self, seller):
        return self.open_comission_init
    def get_open_out(self, seller):
        return self.open_out_init
    def get_open_tickets_count(self, seller):
        return self.open_tickets_count_init

    def get_profit(self, seller):
        return self.entry_value_init - self.get_total_out(seller)
    def get_profit_wc(self, seller):
        return self.entry_value_init - (self.get_total_out(seller) + self.open_out_init)

    class Meta:
        model = Seller
        fields = (
            'id','initialization_field','entry','out','total_out',
            'won_bonus','comission','profit','tickets',
            'open_out','open_tickets_count', 'profit_wc','entry_lan'
        )        


class SellerCashierListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = super().to_representation(data)
        self.child.out_value_end -= self.child.entry_end
        self.child.total_out_end -= self.child.entry_end
        profit = self.child.entry_value_end - self.child.total_out_end
        profit_wc = self.child.entry_value_end - (self.child.total_out_end + self.child.open_out_value_end)
        
        cashier_results = {
            'entry':self.child.entry_value_end,
            'out':self.child.out_value_end,
            'open_out': self.child.open_out_value_end,
            'won_bonus':self.child.won_bonus_end,
            'comission':self.child.comission_end,
            'total_out':self.child.total_out_end,
            'entry_total': self.child.entry_end,
            'profit': profit,
            'profit_wc': profit_wc,
            'open_tickets_count': self.child.open_tickets_count_end,
            'seller_data': data
        }
        
        return [cashier_results]


class SellersCashierSerializer(serializers.HyperlinkedModelSerializer):
    initalization_field = serializers.SerializerMethodField()
    comission = serializers.SerializerMethodField()
    entry = serializers.SerializerMethodField()
    out = serializers.SerializerMethodField()
    won_bonus = serializers.SerializerMethodField()
    total_out = serializers.SerializerMethodField()
    profit_wc = serializers.SerializerMethodField()
    profit = serializers.SerializerMethodField()
    open_tickets = serializers.SerializerMethodField()
    open_out = serializers.SerializerMethodField()
    entry_lan = serializers.SerializerMethodField()
    last_closed_cashier = serializers.SerializerMethodField()

    seller_comission_init = 0
    out_value_init = 0
    entry_value_init = 0
    total_out_init = 0
    won_bonus_init = 0
    open_out_value = 0
    open_tickets_count = 0
    entry_init = 0


    comission_end = 0
    out_value_end = 0
    entry_value_end = 0
    total_out_end = 0
    won_bonus_end = 0
    open_out_value_end = 0
    open_tickets_count_end = 0
    entry_end = 0

    def get_initalization_field(self, seller):
        self.seller_comission_init = 0
        self.out_value_init = 0
        self.entry_value_init = 0
        self.total_out_init = 0
        self.won_bonus_init = 0
        self.open_out_value = 0
        self.open_tickets_count = 0
        self.entry_init = 0

        tickets = Ticket.objects.filter(payment__status=2, payment__who_paid__pk=seller.pk).exclude(Q(status__in=[0,5,6]) | Q(available=False))
        open_tickets = Ticket.objects.filter(status=0, payment__status=2, payment__who_paid__pk=seller.pk).exclude(available=False)

        get_data = self.context['request'].GET
        start_creation_date = None
        end_creation_date = None

        if self.context.get('start_creation_date'):
            start_creation_date = self.context.get('start_creation_date')
            end_creation_date = self.context.get('end_creation_date')
        elif get_data:
            start_creation_date = get_data.get('start_creation_date')
            end_creation_date = get_data.get('end_creation_date')

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
        
        entry_init = seller.my_entries.filter(creation_date__date__gte=start_creation_date, creation_date__date__lte=end_creation_date)\
            .aggregate(Sum('value'))['value__sum']
        if entry_init:
            self.entry_init = entry_init   
        
        open_ticket_count = open_tickets.count()
        self.open_tickets_count = open_ticket_count
        self.open_tickets_count_end += open_ticket_count

        seller_comission = seller.comissions
        seller_key = {
            1: seller_comission.simple,
            2: seller_comission.double,
            3: seller_comission.triple,
            4: seller_comission.fourth,
            5: seller_comission.fifth,
            6: seller_comission.sixth
        }

        won_bonus_enabled = seller.my_store.my_configuration.bonus_won_ticket

        for ticket in tickets:
            # entry value
            self.entry_value_init += ticket.bet_value

            # seller comissions
            cotations_count = CotationCopy.objects.filter(active=True, ticket__pk=ticket.pk).count()
            self.seller_comission_init += seller_key.get(cotations_count, seller_comission.sixth_more) * ticket.bet_value / 100

            # calculating out value
            if ticket.status in [2,4]:
                self.out_value_init += ticket.reward.value

            # calculating won bonus
            if won_bonus_enabled:
                self.won_bonus_init += ticket.won_bonus()

        for ticket in open_tickets:
            self.entry_value_init += ticket.bet_value
            self.open_out_value += ticket.reward.value

            # seller comissions
            cotations_count = CotationCopy.objects.filter(active=True, ticket__pk=ticket.pk).count()
            self.seller_comission_init += seller_key.get(cotations_count, seller_comission.sixth_more) * ticket.bet_value / 100

        self.total_out_init = self.out_value_init + self.seller_comission_init
        self.open_out_value_end += self.open_out_value
        self.entry_value_end += self.entry_value_init
        self.won_bonus_end += self.won_bonus_init
        self.out_value_end += self.out_value_init
        self.total_out_end += self.total_out_init
        self.comission_end += self.seller_comission_init
        self.entry_end += self.entry_init

    def get_comission(self, obj):
        return self.seller_comission_init

    def get_entry(self, obj):
        return self.entry_value_init

    def get_out(self, obj):
        return self.out_value_init - self.entry_init

    def get_won_bonus(self, obj):
        return self.won_bonus_init

    def get_total_out(self, obj):
        return self.total_out_init - self.entry_init
    
    def get_profit_wc(self, obj):
        return self.entry_value_init - (self.get_total_out(obj) + self.open_out_value)

    def get_profit(self, obj):
        return self.entry_value_init - self.get_total_out(obj)

    def get_open_tickets(self, obj):
        return self.open_tickets_count
    
    def get_open_entry(self, obj):
        return self.open_entry_value

    def get_open_out(self, obj):
        return self.open_out_value

    def get_open_comission(self, obj):
        return self.open_comission_init

    def get_entry_lan(self, obj):
        return self.entry_init
    
    def get_last_closed_cashier(self, seller):
        from history.models import CashierCloseSeller
        closed_cashier = CashierCloseSeller.objects.filter(seller=seller).order_by('-date').first()

        if closed_cashier:
            return {
                'id': closed_cashier.pk,
                'date': closed_cashier.date.strftime("%d/%m/%Y %H:%M:%S")
            }
        else:
            return {
                'id': None,
                'date': 'Nenhum registro'
            }

    class Meta:
        model = Seller
        list_serializer_class = SellerCashierListSerializer
        fields = (
            'id','initalization_field','username','comission',
            'entry','won_bonus','out','total_out','profit', 'open_tickets', 
            'open_out', 'last_closed_cashier','profit_wc','entry_lan'
        )


class ManagerCashierListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = super().to_representation(data)

        cashier_results = {
            'entry':self.child.entry_value_end,
            'out':self.child.out_value_end,
            'open_out': self.child.open_out_end,
            'won_bonus':self.child.won_bonus_end,
            'managers_comission':self.child.manager_comission_end,
            'sellers_comission':self.child.seller_comission_end,
            'total_out':self.child.total_out_end,
            'open_tickets_count': self.child.open_tickets_count_end,
            'profit': self.child.entry_value_end - (self.child.total_out_end),
            'profit_wc': self.child.entry_value_end - (self.child.total_out_end + self.child.open_out_end),
            'manager_data':data
        }
        return [cashier_results]


class ManagersCashierSerializer(serializers.HyperlinkedModelSerializer):
    initalization_field = serializers.SerializerMethodField()
    seller_comission = serializers.SerializerMethodField()
    manager_comission = serializers.SerializerMethodField()
    entry = serializers.SerializerMethodField()
    out = serializers.SerializerMethodField()
    open_out = serializers.SerializerMethodField()
    won_bonus = serializers.SerializerMethodField()
    total_out = serializers.SerializerMethodField()
    profit = serializers.SerializerMethodField()
    profit_wc = serializers.SerializerMethodField()
    open_tickets = serializers.SerializerMethodField()
    last_closed_cashier = serializers.SerializerMethodField()

    manager_comission_init = 0
    seller_comission_init = 0
    out_value_init = 0
    entry_value_init = 0
    total_out_init = 0
    won_bonus_init = 0
    open_out_init = 0
    open_tickets_count = 0

    manager_comission_end = 0
    seller_comission_end = 0
    out_value_end = 0
    entry_value_end = 0
    total_out_end = 0
    won_bonus_end = 0
    open_out_end = 0
    open_tickets_count_end = 0

    def get_initalization_field(self, manager):
        self.manager_comission_init = 0
        self.seller_comission_init = 0
        self.open_tickets_count = 0
        self.out_value_init = 0
        self.entry_value_init = 0
        self.total_out_init = 0
        self.won_bonus_init = 0
        self.open_out_init = 0

        manager_comission = manager.comissions

        manager_key = {
            1:manager_comission.simple,
            2:manager_comission.double,
            3:manager_comission.triple,
            4:manager_comission.fourth,
            5:manager_comission.fifth,
            6:manager_comission.sixth
        }
        won_bonus_enabled = manager.my_store.my_configuration.bonus_won_ticket

        sellers = Seller.objects.filter(my_manager__pk=manager.pk).exclude(is_active=False)

        for seller in sellers:
            tickets = Ticket.objects.filter(payment__status=2, payment__who_paid__pk=seller.pk).exclude(Q(status__in=[0,5,6]) | Q(available=False))
            open_tickets = Ticket.objects.filter(status=0, payment__status=2, payment__who_paid__pk=seller.pk).exclude(available=False)

            get_data = self.context['request'].GET
            start_creation_date = None
            end_creation_date = None

            if self.context.get('start_creation_date'):
                start_creation_date = self.context.get('start_creation_date')
                end_creation_date = self.context.get('end_creation_date')
            elif get_data:
                start_creation_date = get_data.get('start_creation_date')
                end_creation_date = get_data.get('end_creation_date')

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

            open_ticket_count = open_tickets.count()
            self.open_tickets_count += open_ticket_count

            seller_comission = seller.comissions

            seller_key = {
                1:seller_comission.simple,
                2:seller_comission.double,
                3:seller_comission.triple,
                4:seller_comission.fourth,
                5:seller_comission.fifth,
                6:seller_comission.sixth
            }

            for ticket in tickets:
                cotations_count = CotationCopy.objects.filter(active=True, ticket__pk=ticket.pk).count()
                # manager comissions
                self.manager_comission_init += manager_key.get(cotations_count, manager_comission.sixth_more) * ticket.bet_value / 100

                # seller comissions
                self.seller_comission_init += seller_key.get(cotations_count, seller_comission.sixth_more) * ticket.bet_value / 100

                # entry value
                self.entry_value_init += ticket.bet_value

                # calculating out value
                if ticket.status in [2,4]:
                    self.out_value_init += ticket.reward.value

                # calculating won bonus
                if won_bonus_enabled:
                    self.won_bonus_init += ticket.won_bonus()

            for ticket in open_tickets:
                cotations_count = CotationCopy.objects.filter(active=True, ticket__pk=ticket.pk).count()
                # manager comissions
                self.manager_comission_init += manager_key.get(cotations_count, manager_comission.sixth_more) * ticket.bet_value / 100

                # seller comissions
                self.seller_comission_init += seller_key.get(cotations_count, seller_comission.sixth_more) * ticket.bet_value / 100

                # entry value
                self.entry_value_init += ticket.bet_value

                # calculating out value
                self.open_out_init += ticket.reward.value

                # calculating won bonus
                if won_bonus_enabled:
                    self.won_bonus_init += ticket.won_bonus()

            # defining total out
            self.total_out_init = self.out_value_init + self.seller_comission_init + self.manager_comission_init
        
        self.open_tickets_count_end += self.open_tickets_count
        self.entry_value_end += self.entry_value_init
        self.won_bonus_end += self.won_bonus_init
        self.out_value_end += self.out_value_init
        self.total_out_end += self.total_out_init
        self.manager_comission_end += self.manager_comission_init
        self.seller_comission_end += self.seller_comission_init
        self.open_out_end += self.open_out_init



    def get_entry(self, obj):
        return self.entry_value_init

    def get_manager_comission(self, obj):
        return self.manager_comission_init

    def get_out(self, obj):
        return self.out_value_init
    
    def get_won_bonus(self, obj):
        return self.won_bonus_init

    def get_total_out(self, obj):
        return self.total_out_init

    def get_seller_comission(self, obj):
        return self.seller_comission_init

    def get_open_tickets(self, obj):
        return self.open_tickets_count

    def get_open_out(self, obj):
        return self.open_out_init

    def get_profit(self, obj):
        return self.entry_value_init - self.total_out_init

    def get_profit_wc(self, obj):
        return self.entry_value_init - (self.total_out_init + self.open_out_init)

    def get_last_closed_cashier(self, manager):
        from history.models import CashierCloseManager
        closed_cashier = CashierCloseManager.objects.filter(manager=manager).order_by('-date').first()

        if closed_cashier:
            return {
                'id': closed_cashier.pk,
                'date': closed_cashier.date.strftime("%d/%m/%Y %H:%M:%S")
            }
        else:
            return {
                'id': None,
                'date': 'Nenhum registro'
            }
    
    class Meta:
        model = Manager
        list_serializer_class = ManagerCashierListSerializer
        fields = ('id','initalization_field', 'username',
            'manager_comission','seller_comission','entry','open_tickets',
            'won_bonus','out','open_out','total_out','profit','profit_wc',
            'last_closed_cashier'
        )


class ManagerSpecificCashierListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = super().to_representation(data)
        cashier_results = {
            'entry':self.child.entry_value_end,
            'out':self.child.out_value_end,
            'open_out':self.child.open_out_value_end,
            'open_tickets':self.child.open_tickets_count_end,
            'won_bonus':self.child.won_bonus_end,
            'manager_comission':self.child.manager_comission_end,
            'seller_comission':self.child.seller_comission_end,
            'total_out':self.child.total_out_end,
            'profit_wc': self.child.entry_value_end - (self.child.total_out_end + self.child.open_out_value_end),
            'profit': self.child.entry_value_end - self.child.total_out_end,
            'seller_data':data
        }
        return [cashier_results]


class ManagerSpecificCashierSerializer(serializers.HyperlinkedModelSerializer):
    initalization_field = serializers.SerializerMethodField()
    manager_comission = serializers.SerializerMethodField()
    seller_comission = serializers.SerializerMethodField()
    entry = serializers.SerializerMethodField()
    out = serializers.SerializerMethodField()
    open_out = serializers.SerializerMethodField()
    profit = serializers.SerializerMethodField()
    profit_wc = serializers.SerializerMethodField()
    won_bonus = serializers.SerializerMethodField()
    total_out = serializers.SerializerMethodField()
    open_tickets = serializers.SerializerMethodField()

    manager_comission_init = 0
    seller_comission_init = 0
    out_value_init = 0
    open_out_init = 0
    won_bonus_init = 0
    total_out_init = 0
    entry_value_init = 0
    open_tickets_count_init = 0

    manager_comission_end = 0
    seller_comission_end = 0
    out_value_end = 0
    open_out_value_end = 0
    won_bonus_end = 0
    total_out_end = 0
    entry_value_end = 0
    open_tickets_count_end = 0


    def get_initalization_field(self, seller):
        self.manager_comission_init = 0
        self.seller_comission_init = 0
        self.out_value_init = 0
        self.open_out_init = 0
        self.won_bonus_init = 0
        self.total_out_init = 0
        self.entry_value_init = 0
        self.open_tickets_count_init = 0

        manager_comission = seller.my_manager.comissions
        
        manager_key = {
            1:manager_comission.simple,
            2:manager_comission.double,
            3:manager_comission.triple,
            4:manager_comission.fourth,
            5:manager_comission.fifth,
            6:manager_comission.sixth
        }

        tickets = Ticket.objects.filter(payment__status=2, payment__who_paid__pk=seller.pk).exclude(Q(status__in=[0,5,6]) | Q(available=False))
        open_tickets = Ticket.objects.filter(status=0, payment__status=2, payment__who_paid__pk=seller.pk).exclude(available=False)

        get_data = self.context['request'].GET
        start_creation_date = None
        end_creation_date = None

        if get_data:
            start_creation_date = get_data.get('start_creation_date')
            end_creation_date = get_data.get('end_creation_date')

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
        
        open_ticket_count = open_tickets.count()
        self.open_tickets_count_init = open_ticket_count
        self.open_tickets_count_end += open_ticket_count

        seller_comission = seller.comissions
        seller_key = {
            1: seller_comission.simple,
            2: seller_comission.double,
            3: seller_comission.triple,
            4: seller_comission.fourth,
            5: seller_comission.fifth,
            6: seller_comission.sixth
        }

        won_bonus_enabled = seller.my_store.my_configuration.bonus_won_ticket

        for ticket in tickets:
            # entry value
            self.entry_value_init += ticket.bet_value

            # seller comissions
            cotations_count = CotationCopy.objects.filter(active=True, ticket__pk=ticket.pk).count()
            self.seller_comission_init += seller_key.get(cotations_count, seller_comission.sixth_more) * ticket.bet_value / 100
            self.manager_comission_init += manager_key.get(cotations_count, manager_comission.sixth_more) * ticket.bet_value / 100

            # calculating out value
            if ticket.status in [2,4]:
                self.out_value_init += ticket.reward.value

            # calculating won bonus
            if won_bonus_enabled:
                self.won_bonus_init += ticket.won_bonus()

        for ticket in open_tickets:
            self.entry_value_init += ticket.bet_value
            self.open_out_init += ticket.reward.value

            # seller comissions
            cotations_count = CotationCopy.objects.filter(active=True, ticket__pk=ticket.pk).count()
            self.seller_comission_init += seller_key.get(cotations_count, seller_comission.sixth_more) * ticket.bet_value / 100
            self.manager_comission_init += manager_key.get(cotations_count, manager_comission.sixth_more) * ticket.bet_value / 100

        self.total_out_init = self.out_value_init + self.seller_comission_init + self.manager_comission_init
        self.open_out_value_end += self.open_out_init
        self.entry_value_end += self.entry_value_init
        self.won_bonus_end += self.won_bonus_init
        self.out_value_end += self.out_value_init
        self.total_out_end += self.total_out_init
        self.seller_comission_end += self.seller_comission_init
        self.manager_comission_end += self.manager_comission_init

    def get_manager_comission(self, obj):
        return self.manager_comission_init

    def get_seller_comission(self, obj):
        return self.seller_comission_init

    def get_entry(self, obj):
        return self.entry_value_init

    def get_out(self, obj):
        return self.out_value_init

    def get_open_out(self, obj):
        return self.open_out_init

    def get_won_bonus(self, obj):
        return self.won_bonus_init

    def get_total_out(self, obj):
        return self.total_out_init

    def get_open_tickets(self, obj):
        return self.open_tickets_count_init

    def get_profit(self, obj):
        return self.entry_value_init - self.total_out_init

    def get_profit_wc(self, obj):
        return self.entry_value_init - (self.total_out_init + self.open_out_init)

    class Meta:
        model = Seller
        list_serializer_class = ManagerSpecificCashierListSerializer
        fields = ('id','initalization_field','username','manager_comission',
        'seller_comission','entry','won_bonus','out','total_out',
        'profit','profit_wc','open_out','open_tickets'
    )
