# Generated by Django 3.1.8 on 2023-04-12 05:31

from django.db import migrations, models
import django.utils.timezone
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='status',
            field=django_fsm.FSMField(choices=[('unresolved', 'unresolved'), ('inappropriate', 'inappropriate'), ('reject', 'Reject')], default='unresolved', max_length=50, protected=True),
        ),
    ]
