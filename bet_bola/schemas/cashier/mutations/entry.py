from utils.models import Entry
from user.models import Seller
from django.db import transaction

@transaction.atomic()
def add_entry(request, **kwargs):
    seller_id = kwargs.get('seller_id')
    value = kwargs.get('value')

    entry = Entry.objects.create(
        creator_user=request.user,
        user=Seller.objects.get(pk=seller_id),
        value=value,
        store=request.user.my_store
    )

    return {
        'success': True
    }

@transaction.atomic()
def delete_entry(request, **kwargs):
    entry_id = kwargs.get('entry_id')

    entry = Entry.objects.get(pk=entry_id)
    entry.delete()
    return {
        'success': True
    }