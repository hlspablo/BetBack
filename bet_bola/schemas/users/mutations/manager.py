from user.models import Seller, Manager
from django.db import  transaction

@transaction.atomic
def remove_manager(request, **kwargs):
    ## TODO VALIDATIONS ON DATA SENT
    ## AND PERMISSIONS CHECKING

    manager_id = kwargs.get('manager_id')
    manager = Manager.objects.get(pk=manager_id)
    num = 0
    removed_name = manager.username + "_removed_" + str(num)
    while Manager.objects.filter(username=removed_name).count() > 0:
        num +=1
        removed_name = manager.username + "_removed_" + str(num)
    manager.username = removed_name
    manager.is_active = False
    manager.save()
    
    return{
        'success': True
    }

@transaction.atomic
def edit_manager(request, **kwargs):
    ## TODO VALIDATIONS ON DATA SENT
    ## AND PERMISSIONS CHECKING

    manager_id = kwargs.get('manager_id')
    manager = Manager.objects.get(pk=manager_id)

    name = kwargs.get('name', manager.first_name)
    email = kwargs.get('email', manager.email)
    password = kwargs.get('password', manager.password)
    cellphone = kwargs.get('cellphone', manager.cellphone)
    cpf = kwargs.get('cpf', manager.cpf)
    address = kwargs.get('address', manager.address)
    cancel_limit_time = kwargs.get('cancel_limit_time', manager.limit_time_to_cancel)
    can_cancel_ticket = kwargs.get('can_cancel_ticket', manager.can_cancel_ticket)
    can_create_ticket_unlimited = kwargs.get('can_create_ticket_unlimited', manager.can_sell_unlimited)
    can_change_limit_time = kwargs.get('can_change_limit_time', manager.can_change_limit_time)
    can_modify_seller = kwargs.get('can_modify_seller', manager.can_modify_seller)
    can_modify_seller_comissions = kwargs.get('can_modify_seller_comissions', manager.can_modify_seller_comissions)
    comission_based_on_profit = kwargs.get('comission_based_on_profit', manager.comission_based_on_profit)
    can_close_cashier = kwargs.get('can_close_cashier', manager.can_close_cashier)
    can_add_entry = kwargs.get('can_add_entry', manager.can_add_entry)
    active = kwargs.get('active', manager.is_active)

    
    Manager.objects.filter(pk=manager_id).update(
        first_name=name,
        email=email,
        password=password,
        cellphone=cellphone,
        cpf=cpf,
        address=address,
        limit_time_to_cancel=cancel_limit_time,
        can_sell_unlimited=can_create_ticket_unlimited,
        can_cancel_ticket=can_cancel_ticket,
        can_change_limit_time=can_change_limit_time,
        can_modify_seller=can_modify_seller,
        can_modify_seller_comissions=can_modify_seller_comissions,
        comission_based_on_profit=comission_based_on_profit,
        can_close_cashier=can_close_cashier,
        can_add_entry=can_add_entry,
        is_active=active
    )

    return {
        'success': True
    }



@transaction.atomic
def create_manager(request, **kwargs):
    ## TODO VALIDATIONS ON DATA SENT
    ## AND PERMISSIONS CHECKING

    username = kwargs.get('username')
    name = kwargs.get('name')
    email = kwargs.get('email')
    password = kwargs.get('password')
    cellphone = kwargs.get('cellphone')
    cpf = kwargs.get('cellphone')
    address = kwargs.get('address')
    
    manager = Manager.objects.create(
        first_name=name,
        username=username,
        password=password,
        cellphone=cellphone,
        email=email,
        cpf=cpf,
        address=address,
        my_store=request.user.my_store
    )

    return {
        'success': True
    }
