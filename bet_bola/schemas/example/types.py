from graphene_django import DjangoObjectType
from core.models import Game
from graphene import ObjectType
from graphene.types import String, Decimal, Float, Int, DateTime, Field, List, Boolean

# class TicketType(ObjectType):
#     ticket_id = String()
#     status = String()
#     creation_date = String()
