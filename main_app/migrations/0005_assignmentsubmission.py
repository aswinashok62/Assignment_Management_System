# Generated by Django 5.0 on 2025-02-02 09:55

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignmentSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='submissions/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('grade', models.CharField(blank=True, max_length=10, null=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='main_app.assignment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='main_app.student')),
            ],
        ),
    ]
