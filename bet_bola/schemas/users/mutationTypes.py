import graphene
from graphene import Field
from graphene.types import Boolean, Int, String, List
from .mutations.seller import create_seller, edit_seller, remove_seller
from .mutations.manager import create_manager, edit_manager, remove_manager

class RemoveManagerType(graphene.Mutation):
    success = Boolean()
    errors = List(String) 

    class Arguments:
        manager_id = Int(required=True)

    def mutate(self, info, **kwargs):
        return remove_manager(info.context, **kwargs)

class EditManagerType(graphene.Mutation):
    success = Boolean()
    errors = List(String) 

    class Arguments:
        manager_id = Int(required=True)
        password = String()
        name = String()
        cellphone = String()
        email = String()
        cpf = String()
        address = String()
        manager_id = Int()
        cancel_limit_time = Int()
        can_create_ticket_unlimited = Boolean()
        can_cancel_ticket = Boolean()
        can_change_limit_time = Boolean()
        can_modify_seller = Boolean()
        can_modify_seller_comissions = Boolean()
        comission_based_on_profit = Boolean()
        can_close_cashier =  Boolean()
        can_add_entry = Boolean()
        active = Boolean()

    def mutate(self, info, **kwargs):
        return edit_manager(info.context, **kwargs)

class CreateManagerType(graphene.Mutation):
    success = Boolean()
    errors = List(String) 

    class Arguments:
        username = String(required=True)
        password = String(required=True)
        name = String(required=True)
        cellphone = String()
        email = String(required=True)
        cpf = String()
        address = String()

    def mutate(self, info, **kwargs):
        return create_manager(info.context, **kwargs)

class RemoveSellerType(graphene.Mutation):
    success = Boolean()
    errors = List(String) 

    class Arguments:
        seller_id = Int(required=True)

    def mutate(self, info, **kwargs):
        return remove_seller(info.context, **kwargs)

class CreateSellerType(graphene.Mutation):
    success = Boolean()
    errors = List(String) 

    class Arguments:
        username = String(required=True)
        password = String(required=True)
        name = String(required=True)
        cellphone = String()
        email = String(required=True)
        cpf = String()
        address = String()
        manager_id = Int()

    def mutate(self, info, **kwargs):
        return create_seller(info.context, **kwargs)


class EditSellerType(graphene.Mutation):
    success = Boolean()
    errors = List(String) 

    class Arguments:
        seller_id = Int(required=True)
        password = String()
        name = String()
        cellphone = String()
        email = String()
        cpf = String()
        address = String()
        manager_id = Int()
        cancel_limit_time = Int()
        can_create_ticket_unlimited = Boolean()
        can_cancel_ticket = Boolean()
        active = Boolean()


    def mutate(self, info, **kwargs):
        return edit_seller(info.context, **kwargs)

