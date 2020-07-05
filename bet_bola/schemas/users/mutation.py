import graphene
from graphene import  Field
from .mutationTypes import CreateSellerType, EditSellerType, RemoveSellerType

class UserMutation(graphene.ObjectType):
    create_seller = CreateSellerType.Field()
    edit_seller = EditSellerType.Field()
    remove_seller = RemoveSellerType.Field()