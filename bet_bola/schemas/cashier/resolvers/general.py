from user.models import Seller, Manager
from schemas.base import BaseResolver
from .seller import SellerCashierResolver
from decimal import Decimal as dec


class GeneralCashierResolver(BaseResolver):
    queryset = Manager.objects.filter(is_active=True)

    def __init__(self, request, **kwargs):
        super().__init__(request, **kwargs)
        self.seller_resolver = SellerCashierResolver(request, **kwargs)

    def get_general_cashier(self):
        sellers_cashier = self.seller_resolver.get_sellers_cashier(with_managers_comission=False)
        return sellers_cashier
