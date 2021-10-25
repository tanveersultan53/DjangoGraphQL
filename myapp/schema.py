import graphene
from .models import Author
from graphene_django import DjangoObjectType


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = ("id", "name", "biodata")


class Query(graphene.ObjectType):
    all_authors = graphene.List(AuthorType)
    single_author = graphene.Field(AuthorType, id=graphene.Int())

    @graphene.resolve_only_args
    def resolve_all_authors(self):
        return Author.objects.filter()

    def resolve_single_author(self, info, id):
        return Author.objects.get(pk=id)


class AuthorMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        biodata = graphene.String(required=True)

    author = graphene.Field(AuthorType)

    @classmethod
    def mutate(cls, root, info, name, biodata):
        author = Author(name=name, biodata=biodata)
        author.save()
        return AuthorMutation(author=author)
class AuthorUpdate(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)
        biodata = graphene.String(required=True)

    author = graphene.Field(AuthorType)

    @classmethod
    def mutate(cls, root, info, id,name, biodata):
        author = Author.objects.get(pk=id)
        author.name = name
        author.biodata = biodata
        author.save()
        return AuthorMutation(author=author)

class AuthorDelete(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    author = graphene.Field(AuthorType)
    @classmethod
    def mutate(cls, root, info, id):
        author = Author.objects.get(id=id)
        author.delete()
        return "Delete Data Successfully!"


class Mutation(graphene.ObjectType):
    add_author = AuthorMutation.Field()
    author_delete = AuthorDelete.Field()
    update_author = AuthorUpdate.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
