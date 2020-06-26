import graphene
from graphene import  Field
from .mutationTypes import CloseSellerCashierType

class CashierMutation(graphene.ObjectType):
    close_seller_cashier = CloseSellerCashierType.Field()