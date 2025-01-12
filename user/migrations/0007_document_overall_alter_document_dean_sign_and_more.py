# Generated by Django 5.0.9 on 2024-10-12 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_document_dean_sign_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='overall',
            field=models.CharField(choices=[('waiting', 'Waiting'), ('cancelled', 'Cancelled'), ('accepted', 'Accepted')], default='waiting', max_length=30),
        ),
        migrations.AlterField(
            model_name='document',
            name='dean_sign',
            field=models.CharField(choices=[('waiting', 'Waiting'), ('cancelled', 'Cancelled'), ('accepted', 'Accepted')], default='waiting', max_length=30),
        ),
        migrations.AlterField(
            model_name='document',
            name='department_head_sign',
            field=models.CharField(choices=[('waiting', 'Waiting'), ('cancelled', 'Cancelled'), ('accepted', 'Accepted')], default='waiting', max_length=30),
        ),
        migrations.AlterField(
            model_name='document',
            name='study_head_sign',
            field=models.CharField(choices=[('waiting', 'Waiting'), ('cancelled', 'Cancelled'), ('accepted', 'Accepted')], default='waiting', max_length=30),
        ),
        migrations.AlterField(
            model_name='document',
            name='study_prorector_sign',
            field=models.CharField(choices=[('waiting', 'Waiting'), ('cancelled', 'Cancelled'), ('accepted', 'Accepted')], default='waiting', max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'admin'), ('teacher', 'teacher'), ('department_head', 'department_head'), ('dean', 'dean'), ('study_head', 'study_head'), ('prorector', 'prorector')], max_length=20),
        ),
    ]
