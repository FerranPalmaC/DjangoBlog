# Generated by Django 4.2.5 on 2023-10-10 09:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_remove_comment_active_remove_comment_dislikes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 10, 9, 20, 18, 556411, tzinfo=datetime.timezone.utc), editable=False),
            preserve_default=False,
        ),
    ]
