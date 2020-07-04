import graphene
from graphene import Field
from graphene.types import String, Int
from .types import (
    SellerCashierType, SellersCashierType, 
    ManagerCashierType, ManagerOwnerCashierType,
    ManagersCashierType, GeneralCashierType,
    EntryTypeTotal
)
from .resolvers.seller import SellerCashierResolver
from .resolvers.manager import ManagerCashierResolver
from .resolvers.general import GeneralCashierResolver
from .resolvers.entry import get_entries

class CashierQuery(graphene.ObjectType):
    get_entries = Field(EntryTypeTotal, seller_username=String(), start_date=String(), end_date=String())
    seller_cashier = Field(
        SellerCashierType, seller_id=Int(required=True), start_date=String(), end_date=String()
    )
    sellers_cashier = Field(
        SellersCashierType, start_date=String(), end_date=String()
    )
    manager_cashier = Field(
        ManagerCashierType, manager_id=Int(required=True), start_date=String(), end_date=String()
    )
    manager_owner_cashier = Field(
        ManagerOwnerCashierType, manager_id=Int(required=True), start_date=String(), end_date=String()
    )
    managers_cashier = Field(
        ManagersCashierType, start_date=String(), end_date=String()
    )
    general_cashier = Field(
        GeneralCashierType, start_date=String(), end_date=String()
    )

    def resolve_get_entries(self, info, **kwargs):
        return get_entries(info.context, **kwargs)

    def resolve_seller_cashier(self, info, **kwargs):
        resolver = SellerCashierResolver(info.context, **kwargs)
        return resolver.get_seller_cashier()

    def resolve_sellers_cashier(self, info, **kwargs):
        resolver = SellerCashierResolver(info.context, **kwargs)
        return resolver.get_sellers_cashier()

    def resolve_manager_cashier(self, info, **kwargs):
        resolver = ManagerCashierResolver(info.context, **kwargs)
        return resolver.get_manager_cashier()

    def resolve_managers_cashier(self, info, **kwargs):
        resolver = ManagerCashierResolver(info.context, **kwargs)
        return resolver.get_managers_cashier()

    def resolve_manager_owner_cashier(self, info, **kwargs):
        resolver = ManagerCashierResolver(info.context, **kwargs)
        return resolver.get_manager_owner_cashier()

    def resolve_general_cashier(self, info, **kwargs):
        resolver = GeneralCashierResolver(info.context, **kwargs)
        return resolver.get_general_cashier()


