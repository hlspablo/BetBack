from core.paginations import PageNumberPagination
from rest_framework.response import Response
from decimal import Decimal
from utils.models import Entry

class EntryPagination(PageNumberPagination):
    page_size = 50

    def get_paginated_response(self, data):        
        entry_total = 0

        if self.request.user.user_type == 3:
            users = [{"id":entry_data.user.pk, "username":entry_data.user.username} for entry_data in Entry.objects.filter(creator_user=self.request.user).distinct('user')]
        else:
            users = [{"id":entry_data.user.pk, "username":entry_data.user.username} for entry_data in Entry.objects.all().distinct('user')]

        for entry in data:
            entry_total += float(entry['value'])

        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,            
            'total_entry': entry_total,
            'users': users,
            'data': data
        })
