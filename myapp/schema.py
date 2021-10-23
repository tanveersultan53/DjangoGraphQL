import graphene
from graphene_django import DjangoObjectType
from myapp.models import Category


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = "__all__"


class UpdateCategory(graphene.Mutation):
    class Arugments:
        name = graphene.String(required=True)
        id = graphene.ID()

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name, id):
        category = Category.objects.get(pk=id)
        category.name = name
        category.save()

        return UpdateCategory(category=category)


class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

        @classmethod
        def mutate(cls, root, info, name):
            category = Category(name=name)
            category.save()
            return CreateCategory(category=category)


class Query(graphene.ObjectType):
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))

    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return None


class Mutation(graphene.ObjectType):
    update_category = UpdateCategory.Field()
    create_category = CreateCategory.Field()


schema = graphene.Schema(query=Query,mutation=Mutation)

