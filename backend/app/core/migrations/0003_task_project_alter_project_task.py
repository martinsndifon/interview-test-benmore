# Generated by Django 4.0.10 on 2024-03-14 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_task_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='task_project', to='core.project'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='task',
            field=models.ManyToManyField(blank=True, related_name='tasks', to='core.task'),
        ),
    ]
