# Generated by Django 4.2.9 on 2024-01-30 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0002_rename_sipgate_user_companycontacts_sipgate_use'),
    ]

    operations = [
        migrations.RenameField(
            model_name='companycontacts',
            old_name='sipgate_use',
            new_name='sipgate_user',
        ),
        migrations.RenameField(
            model_name='sipgateuser',
            old_name='SipgateUserToken',
            new_name='sipgate_user_token',
        ),
        migrations.AlterField(
            model_name='sipgateuser',
            name='sipgate_user',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
    ]
