import factory
from members.models import CustomUser

class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
    
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.Faker('password')
    username = factory.LazyAttribute(lambda user: '{}{}'.format(user.first_name, user.last_name[0]).lower())
    email = factory.LazyAttribute(lambda user: '{}.{}@test.com'.format(user.first_name, user.last_name).lower())
