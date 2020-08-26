# Generated by Django 3.1 on 2020-08-26 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conlicita_app', '0006_auto_20200826_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='licitacao',
            name='arquivo_edital',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='licitacao',
            name='edital',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]