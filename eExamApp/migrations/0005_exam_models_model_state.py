# Generated by Django 4.2.1 on 2023-06-21 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eExamApp', '0004_rename_model_state_exam_models_model_degree_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam_models',
            name='model_state',
            field=models.IntegerField(default=0),
        ),
    ]
