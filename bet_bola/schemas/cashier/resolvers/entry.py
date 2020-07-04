from utils.models import Entry
from django.db.models import Sum
from utils.utils import get_last_monay_as_date
from utils import timezone as tzlocal
from datetime import datetime

def get_entries(request, **kwargs):
    start_date = datetime.strptime(kwargs.get('start_date'), '%d/%m/%Y').strftime('%Y-%m-%d') if kwargs.get('start_date') else get_last_monay_as_date()
    end_date = datetime.strptime(kwargs.get('end_date'), '%d/%m/%Y').strftime('%Y-%m-%d') if kwargs.get('end_date') else tzlocal.now()

    seller_id = kwargs.get('seller_id')
    total_sum = Entry.objects.aggregate(Sum('value'))
    entries = Entry.objects.filter(creation_date__date__gte=start_date, creation_date__date__lte=end_date)

    if kwargs.get('seller_username'):
        entries = entries.filter(user__username__icontains=kwargs.get('seller_username'))

    return {
        'entry_total': total_sum.get('value__sum'),
        'entries': entries
    }
