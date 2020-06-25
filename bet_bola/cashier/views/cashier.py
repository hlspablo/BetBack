from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from filters.mixins import FiltersMixin
from ticket.models import Ticket
from cashier.serializers.cashier import (
    SellerCashierSerializer, SellersCashierSerializer, 
    ManagerCashierSerializer, ManagersCashierSerializer, ManagerSpecificCashierSerializer
)
from history.paginations import (
    SellerCashierPagination, ManagerCashierPagination, 
    SellersCashierPagination, ManagersCashierPagination, ManagerSpecificCashierPagination
)
from user.models import Seller, Manager, CustomUser
from history.models import ManagerCashierHistory, SellerCashierHistory
from history.permissions import (
    CashierCloseManagerPermission, ManagerCashierPermission, 
    CashierCloseSellerPermission, SellerCashierPermission
)
from user.permissions import IsManager
import json, datetime, decimal
from django.shortcuts import redirect
from utils.utils import get_last_monay_as_date
from utils.utils import tzlocal


class SellersCashierView(FiltersMixin, ModelViewSet):
    queryset = Seller.objects.exclude(is_active=False)
    serializer_class = SellersCashierSerializer
    permission_classes = [SellerCashierPermission]
    pagination_class = SellersCashierPagination

    filter_mappings = {        
        'managed_by': 'my_manager__pk',
    }

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 2:
            return self.queryset.filter(pk=user.pk, my_store=user.my_store)
        elif user.user_type == 3:
            return self.queryset.filter(my_manager__pk=user.pk, my_store=user.my_store)
        return self.queryset.filter(my_store=user.my_store)

    @action(methods=['post'], detail=False, permission_classes = [CashierCloseSellerPermission])
    def close_seller(self, request, pk=None):
        from history.models import CashierCloseSeller

        data = json.loads(request.POST.get('data'))
        seller_id = data.get('seller_id')
        close_all = data.get('close_all')

        
        start_date = datetime.datetime.strptime(data.get('start_creation_date'), '%d/%m/%Y').strftime('%Y-%m-%d')
        end_date = data.get('end_creation_date')
        
        if not end_date:
            end_date = tzlocal.now()
        else:
            end_date = datetime.datetime.strptime(data.get('end_creation_date'), '%d/%m/%Y').strftime('%Y-%m-%d')

        if close_all:
            sellers = self.get_queryset()

            for seller in sellers:
                CashierCloseSeller.objects.create(
                    register_by=request.user,
                    seller=seller,
                    start_date=start_date,
                    end_date=end_date,
                    store=request.user.my_store
                )
        else:
            CashierCloseSeller.objects.create(
                register_by=request.user,
                seller=Seller.objects.get(pk=seller_id),
                start_date=start_date,
                end_date=end_date,
                store=request.user.my_store
            )

        return Response({
            'success': True,
            'message': 'Prestação registrada com sucesso.'
        })      



class ManagersCashierView(FiltersMixin, ModelViewSet):
    queryset = Manager.objects.exclude(is_active=False)
    serializer_class = ManagersCashierSerializer
    permission_classes = [ManagerCashierPermission]
    pagination_class = ManagersCashierPagination


    def get_queryset(self):
        user = self.request.user
        if user.user_type == 3:
            return self.queryset.filter(pk=user.pk)
        return self.queryset.filter(my_store=user.my_store)

    
    @action(methods=['post'], detail=False, permission_classes = [CashierCloseManagerPermission])
    def close_manager(self, request, pk=None):
        from history.models import CashierCloseManager

        data = json.loads(request.POST.get('data'))
        manager_id = data.get('manager_id')
        close_all = data.get('close_all')

        start_date = datetime.datetime.strptime(data.get('start_creation_date'), '%d/%m/%Y').strftime('%Y-%m-%d')
        end_date = data.get('end_creation_date')
        
        if not end_date:
            end_date = tzlocal.now()
        else:
            end_date = datetime.datetime.strptime(data.get('end_creation_date'), '%d/%m/%Y').strftime('%Y-%m-%d')

        if close_all:
            managers = self.get_queryset()
            for manager in managers:
                CashierCloseManager.objects.create(
                    register_by=request.user,
                    manager=manager,
                    start_date=start_date,
                    end_date=end_date,
                    store=request.user.my_store
                )
        else:
            CashierCloseManager.objects.create(
                register_by=request.user,
                manager=Manager.objects.get(pk=manager_id),
                start_date=start_date,
                end_date=end_date,
                store=request.user.my_store
            )
        
        return Response({
            'success': True,
            'message': 'Prestação registrada com sucesso.'
        })   


class SellerCashierView(FiltersMixin, ModelViewSet):
    queryset = Seller.objects.exclude(is_active=False)
    serializer_class = SellerCashierSerializer
    permission_classes = [SellerCashierPermission]  
    pagination_class = SellerCashierPagination

    filter_mappings = {        
        'paid_by': 'pk',        
    }

    def get_queryset(self):
        seller = self.request.GET.get('paid_by')
        if seller:
            return self.queryset.filter(pk=seller)
        elif self.request.user.user_type == 2:
            return self.queryset.filter(pk=self.request.user.pk)
        return Seller.objects.none()
                

class ManagerCashierView(FiltersMixin, ModelViewSet):
    queryset = Manager.objects.exclude(is_active=False)
    serializer_class = ManagerCashierSerializer
    permission_classes = [ManagerCashierPermission]
    pagination_class = ManagerCashierPagination

    filter_mappings = {        
        'manager': 'pk',                
    }

    def get_queryset(self):        
        manager = self.request.GET.get('manager')        
        if manager:
            return self.queryset.filter(pk=manager)        
        elif self.request.user.user_type == 3:
            return self.queryset.filter(pk=self.request.user.pk)
        return Manager.objects.none()



class ManagerSpecificCashierView(FiltersMixin, ModelViewSet):
    queryset = Seller.objects.exclude(is_active=False) 
    serializer_class = ManagerSpecificCashierSerializer
    permission_classes = [IsManager]
    pagination_class = ManagerSpecificCashierPagination


    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(my_manager__pk=user.pk,my_store=user.my_store)
