import graphene
from graphene.types import Int, Boolean
from history.models import CashierCloseManager
from schemas.base import BaseMutation
from utils.utils import get_last_monay_as_date
from user.models import Manager
from django.db import transaction
from utils.utils import tzlocal

class ManagerMutations(BaseMutation):
    queryset = Manager.objects.filter(is_active=True)

    def get_managers(self):
        return self.get_queryset()

    def get_manager(self):
        return self.get_queryset().get(pk=self.kwargs.get('manager_id'))

    @transaction.atomic
    def close_manager_cashier(self):
        start_date = datetime.strptime(self.kwargs.get('start_date'), '%d/%m/%Y').strftime('%Y-%m-%d') if self.kwargs.get('start_date') else get_last_monay_as_date()
        end_date = datetime.strptime(self.kwargs.get('end_date'), '%d/%m/%Y').strftime('%Y-%m-%d') if self.kwargs.get('end_date') else tzlocal.now()

        if self.kwargs.get('close_all'):
            managers = self.get_managers()
            for manager in managers:
                CashierCloseManager.objects.create(
                    register_by=self.request.user,
                    manager=manager,
                    start_date=start_date,
                    end_date=end_date,
                    store=self.request.user.my_store
                )
        else:
            CashierCloseManager.objects.create(
                register_by=self.request.user,
                manager=self.get_manager(),
                start_date=start_date,
                end_date=end_date,
                store=self.request.user.my_store
            )
        return True
    