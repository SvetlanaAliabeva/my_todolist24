from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

class PasswordField(serializers.CharField):

    def __init__(self, **kwargs) -> None:
        kwargs['style'] = {'input_type': 'password'}
        kwargs.setdefault('write_only', True)
        kwargs.setdefault('required', True)
        super().__init__(**kwargs)
        self.validators.append(validate_password)

