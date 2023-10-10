from django.utils import timezone
import factory
from members.tests.factories import CustomUserFactory
from posts.models import Post, Comment

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Faker('text')
    creation_date = factory.Faker('date_time', tzinfo = timezone.get_current_timezone())
    publication_date = factory.Faker('date_time', tzinfo = timezone.get_current_timezone())
    updated_on = factory.Faker('date_time', tzinfo = timezone.get_current_timezone())
    author = factory.SubFactory(CustomUserFactory)
    content = factory.Faker('text')


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    author = factory.SubFactory(CustomUserFactory)
    post = factory.SubFactory(PostFactory)
    publication_date = factory.Faker('date_time', tzinfo = timezone.get_current_timezone())
    content = factory.Faker('text')
    updated_on = factory.Faker('date_time', tzinfo = timezone.get_current_timezone()) 
