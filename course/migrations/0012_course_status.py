# Generated by Django 5.0.3 on 2024-03-26 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0011_course_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('in_review', 'In_Review'), ('published', 'Published')], default='draft', max_length=25),
        ),
    ]
