# Generated by Django 3.1.7 on 2021-08-26 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cureview', '0011_review_relatedprofessor'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewableobject',
            name='numReviews',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
