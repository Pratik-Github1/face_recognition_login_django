# Generated by Django 4.2.4 on 2023-08-19 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_userprofile_current_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='current_location',
        ),
        migrations.CreateModel(
            name='user_current_location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_location', models.CharField(blank=True, max_length=400, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile')),
            ],
        ),
    ]