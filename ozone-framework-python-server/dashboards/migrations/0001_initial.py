# Generated by Django 2.2.1 on 2019-08-15 21:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stacks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('version', models.BigIntegerField()),
                ('isdefault', models.BooleanField()),
                ('dashboard_position', models.IntegerField()),
                ('altered_by_admin', models.BooleanField()),
                ('guid', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=4000, null=True)),
                ('created_date', models.DateTimeField(blank=True, null=True)),
                ('edited_date', models.DateTimeField(blank=True, null=True)),
                ('layout_config', models.TextField(blank=True, null=True)),
                ('locked', models.BooleanField(blank=True, null=True)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
                ('icon_image_url', models.CharField(blank=True, max_length=2083, null=True)),
                ('published_to_store', models.BooleanField(blank=True, null=True)),
                ('marked_for_deletion', models.BooleanField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='dashboard_created_by', to=settings.AUTH_USER_MODEL)),
                ('edited_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='dashboard_edited_by', to=settings.AUTH_USER_MODEL)),
                ('stack', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='stacks.Stack')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='dashboard_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'dashboard',
                'managed': True,
            },
        ),
    ]