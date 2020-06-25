from graphene_django import DjangoObjectType
from core.models import Game
from graphene import ObjectType
from graphene.types import String, Decimal, Float, Int, DateTime, Field, List

class TicketType(ObjectType):
    ticket_id = String()
    status = String()
    creation_date = String()
    comission = Decimal()
    cotations_count = Int()
    bonus_of_won = Decimal()
    reward = Decimal()
    bet_value = Decimal()

class SellerCashierType(ObjectType):
    username = String()
    incoming = Decimal()
    comission = Decimal()
    outgoing = Decimal()
    outgoing_total = Decimal()
    open_outgoing = Decimal()
    bonus_of_won = Decimal()
    open_tickets_count = Int()
    entry = Decimal()
    profit_wost_case = Decimal()
    profit = Decimal()
    tickets = List(TicketType)


class SellerCashierTypeB(SellerCashierType):
    last_closed_cashier = String()

class SellersCashierType(ObjectType):
    incoming_total = Decimal()
    comission_total = Decimal()
    outgoing_sum_total = Decimal()
    outgoing_total_sum_total = Decimal()
    open_outgoing_total = Decimal()
    bonus_of_won_total = Decimal()
    open_tickets_count_total = Int()
    entry_total = Decimal()
    profit_wost_case_total = Decimal()
    profit_total = Decimal()
    sellers = List(SellerCashierTypeB)