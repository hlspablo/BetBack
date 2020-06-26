from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status
from filters.mixins import FiltersMixin
from ticket.models import Ticket, Reward, Payment
from cashier.serializers.cashier import SellersCashierSerializer, ManagersCashierSerializer
from history.paginations import SellerCashierPagination, ManagerCashierPagination, SellersCashierPagination, ManagersCashierPagination
from ticket.paginations import TicketPagination
from ticket.serializers.ticket import TicketSerializer, CreateTicketSerializer
from user.models import Seller, Manager
from utils.models import Entry
from utils import timezone as tzlocal
from django.shortcuts import redirect
from config import settings
import json, datetime, decimal
import time

class GeneralCashier(APIView):

    def get(self, request):
        user = self.request.user
        start_creation_date = self.request.GET.get('start_creation_date')
        end_creation_date = self.request.GET.get('end_creation_date')

        managers = Manager.objects.filter(my_store=user.my_store).exclude(is_active=False)
        sellers = Seller.objects.filter(my_store=user.my_store).exclude(is_active=False)
        

        ctx = { 
            'request': self.request,
            'start_creation_date': start_creation_date,
            'end_creation_date': end_creation_date
        }

        manager_serializer = ManagersCashierSerializer(managers, many=True, context=ctx).data[0]
        seller_serializer = SellersCashierSerializer(sellers, many=True, context=ctx).data[0]

        data = {
            'total_entry': seller_serializer['entry'],
            'entry_lan': seller_serializer['entry_total'],
            'total_reward_out': seller_serializer[ 'out'],
            'total_seller_comission': seller_serializer['comission'],

            'total_manager_comission': manager_serializer['managers_comission'],
            
            'total_won_bonus': seller_serializer['won_bonus'],
            'total_out': seller_serializer['total_out'] + manager_serializer['managers_comission'],
            'total_open_out': seller_serializer['open_out'],
            'total_open_tickets': seller_serializer['open_tickets_count'],
            'profit': seller_serializer['profit'] - manager_serializer['managers_comission'],
            'profit_wc': seller_serializer['profit_wc'] - manager_serializer['managers_comission']
        }

        return Response(data)
