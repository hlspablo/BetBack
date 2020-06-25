from history.models import CashierCloseSeller, CashierCloseManager

def get_last_closed_cashier_seller(seller):
    return CashierCloseSeller.objects.filter(seller=seller).order_by('-date')\
        .first().date.strftime("%d/%m/%Y %H:%M:%S") if CashierCloseSeller\
        .objects.filter(seller=seller).count() > 0 else "Sem Registro"

def get_last_closed_cashier_manager(manager):
    return CashierCloseManager.objects.filter(manager=manager).order_by('-date')\
        .first().date.strftime("%d/%m/%Y %H:%M:%S") if CashierCloseManager\
        .objects.filter(manager=manager).count() > 0 else "Sem Registro"