import graphene
from graphene.types import Int, Boolean
from history.models import CashierCloseSeller
from schemas.base import BaseMutation

class SellerMutations(BaseMutation):
    
    def close_seller_cashier(self):
        print(self.kwargs)
        # #get and convert to datetime
        # start_date = datetime.datetime.strptime(data.get('start_creation_date'), '%d/%m/%Y').strftime('%Y-%m-%d')
        # end_date = datetime.datetime.strptime(data.get('end_creation_date'), '%d/%m/%Y').strftime('%Y-%m-%d')

        # if close_all:
        #     sellers = self.get_queryset()
        #     for seller in sellers:
        #         CashierCloseSeller.objects.create(
        #             register_by=request.user,
        #             seller=seller,
        #             start_date=start_date,
        #             end_date=end_date,
        #             store=request.user.my_store
        #         )
        # else:
        #     CashierCloseSeller.objects.create(
        #         register_by=request.user,
        #         seller=Seller.objects.get(pk=seller_id),
        #         start_date=start_date,
        #         end_date=end_date,
        #         store=request.user.my_store
        #     )

        # return False
    