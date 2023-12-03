from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import password_validation

from.models import Usuario


# AuthenticationForm
class FormularioLogin(AuthenticationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el Nombre de Usuario',
                }
            ),
            'password': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la contraseña',
                }
            )
        }
        


class FormularioUsuario(forms.ModelForm):
    password1 = forms.CharField(
        required=True,
        label='Contraseña',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su contraseña',
                'id': 'password1',
            }
        ),
        validators=[password_validation.validate_password],
        help_text=password_validation.password_validators_help_text_html(),
    )

    password2 = forms.CharField(
        required=True,
        label='Confirmación de Contraseña',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su contraseña de nuevo',
                'id': 'password2',
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),

    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nombres', 'apellidos', 'rol', 'edificio', 'piso', 'password1', 'password2']
        widgets = {
            'rol': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el rol',
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre de usuario',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Correo electrónico',
                }
            ),
            'nombres': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su/s nombre/s',
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'edificio': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el edificio',
                }
            ),
            'piso': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el edificio',
                }
            )
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.save()

        if commit:
            user.save()
        return user

    def get_user(self):
        email = self.cleaned_data.get('email')
        return Usuario.objects.get(email=email)