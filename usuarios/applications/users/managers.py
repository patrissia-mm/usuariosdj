from django.db import models
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager, models.Manager):
    def _create_user(self, username, email, password, is_staff, is_superuser, is_active, **extra_fields):
        # crear una variable 'user' que va ser igual al modelo que está haciendo el llamado a este Manager
        user = self.model(
            username = username,
            email = email,
            is_staff = is_staff,
            is_superuser = is_superuser,
            is_active = is_active,
            **extra_fields
        )
        #encripta el password que se está guardando
        user.set_password(password)
        #guardamos el usuario
        user.save(using=self.db)
        return user
    
    #crear una función para crear un usuario
    def create_user(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, False, **extra_fields)
    
    def create_superuser(self, username, email, password = None, **extra_fields):
        return self._create_user(username, email, password, True, True, True, **extra_fields)

    def cod_validation(self, id_user, cod_registro):
        if self.filter(id=id_user, codregistro=cod_registro).exists():
            return True
        else:
            return False