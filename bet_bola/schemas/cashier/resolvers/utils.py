from history.models import CashierCloseSeller

def get_last_closed_cashier_seller(seller):
    return CashierCloseSeller.objects.filter(seller=seller).order_by('-date')\
        .first().date.strftime("%d/%m/%Y %H:%M:%S") if CashierCloseSeller\
        .objects.filter(seller=seller).count() > 0 else "Sem Registro"