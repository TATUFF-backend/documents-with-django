# Generated by Django 5.0.9 on 2024-10-01 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_faculty_document_comment_user_faculty_field_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='document/comment/'),
        ),
    ]
