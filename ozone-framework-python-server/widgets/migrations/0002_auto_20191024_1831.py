# Generated by Django 2.2.1 on 2019-10-24 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('widgets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='widgetdefinitionwidgettypes',
            name='widget_definition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='widgets.WidgetDefinition'),
        ),
    ]
