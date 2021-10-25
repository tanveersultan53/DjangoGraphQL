import graphene
from .quries import Query
from .mutations import Mutation

schema = graphene.Schema(query=Query, mutation=Mutation)