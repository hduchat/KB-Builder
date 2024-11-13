# Generated by Django 4.1.13 on 2024-11-04 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0004_alter_model_credential'),
    ]

    operations = [
        migrations.AddField(
            model_name='model',
            name='permission_type',
            field=models.CharField(choices=[('PUBLIC', '公开'), ('PRIVATE', '私有')], default='PRIVATE', max_length=20, verbose_name='权限类型'),
        ),
    ]
