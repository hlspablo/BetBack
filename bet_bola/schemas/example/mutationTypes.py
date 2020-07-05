import graphene
from graphene import Field
from graphene.types import Boolean, Int, String, List

class TodoType(graphene.Mutation):
    #success = Boolean() 

    class Arguments:
        # close_all = Boolean()

    def mutate(self, info, **kwargs):
        pass

