from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator, EmailValidator
from django.contrib.auth.hashers import make_password

class UsuarioManager(BaseUserManager):
    def _create_user(self,username,email,nombres,apellidos,rol,edificio,piso,password,is_staff,is_superuser,**extra_fields):
        user = self.model(
            username = username,
            email = email,
            nombres = nombres,
            apellidos = apellidos,
            rol = rol,
            edificio = edificio,
            piso = piso,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, nombres, apellidos, rol, edificio, piso, password = None,**extra_fields):
        return self._create_user(username, email, nombres, apellidos, rol, edificio, piso, password, False, False,**extra_fields)
    
    def create_superuser(self, username, email, nombres, apellidos, rol, edificio, piso, password = None,**extra_fields):
        return self._create_user(username, email, nombres, apellidos, rol, edificio, piso, password, True, True,**extra_fields)
    
class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Usuario',max_length=50, unique=True, validators=[MinLengthValidator(limit_value=6)])
    email = models.EmailField('Correo electrónico',unique=True, validators=[EmailValidator()])
    
    class Rol(models.TextChoices):
        ADMIN = 'Admin', 'Administrador'
        INTENDENCIA = 'Intendente', 'Intendencia'
    nombres = models.CharField('Nombres',max_length=50)
    apellidos = models.CharField('Apellidos',max_length=50)
    rol = models.CharField('Rol',max_length=12, choices=Rol.choices)
    edificio = models.CharField('Edificio',max_length=50, blank=True, null=True)
    piso = models.PositiveIntegerField('Piso',blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    # Iniciar con username
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','nombres', 'apellidos', 'rol']

    objects = UsuarioManager()
    
    class Meta:
        ordering = ['nombres']

    def __str__(self):
        return f'{self.rol} - {self.nombres} {self.apellidos}'
