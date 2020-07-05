import graphene
from graphene import Field
from graphene.types import String, Int
from graphene_django.filter import DjangoFilterConnectionField
from .types import (
    SellersNodeType
)
from user.models import Seller

class UserQuery(graphene.ObjectType):
    get_sellers = DjangoFilterConnectionField(SellersNodeType)

    def resolve_ (self, info, **kwargs):
        return Seller.objects.all()
