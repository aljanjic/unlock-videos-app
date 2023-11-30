# Generated by Django 4.2.7 on 2023-11-30 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0004_uploadedimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='images/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='UploadedImage',
        ),
    ]
