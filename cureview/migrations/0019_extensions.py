from django.db import migrations, models
from django.contrib.postgres.operations import TrigramExtension

class Migration(migrations.Migration):
    dependencies = [
        ('cureview', '0018_auto_20210826_1503'),
    ]

    operations = [
        TrigramExtension(),
    ]