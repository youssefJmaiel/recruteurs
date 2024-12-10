# Generated by Django 4.2.17 on 2024-12-07 23:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recruitment', '0002_cv_delete_customuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='cv',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cv',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='cv',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cvs', to=settings.AUTH_USER_MODEL),
        ),
    ]