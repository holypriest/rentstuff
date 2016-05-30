import re
from django import forms
from .models import Usuario
from django.utils.translation import ugettext_lazy as _

class RegistrationForm(forms.Form):

    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    cpf = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=11)), label=_("CPF"))
    first_name = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("First name"))
    last_name = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Last name"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password (again)"))

    def clean_username(self):
        try:
            user = Usuario.objects.get(username__iexact=self.cleaned_data['username'])
        except Usuario.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data

class AdForm(forms.Form):

    categoria = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=100)), label=_("Categoria"))
    produto = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=100)), label=_("Produto"))
    marca = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=50)), label=_("Marca"))
    modelo = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=50)), label=_("Modelo"))
    descricao = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=500)), label=_("Descrição"))
    numserie = forms.IntegerField(widget=forms.NumberInput(attrs=dict(required=True, max_length=30)), label=_("Numero de serie"))
    peso = forms.FloatField(widget=forms.NumberInput(attrs=dict(required=True, max_length=30)), label=_("Peso"))
    c_prof = forms.FloatField(widget=forms.NumberInput(attrs=dict(required=True, max_length=30)), label=_("Profundidade"))
    c_altura = forms.FloatField(widget=forms.NumberInput(attrs=dict(required=True, max_length=30)), label=_("Altura"))
    c_largura = forms.FloatField(widget=forms.NumberInput(attrs=dict(required=True, max_length=30)), label=_("Largura"))
    diaria = forms.FloatField(widget=forms.NumberInput(attrs=dict(required=True, max_length=30)), label=_("Diária"))

class RentForm(forms.Form):

    dt_inicio = forms.DateField(widget=forms.DateInput(attrs=dict(required=True)), label=_("Data de início"))
    dt_fim = forms.DateField(widget=forms.DateInput(attrs=dict(required=True)), label=_("Data de finalização"))
