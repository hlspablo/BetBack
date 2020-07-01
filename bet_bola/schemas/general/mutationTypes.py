import graphene
from graphene import Field
from graphene.types import Boolean, Int, String
#from .mutations.seller import SellerMutations

class TodoType(graphene.Mutation):
    #success = Boolean() 

    class Arguments:
        # close_all = Boolean()
        # manager_id = Int()

    def mutate(self, info, **kwargs):
        pass

