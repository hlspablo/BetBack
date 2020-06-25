from graphene_django import DjangoObjectType
from core.models import Game
from graphene import ObjectType
from graphene.types import String, Decimal, Float, Int, DateTime, Field, List

class TicketType(ObjectType):
    ticket_id = String()
    status = String()
    comission = Decimal()
    bonus_of_won = Decimal()
    bet_value = Decimal()
    cotations_count = Int()
    reward = Decimal()
    creation_date = String()

class SellerCashierType(ObjectType):
    entry = Decimal()
    incoming = Decimal()
    comission = Decimal()
    outgoing = Decimal()
    bonus_of_won = Decimal()
    tickets = List(TicketType)
    open_outgoing = Decimal()
    open_tickets_count = Int()
    outgoing_total = Decimal()
    profit = Decimal()
    profit_wost_case = Decimal()

class SellerCashierTypeB(SellerCashierType):
    last_closed_cashier = String()

class SellersCashierType(ObjectType):
    entry_total = Decimal()
    incoming_total = Decimal()
    comission_total = Decimal()
    bonus_of_won_total = Decimal()
    open_outgoing_total = Decimal()
    open_tickets_count_total = Int()
    outgoing_total_total = Decimal()
    profit_total = Decimal()
    profit_wost_case_total = Decimal()
    sellers = List(SellerCashierTypeB)