import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Author, Book

class AuthorNode(DjangoObjectType):
    class Meta:
        model = Author
        filter_fields = ['name']
        interfaces = (graphene.relay.Node,)

class BookNode(DjangoObjectType):
    class Meta:
        model = Book
        filter_fields = [
            'title',
            'pages',
            'year',
            'author',
        ]
        interfaces = (graphene.relay.Node,)

class CreateAuthor(graphene.relay.ClientIDMutation):
    author = graphene.Field(AuthorNode)

    class Input:
        name = graphene.String()

    @classmethod
    def mutate_and_get_payload(self,root,info,**input):
        author = Author(name = input.get('name'))
        author.save()

        return CreateAuthor(author=author)

class Mutation(object):
    input_author = CreateAuthor.Field()

class Query(object):
    author = graphene.relay.Node.Field(AuthorNode)
    all_authors = DjangoFilterConnectionField(AuthorNode)

    book = graphene.relay.Node.Field(BookNode)
    all_books = DjangoFilterConnectionField(BookNode)