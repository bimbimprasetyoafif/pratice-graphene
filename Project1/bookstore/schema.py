import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Author, Book

class AuthorInput(graphene.InputObjectType):
    name = graphene.String(required = True)

class BookInput(graphene.InputObjectType):
    title = graphene.String(required = True)
    pages = graphene.Int(required = True)
    year = graphene.Int(required = True)
    author = graphene.InputField(AuthorInput)

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

class CreateAuthor(graphene.Mutation):
    class Arguments:
        author_data = AuthorInput(required = True)
    
    author = graphene.Field(AuthorNode)

    @staticmethod
    def mutate(root, info, author_data=None):
        author = Author(name = author_data.name)
        author.save()

        return CreateAuthor(author=author)

class CreateBook(graphene.Mutation):
    class Arguments:
        book_data = BookInput(required = True)
    
    book = graphene.Field(BookNode)

    @staticmethod
    def mutate(root, info, book_data=None):
        try:
            author = Author.objects.get(name=book_data.author.name)
        except:
            author = Author.objects.create(name=book_data.author.name)

        book = Book.objects.create(
            title = book_data.title,
            pages = book_data.pages,
            year = book_data.year,
            author = author
            )
            
        return CreateBook(book = book)

class Mutation(object):
    create_author = CreateAuthor.Field()
    create_book = CreateBook.Field()

class Query(object):
    author = graphene.relay.Node.Field(AuthorNode)
    all_authors = DjangoFilterConnectionField(AuthorNode)

    book = graphene.relay.Node.Field(BookNode)
    all_books = DjangoFilterConnectionField(BookNode)