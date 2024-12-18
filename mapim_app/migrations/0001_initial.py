# Generated by Django 5.1.2 on 2024-11-20 16:52

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deteccion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dni_paciente', models.BigIntegerField(blank=True, null=True)),
                ('imagen', models.TextField(blank=True, null=True)),
                ('resultado', models.CharField(blank=True, max_length=50, null=True)),
                ('precision', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('fecha', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'deteccion',
            },
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('dni', models.CharField(blank=True, max_length=8, null=True, unique=True)),
                ('nombres', models.CharField(blank=True, max_length=100, null=True)),
                ('apellido_paterno', models.CharField(blank=True, max_length=100, null=True)),
                ('apellido_materno', models.CharField(blank=True, max_length=100, null=True)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('direccion', models.TextField(blank=True, null=True)),
                ('numero_contacto', models.CharField(blank=True, max_length=15, null=True)),
            ],
            options={
                'db_table': 'pacientes',
            },
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Historial',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_analisis', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('imagen', models.TextField(blank=True, null=True)),
                ('resultado', models.CharField(blank=True, choices=[('Benigno', 'Benigno'), ('Maligno', 'Maligno')], default='Benigno', max_length=10, null=True)),
                ('realizado_por', models.CharField(blank=True, max_length=100, null=True)),
                ('comentarios', models.TextField(blank=True, null=True)),
                ('paciente', models.ForeignKey(blank=True, db_column='paciente_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='mapim_app.paciente')),
            ],
            options={
                'db_table': 'historial',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_completo', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('user', models.CharField(max_length=50)),
                ('contraseña', models.CharField(max_length=255)),
                ('fecharegistro', models.DateTimeField(auto_now_add=True)),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mapim_app.rol')),
            ],
        ),
        migrations.AddField(
            model_name='paciente',
            name='usuario',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mapim_app.usuario'),
        ),
        migrations.CreateModel(
            name='Analisis',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='analisis/')),
                ('fecha_subida', models.DateTimeField(auto_now_add=True, null=True)),
                ('es_benigno', models.BooleanField(blank=True, null=True)),
                ('fecha_analisis', models.DateTimeField(auto_now_add=True, null=True)),
                ('paciente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mapim_app.paciente')),
                ('analizado_por', models.ForeignKey(blank=True, limit_choices_to={'rol__nombre': 'Médico'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='analisis_realizados', to='mapim_app.usuario')),
                ('subido_por', models.ForeignKey(blank=True, limit_choices_to={'rol__nombre': 'Médico'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mapim_app.usuario')),
            ],
        ),
    ]
