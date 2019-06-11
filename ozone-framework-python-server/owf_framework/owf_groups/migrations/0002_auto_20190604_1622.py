# Generated by Django 2.2.1 on 2019-06-04 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0002_auto_20190603_2241'),
        ('owf_groups', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OWFGroupPeople',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='owf_groups.OWFGroup')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.Person')),
            ],
            options={
                'db_table': 'owf_group_people',
            },
        ),
        migrations.AddField(
            model_name='owfgroup',
            name='people',
            field=models.ManyToManyField(through='owf_groups.OWFGroupPeople', to='people.Person'),
        ),
    ]
