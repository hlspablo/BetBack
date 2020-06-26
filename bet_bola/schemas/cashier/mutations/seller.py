import graphene
from graphene.types import Int, Boolean
from history.models import CashierCloseSeller
from schemas.base import BaseMutation
from utils.utils import get_last_monay_as_date
from user.models import Seller
from django.db import transaction
from utils.utils import tzlocal

class SellerMutations(BaseMutation):
    queryset = Seller.objects.filter(is_active=True)

    def get_sellers(self):
        return self.get_queryset()

    def get_seller(self):
        return self.get_queryset().get(pk=self.kwargs.get('seller_id'))

    @transaction.atomic
    def close_seller_cashier(self):
        start_date = datetime.strptime(self.kwargs.get('start_date'), '%d/%m/%Y').strftime('%Y-%m-%d') if self.kwargs.get('start_date') else get_last_monay_as_date()
        end_date = datetime.strptime(self.kwargs.get('end_date'), '%d/%m/%Y').strftime('%Y-%m-%d') if self.kwargs.get('end_date') else tzlocal.now()

        if self.kwargs.get('close_all'):
            sellers = self.get_sellers()
            for seller in sellers:
                CashierCloseSeller.objects.create(
                    register_by=self.request.user,
                    seller=seller,
                    start_date=start_date,
                    end_date=end_date,
                    store=self.request.user.my_store
                )
        else:
            CashierCloseSeller.objects.create(
                register_by=self.request.user,
                seller=self.get_seller(),
                start_date=start_date,
                end_date=end_date,
                store=self.request.user.my_store
            )

        return True
    