# Generated by Django 4.2.7 on 2024-01-17 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transcription', '0012_transcripts_chatgpt_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transcripts',
            name='content',
            field=models.TextField(max_length=4000),
        ),
    ]
