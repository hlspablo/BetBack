from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from filters.mixins import FiltersMixin
from user.models import CustomUser
from user.permissions import IsAdmin
from utils.paginations import EntryPagination
from utils.models import Entry
from utils.serializers.entry import EntrySerializer
from utils.permissions import EntryPermission, CanAddOrRemoveEntryPermission
import json, datetime
from utils.models import Entry
from user.models import Seller

class EntryView(FiltersMixin, ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    pagination_class = EntryPagination
    permission_classes = [EntryPermission]

    filter_mappings = {
        'user':'user__pk',
        'start_creation_date': 'creation_date__date__gte',
        'end_creation_date': 'creation_date__date__lte',
    }

    filter_value_transformations = {
        'start_creation_date': lambda val: datetime.datetime.strptime(val, '%d/%m/%Y').strftime('%Y-%m-%d'),
        'end_creation_date': lambda val: datetime.datetime.strptime(val, '%d/%m/%Y').strftime('%Y-%m-%d'),        
    }

    def get_queryset(self):
        if self.request.user.user_type == 2:
            return Entry.objects.filter(user=self.request.user, store=self.request.user.my_store).order_by('-creation_date')
        if self.request.user.user_type == 3:
            return Entry.objects.filter(creator_user=self.request.user, store=self.request.user.my_store).order_by('-creation_date')
        if self.request.user.user_type == 4:
            return Entry.objects.filter(store=self.request.user.my_store).order_by('-creation_date')
        return Entry.objects.none()
        

    @action(methods=['post'], detail=False, permission_classes=[CanAddOrRemoveEntryPermission])
    def add_entry(self, request, pk=None):
        data = json.loads(request.POST.get('data'))
        seller_id = data.get('seller_id')
        entry_value = data.get('entry_value')
        
        Entry.objects.create(
            creator_user=self.request.user,
            user=Seller.objects.get(pk=seller_id),
            value=entry_value,
            store=self.request.user.my_store
        )

        return Response({'success':True, 'message': 'Lançamento Adicionado.'})

    @action(methods=['post'], detail=False, permission_classes=[CanAddOrRemoveEntryPermission])
    def remove_entry(self, request, pk=None):        
        data = json.loads(request.POST.get('data'))
        entry_id = data.get('entry_id')
        entry = Entry.objects.filter(pk=entry_id)
        if entry.first().store == self.request.user.my_store:
            entry.delete()
        return Response({'success':True, 'message': 'Lançamento Deletado'})