# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models
import django.utils.timezone
import django.db.models.deletion
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('username', models.CharField(validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], unique=True, error_messages={'unique': 'A user with that username already exists.'}, verbose_name='username', max_length=30, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(verbose_name='staff status', help_text='Designates whether the user can log into this admin site.', default=False)),
                ('is_active', models.BooleanField(verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('cpf', models.CharField(max_length=11, unique=True)),
                ('nota', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)], default=5.0)),
                ('groups', models.ManyToManyField(blank=True, related_query_name='user', to='auth.Group', verbose_name='groups', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set')),
                ('user_permissions', models.ManyToManyField(blank=True, related_query_name='user', to='auth.Permission', verbose_name='user permissions', help_text='Specific permissions for this user.', related_name='user_set')),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Aluguel',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('dt_inicio', models.DateField()),
                ('dt_fim', models.DateField()),
                ('dt_lance', models.DateTimeField(default=django.utils.timezone.now)),
                ('aval_1', models.FloatField(null=True)),
                ('aval_2', models.FloatField(null=True)),
                ('preco', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
            ],
        ),
        migrations.CreateModel(
            name='Anuncio',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('produto', models.CharField(max_length=100)),
                ('marca', models.CharField(max_length=50)),
                ('modelo', models.CharField(max_length=50)),
                ('descricao', models.TextField(max_length=500)),
                ('numserie', models.IntegerField(unique=True)),
                ('peso', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('c_prof', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('c_altura', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('c_largura', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('diaria', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('dt_inicio', models.DateTimeField(default=django.utils.timezone.now)),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='anuncios')),
            ],
        ),
        migrations.AddField(
            model_name='aluguel',
            name='anuncio',
            field=models.ForeignKey(to='rentstuff.Anuncio', on_delete=django.db.models.deletion.PROTECT, related_name='alugueis'),
        ),
        migrations.AddField(
            model_name='aluguel',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.PROTECT, related_name='alugueis'),
        ),
    ]
