from graphene_django import DjangoObjectType
from ticket.models import Ticket
from graphene import ObjectType, relay
from graphene.types import String, Decimal, Float, Int, DateTime, Field, List, Boolean

class TicketTypeListNode(DjangoObjectType):
    real_id = String()
    owner = String()
    creator = String()
    reward = Decimal()
    payment = String()
    status = String()
    cotation_sum = Decimal()
    client_cellphone = String()
    payment_date = String()
    cotation_count = Int()
    
    def resolve_real_id(self, info):
        return self.id

    def resolve_cotation_count(self, info):
        return self.cotation_count()

    def resolve_payment_date(self, info):
        return self.payment.date

    def resolve_client_cellphone(self, info):
        return self.owner.cellphone

    def resolve_cotation_sum(self, info):
        return self.cotation_sum()[1]

    def resolve_status(self, info):
        return self.get_status_display()

    def resolve_owner(self, info):
        return self.owner.first_name

    def resolve_creator(self, info):
        return self.creator.username

    def resolve_reward(self, info):
        return self.reward.value

    def resolve_payment(self, info):
        return self.payment.get_status_display()

    class Meta:
        model = Ticket
        interfaces = (relay.Node, )
        filter_fields = {
            'ticket_id': ['icontains'],
            'available': ['exact'],
            'status': ['exact'],
            'owner__first_name': ['icontains'],
            'creator__username': ['icontains'],
            'payment__who_paid__username': ['icontains'],
            'creation_date': ['date__exact'],
            'payment__date': ['exact']
        }
