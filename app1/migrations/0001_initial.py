# Generated by Django 4.2.1 on 2023-05-12 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ishchi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ism', models.CharField(max_length=120)),
                ('familya', models.CharField(max_length=120)),
                ('jins', models.BooleanField(default=True)),
                ('birth_date', models.DateField()),
                ('lavozim', models.CharField(max_length=120)),
                ('oylik', models.CharField(max_length=120)),
            ],
        ),
    ]