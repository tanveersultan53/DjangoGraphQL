import graphene
from .models import Author
from graphene_django import DjangoObjectType


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = ("id", "name", "biodata")


class Query(graphene.ObjectType):
    all_authors = graphene.List(AuthorType)

    @graphene.resolve_only_args
    def resolve_all_authors(self):
        return Author.objects.filter()


schema = graphene.Schema(query=Query)
