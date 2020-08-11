# Generated by Django 3.1 on 2020-08-11 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conlicita_app', '0004_auto_20200810_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='telefone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='empresa',
            unique_together={('cnpj',)},
        ),
    ]
