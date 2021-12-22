from django import forms
from django.db import models
from django.db.models import fields
from django.forms import widgets
from folio.models import Usuario
from folio.models import solicitud
from django.contrib.auth.models import User

class Solicitud_form(forms.ModelForm):
    class Meta:
        model = solicitud
        fields = "__all__"
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'dependencia': forms.TextInput(attrs={'class': 'form-control'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control'}),
            'firmado': forms.Select(attrs={'class': 'form-control'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'estatus': forms.Select(attrs={'class': 'form-control'})
        }

class Registro_form(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = "__all__"
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'rfc': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'type': 'password'})
        }

class Registro_form2(Registro_form):
    class Meta(Registro_form.Meta):
        exclude = ['password']