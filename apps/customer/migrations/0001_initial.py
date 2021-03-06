# Generated by Django 3.1.7 on 2021-06-13 14:10

import core.django.validators
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth_user.user')),
                ('address1', models.CharField(max_length=250, verbose_name='address1')),
                ('address2', models.CharField(blank=True, max_length=250, verbose_name='address1')),
                ('suburb', models.CharField(max_length=250, verbose_name='suburb')),
                ('city', models.CharField(max_length=250, verbose_name='city')),
                ('post_code', models.CharField(max_length=4, validators=[core.django.validators.NumberOnlyValidator()], verbose_name='post code')),
                ('state', models.CharField(blank=True, choices=[('NSW', 'NSW'), ('VIC', 'VIC'), ('QLD', 'QLD'), ('TAS', 'TAS'), ('WA', 'WA'), ('ACT', 'ACT'), ('NT', 'NT')], max_length=255, verbose_name='state')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth_user.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('POOL', 'POOL'), ('SPA', 'SPA')], max_length=32, verbose_name='pool type')),
                ('chlorine_source', models.CharField(blank=True, choices=[('BLEACH', 'BLEACH'), ('SWG', 'SWG'), ('TRICHLOR', 'TRICHLOR')], max_length=32, verbose_name='chlorine source')),
                ('pool_surface', models.CharField(blank=True, choices=[('PLASTER', 'PLASTER'), ('VINYL', 'VINYL'), ('FIBERGLASS', 'FIBERGLASS')], max_length=32, verbose_name='pool surface')),
                ('volume', models.IntegerField(verbose_name='volume litre')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
            ],
        ),
    ]
