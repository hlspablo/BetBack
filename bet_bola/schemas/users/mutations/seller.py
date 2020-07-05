from user.models import Seller, Manager
from django.db import  transaction

@transaction.atomic
def remove_seller(request, **kwargs):
    ## TODO VALIDATIONS ON DATA SENT
    ## AND PERMISSIONS CHECKING

    seller_id = kwargs.get('seller_id')
    seller = Seller.objects.get(pk=seller_id)
    num = 0
    removed_name = seller.username + "_removed_" + str(num)
    while Seller.objects.filter(username=removed_name).count() > 0:
        num +=1
        removed_name = seller.username + "_removed_" + str(num)
    seller.username = removed_name
    seller.is_active = False
    seller.save()
    
    return{
        'success': True
    }

@transaction.atomic
def edit_seller(request, **kwargs):
    ## TODO VALIDATIONS ON DATA SENT
    ## AND PERMISSIONS CHECKING

    seller_id = kwargs.get('seller_id')
    seller = Seller.objects.get(pk=seller_id)

    name = kwargs.get('name', seller.first_name)
    email = kwargs.get('email', seller.email)
    password = kwargs.get('password', seller.password)
    cellphone = kwargs.get('cellphone', seller.cellphone)
    cpf = kwargs.get('cpf', seller.cpf)
    address = kwargs.get('address', seller.address)
    manager_id = kwargs.get('manager_id', seller.my_manager.pk)
    cancel_limit_time = kwargs.get('cancel_limit_time', seller.limit_time_to_cancel)
    can_create_ticket_unlimited = kwargs.get('can_create_ticket_unlimited', seller.can_sell_unlimited)
    can_cancel_ticket = kwargs.get('can_cancel_ticket', seller.can_cancel_ticket)
    active = kwargs.get('active', seller.is_active)
    
    
    Seller.objects.filter(pk=seller_id).update(
        first_name=name,
        email=email,
        password=password,
        cellphone=cellphone,
        cpf=cpf,
        address=address,
        my_manager=Manager.objects.get(pk=manager_id),
        limit_time_to_cancel=cancel_limit_time,
        can_sell_unlimited=can_create_ticket_unlimited,
        can_cancel_ticket=can_cancel_ticket,
        is_active=active
    )

    return {
        'success': True
    }



@transaction.atomic
def create_seller(request, **kwargs):
    ## TODO VALIDATIONS ON DATA SENT
    ## AND PERMISSIONS CHECKING

    username = kwargs.get('username')
    name = kwargs.get('name')
    email = kwargs.get('email')
    password = kwargs.get('password')
    cellphone = kwargs.get('cellphone')
    cpf = kwargs.get('cellphone')
    address = kwargs.get('address')
    manager_id = kwargs.get('manager_id')
    
    seller = Seller.objects.create(
        first_name=name,
        username=username,
        password=password,
        cellphone=cellphone,
        email=email,
        cpf=cpf,
        address=address,
        my_store=request.user.my_store
    )

    if manager_id:
        seller.my_manager = Manager.objects.get(pk=manager_id)
        seller.save()

    return {
        'success': True
    }
