from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    REQUIRED_FIELDS = []

    # class Meta:
    #     verbose_name = 'User'
    #     verbose_name_plural = 'Users'
    #
    # def __str__(self):
    #     return self.username
