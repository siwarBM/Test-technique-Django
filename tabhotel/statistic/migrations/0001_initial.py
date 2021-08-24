# Generated by Django 3.1.7 on 2021-08-24 00:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('urlshort', '0002_auto_20210823_2355'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClickAnalytic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('short_url', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='urlshort.shorturl')),
            ],
        ),
    ]