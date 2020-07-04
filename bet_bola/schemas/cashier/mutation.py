import graphene
from graphene import  Field
from .mutationTypes import (
    CloseSellerCashierType, 
    CloseManagerCashierType,
    AddEntryType,
    DeleteEntryType
)

class CashierMutation(graphene.ObjectType):
    close_seller_cashier = CloseSellerCashierType.Field()
    close_manager_cashier = CloseManagerCashierType.Field()
    add_entry = AddEntryType.Field()
    delete_entry = DeleteEntryType.Field()