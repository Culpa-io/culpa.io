# Generated by Django 3.1.7 on 2021-07-26 02:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cureview', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('date', models.DateField()),
                ('title', models.CharField(max_length=200)),
                ('contents', models.TextField()),
                ('overall_rating', models.PositiveIntegerField(default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('image', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ReviewableCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='coursereview',
            name='course',
        ),
        migrations.RemoveField(
            model_name='coursereview',
            name='professors',
        ),
        migrations.RemoveField(
            model_name='department',
            name='professors',
        ),
        migrations.DeleteModel(
            name='Course',
        ),
        migrations.DeleteModel(
            name='CourseReview',
        ),
        migrations.DeleteModel(
            name='Department',
        ),
        migrations.DeleteModel(
            name='Professor',
        ),
        migrations.AddField(
            model_name='review',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cureview.reviewablecategory'),
        ),
    ]
