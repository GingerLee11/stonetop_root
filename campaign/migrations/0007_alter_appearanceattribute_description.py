# Generated by Django 4.0.6 on 2022-12-07 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0006_alter_specialpossessionextras_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appearanceattribute',
            name='description',
            field=models.CharField(max_length=1000, unique=True),
        ),
    ]
