import graphene
from graphene import  Field
from .mutationTypes import (
    CreateSellerType, 
    EditSellerType, 
    RemoveSellerType,
    CreateManagerType,
    EditManagerType,
    RemoveManagerType
)

class UserMutation(graphene.ObjectType):
    create_seller = CreateSellerType.Field()
    edit_seller = EditSellerType.Field()
    remove_seller = RemoveSellerType.Field()
    create_manager = CreateManagerType.Field()
    edit_manager = EditManagerType.Field()
    remove_manager = RemoveManagerType.Field()