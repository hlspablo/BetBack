
import graphene
from graphene.types import Int, Boolean
from schemas.base import BaseMutation
from django.db import transaction
from utils.utils import tzlocal

class todoMutation(BaseMutation):
    queryset = None # TODO

    @transaction.atomic
    def todo(self):
        pass