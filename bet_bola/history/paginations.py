from django.core.paginator import Paginator
from django.utils.functional import cached_property
from django.db.models import Q, Count
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Count
from user.models import CustomUser, Seller, Manager
from ticket.models import Ticket,Payment
from decimal import Decimal
from math import ceil


class TicketCancelationPagination(PageNumberPagination):
    page_size = 50

    def get_paginated_response(self, data):    
        paid_by_list = [{'id':user.pk,'username':user.username} for user in CustomUser.objects.filter(my_canceled_tickets_who_i_paid__isnull=False, my_store=self.request.user.my_store).distinct()]
        cancelled_by_list = [{'id':user.pk,'username':user.username} for user in CustomUser.objects.filter(my_canceled_tickets__isnull=False, my_store=self.request.user.my_store).distinct()]
   
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,            
            'paid_by_list': paid_by_list,
            'cancelled_by_list': cancelled_by_list,
            'results': data
        })


class TicketValidationPagination(PageNumberPagination):
    page_size = 50

    def get_paginated_response(self, data):
        paid_by_list = [{'id':user.pk,'username':user.username} for user in CustomUser.objects.filter(my_ticket_validations__isnull=False, my_store=self.request.user.my_store).distinct()]
        
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,            
            'paid_by_list': paid_by_list,            
            'results': data
        })


class SellerCashierHistoryPagination(PageNumberPagination):
    page_size = 50

    def get_paginated_response(self, data):        
        register_by_list = [{'id':user.pk,'username':user.username} for user in CustomUser.objects.filter(sellercashierhistory__isnull=False, my_store=self.request.user.my_store).distinct()]        
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,            
            'register_by_list': register_by_list,              
            'results': data
        })


class ManagerCashierHistoryPagination(PageNumberPagination):
    page_size = 50 

    def get_paginated_response(self, data):        
        register_by_list = [{'id':user.pk,'username':user.username} for user in CustomUser.objects.filter(sellercashierhistory__isnull=False, my_store=self.request.user.my_store).distinct()]        

        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,            
            'register_by_list': register_by_list,              
            'results': data
        })


class CreditTransactionsPagination(PageNumberPagination):
    page_size = 50

    def get_paginated_response(self, data):  
        creditor_list = [{'id':user.pk,'username':user.username} for user in CustomUser.objects.filter(pk=self.request.user.pk).distinct()]
        if self.request.user.user_type == 3:
            seller_list = [{'id':user.pk,'username':user.username} for user in CustomUser.objects.filter(credit_transactions__isnull=False, seller__my_manager__pk=self.request.user.pk, my_store=self.request.user.my_store).distinct()]
        else:
            seller_list = [{'id':user.pk,'username':user.username} for user in CustomUser.objects.filter(credit_transactions__isnull=False, my_store=self.request.user.my_store).distinct()]
            
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,                                    
            'results': data,
            'creditor_list':creditor_list,
            'seller_list':seller_list
        })


class SellersCashierPagination(PageNumberPagination):
    page_size = 9999

    def get_paginated_response(self, data):
        sellers = None

        if self.request.user.user_type == 4:        
            sellers = [{'id':seller.pk,'username':seller.username} for seller in Seller.objects.filter(my_store=self.request.user.my_store).exclude(is_active=False)]
        elif self.request.user.user_type == 3:            
            sellers = [{'id':user.pk,'username':user.username} for user in self.request.user.manager.manager_assoc.filter(my_store=self.request.user.my_store).exclude(is_active=False)]
        
        managers = [{'id':user.pk,'username':user.username} for user in Manager.objects.filter(my_store=self.request.user.my_store).exclude(is_active=False)]

        
        data = data.pop()
        
        return Response({
            'managers': managers,
            'sellers': sellers,
            'data': data
        })


class ManagersCashierPagination(PageNumberPagination):
    page_size = 9999

    def get_paginated_response(self, data):        
        managers = [{"id":manager.pk,"username":manager.username} for manager in Manager.objects.filter(my_store=self.request.user.my_store).exclude(is_active=False)]
        data = data.pop()
                
        return Response({
            'managers': managers,
            'data': data
        })


class SellerCashierPagination(PageNumberPagination):
    page_size = 9999

    def get_paginated_response(self, data):
        sellers = []               
        if self.request.user.user_type == 4:        
            sellers = [{'id':seller.pk,'username':seller.username} for seller in Seller.objects.filter(my_store=self.request.user.my_store).exclude(is_active=False)]
        elif self.request.user.user_type == 3:
            sellers = [{'id':seller.pk,'username':seller.username} for seller in self.request.user.manager.manager_assoc.filter(my_store=self.request.user.my_store).exclude(is_active=False)]

        return Response({          
            'sellers': sellers,
            'data': data
        })


class ManagerCashierPagination(PageNumberPagination):
    page_size = 9999

    def get_paginated_response(self, data):                
        managers = [{"id":manager.pk,"username":manager.username} for manager in Manager.objects.filter(my_store=self.request.user.my_store).exclude(is_active=False)]

        return Response({                       
            'managers': managers,            
            'data': data
        })


class ManagerSpecificCashierPagination(PageNumberPagination):
    page_size = 9999

    def get_paginated_response(self, data):
        return Response({
            'data': data[0]
        })
