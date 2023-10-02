from django.core.management.base import BaseCommand
from accounts.models import User
from posts.models import Post
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for i in range(10):
            username = fake.user_name()
            email = fake.email()
            password = '12345678'
            User.objects.create_user(
                username=username, email=email, password=password)

        for i in range(20):
            author = User.objects.order_by('?').first()
            image_url = f'https://picsum.photos/200/300'
            title = fake.text(max_nb_chars=50)
            description = fake.paragraph()
            Post.objects.create(author=author, image_url=image_url,
                                title=title, description=description)

        self.stdout.write(self.style.SUCCESS(
            'Successfully created dummy data'))
