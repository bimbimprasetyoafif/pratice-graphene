import graphene
import bookstore.schema as sc

class Query(sc.Query, graphene.ObjectType):
    pass

class Muatation(sc.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Muatation)