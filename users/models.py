from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email} ({self.first_name} {self.last_name})'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        password_previous = None
        if self.pk:
            user_previous = User.objects.get(pk=self.pk)
            password_previous = user_previous.password
        if self._state.adding or self.password != password_previous:
            self.set_password(self.password)

        return super().save(*args, **kwargs)
