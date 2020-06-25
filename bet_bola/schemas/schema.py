import graphene
from .core.gql import CoreQuery
from .cashier.gql import CashierQuery

class Query(CoreQuery, CashierQuery):
    pass

schema = graphene.Schema(query=Query)