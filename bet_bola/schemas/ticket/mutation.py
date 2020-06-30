import graphene
from graphene import  Field
#from .mutationTypes import CloseSellerCashierType, CloseManagerCashierType

class CashierMutation(graphene.ObjectType):
    #close_seller_cashier = CloseSellerCashierType.Field() TODO