from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Usuario(AbstractUser):
    cpf = models.CharField(max_length=11, unique=True)
    nota = models.FloatField(default=5.0, validators=[MinValueValidator(0.0),
                                        MaxValueValidator(10.0)])

    def __str__(self):
        return self.username

class Anuncio(models.Model):
    usuario = models.ForeignKey(Usuario, related_name='anuncios')
    categoria = models.CharField(max_length=500)
    produto = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    descricao = models.TextField(max_length=500)
    numserie = models.IntegerField(unique=True)
    peso = models.FloatField(validators=[MinValueValidator(0.0)])
    c_prof = models.FloatField(validators=[MinValueValidator(0.0)])
    c_altura = models.FloatField(validators=[MinValueValidator(0.0)])
    c_largura = models.FloatField(validators=[MinValueValidator(0.0)])
    diaria = models.FloatField(validators=[MinValueValidator(0.0)])
    dt_inicio = models.DateTimeField(default=timezone.now)

    def __str__(self):
        anuncio = "%s: %s\n%s" % (self.usuario, self.produto, self.descricao)
        return anuncio

class Aluguel(models.Model):
    usuario = models.ForeignKey(Usuario, related_name='alugueis', on_delete=models.PROTECT)
    anuncio = models.ForeignKey(Anuncio, related_name='alugueis', on_delete=models.PROTECT)
    dt_inicio = models.DateField()
    dt_fim = models.DateField()
    dt_lance = models.DateTimeField(default=timezone.now)
    aval_1 = models.FloatField(null = True)
    aval_2 = models.FloatField(null = True)
    preco = models.FloatField(validators=[MinValueValidator(0.0)])
