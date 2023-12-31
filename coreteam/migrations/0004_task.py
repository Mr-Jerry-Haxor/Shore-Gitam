# Generated by Django 4.2.8 on 2023-12-07 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreteam', '0003_delete_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_title', models.CharField(max_length=100)),
                ('domain', models.CharField(choices=[('president', 'President'), ('vice-president', 'Vice President'), ('technology', 'Technology'), ('events-cultural', 'Events - Cultural'), ('events-sports', 'Events - Sports'), ('legal', 'Legal'), ('operations', 'Operations'), ('marketing', 'Marketing'), ('sponsorship', 'Sponsorship'), ('design', 'Design'), ('finance', 'Finance'), ('media', 'Media'), ('security', 'Security'), ('hospitality', 'Hospitality')], max_length=50)),
                ('description', models.TextField(blank=True)),
                ('priority', models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], max_length=20)),
                ('attached_file', models.FileField(blank=True, null=True, upload_to='Taskattachments/')),
                ('due_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('todo', 'Todo'), ('in_progress', 'In Progress'), ('overdue', 'Overdue'), ('completed', 'Completed')], default='todo', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assigned_to', models.CharField(max_length=100)),
                ('assigned_by', models.CharField(max_length=100)),
            ],
        ),
    ]
