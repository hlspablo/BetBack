import graphene
from graphene import Field
from graphene.types import String, Int
from graphene_django.filter import DjangoFilterConnectionField
from .types import (
    SellersNodeType,
    ManagersNodeType
)
from user.models import Seller, Manager

class UserQuery(graphene.ObjectType):
    get_sellers = DjangoFilterConnectionField(SellersNodeType)
    get_managers = DjangoFilterConnectionField(ManagersNodeType)

    def resolve_get_sellers (self, info, **kwargs):
        return Seller.objects.all()

    def resolve_get_managers(self, info, **kwargs):
        return Manager.objects.all()
