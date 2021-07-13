# Generated by Django 3.2.4 on 2021-07-12 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appindoor1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('hora_encendido', models.DateTimeField()),
                ('hora_apagado', models.DateTimeField()),
                ('temperatura_minima', models.IntegerField(max_length=2)),
                ('temperatura_maxima', models.IntegerField(max_length=2)),
                ('humedad_minima', models.IntegerField(max_length=2)),
                ('humedad_maxima', models.IntegerField(max_length=2)),
            ],
        ),
    ]