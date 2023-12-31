# Generated by Django 4.2.8 on 2023-12-26 00:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('event_type', models.CharField(choices=[('culturals', 'culturals')], max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('min_team_size', models.IntegerField()),
                ('max_team_size', models.IntegerField()),
                ('venue', models.CharField(blank=True, max_length=100, null=True)),
                ('event_guidelines', models.TextField(blank=True, null=True)),
                ('event_image', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visible_name', models.CharField(max_length=100, unique=True)),
                ('captain_regnum', models.CharField(max_length=100)),
                ('registered_at', models.DateTimeField(auto_now=True)),
                ('reference_attatchment', models.FileField(blank=True, null=True, upload_to='reference_attatchments/')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prelims.event')),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=10)),
                ('registration_number', models.CharField(blank=True, max_length=100, null=True)),
                ('campus', models.CharField(choices=[('gitam_vzg', 'GITAM Visakhapatnam'), ('gitam_hyd', 'GITAM Hyderabad'), ('gitam_blr', 'GITAM Bangalore')], max_length=100)),
                ('isCaptain', models.BooleanField(default=False)),
                ('registered_at', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prelims.event')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prelims.team')),
            ],
        ),
    ]
