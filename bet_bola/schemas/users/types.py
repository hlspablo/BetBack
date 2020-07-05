from graphene_django import DjangoObjectType
from user.models import Seller
from graphene import ObjectType
from graphene import relay
from graphene.types import String, Decimal, Float, Int, DateTime, Field, List, Boolean

class SellersNodeType(DjangoObjectType):
    real_id = Int()
    my_manager = String()

    def resolve_real_id(self, info):
        return self.pk

    def resolve_my_manager(self, info):
        return self.my_manager.username if self.my_manager else ""
    
    class Meta:
        model = Seller
        interfaces = (relay.Node, )
        filter_fields = []
        filter_fields = {
            'first_name': ['icontains'],
            'username': ['icontains'],
            'email': ['icontains'],
            'my_manager__username': ['icontains']
        }
