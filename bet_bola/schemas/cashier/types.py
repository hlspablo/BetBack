from graphene_django import DjangoObjectType
from core.models import Game
from graphene import ObjectType
from graphene.types import String, Decimal, Float, Int, DateTime, Field, List, Boolean

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

class ManagerCashierType(ObjectType):
    username = String()
    entry = Decimal()
    incoming = Decimal()
    seller_comission = Decimal()
    manager_comission = Decimal()
    outgoing = Decimal()
    outgoing_total = Decimal()
    open_outgoing = Decimal()
    bonus_of_won = Decimal()
    open_tickets_count = Int()
    based_on_profit = Boolean()
    balance = Decimal()
    profit = Decimal()
    profit_wost_case = Decimal()
    tickets = List(TicketType)

class ManagerOwnerCashierType(ObjectType):
    username = String()
    entry = Decimal()
    incoming = Decimal()
    seller_comission = Decimal()
    manager_comission = Decimal()
    outgoing = Decimal()
    outgoing_total = Decimal()
    open_outgoing = Decimal()
    bonus_of_won = Decimal()
    open_tickets_count = Int()
    based_on_profit = Boolean()
    balance = Decimal()
    profit = Decimal()
    profit_wost_case = Decimal()
    sellers = List(SellerCashierTypeB)

class ManagersCashierType(ObjectType):
    entry_sum_total = String()
    incoming_sum_total = Decimal()
    seller_comission_sum_total = Decimal()
    manager_comission_sum_total = Decimal()
    outgoing_sum_total = Decimal()
    outgoing_total_sum_total = Decimal()
    bonus_of_won_sum_total = Decimal()
    open_outgoing_sum_total = Decimal()
    open_tickets_count_sum_total = Int()
    profit_sum_total = Decimal()
    profit_wost_case_sum_total = Decimal()
    managers = List(ManagerCashierType)


class GeneralCashierType(SellersCashierType):
    managers_comission = Decimal()