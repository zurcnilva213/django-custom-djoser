# Generated by Django 4.1.4 on 2023-11-28 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_influencer_birthday_influencer_facebook_handle_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='influencer',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name='Birthday'),
        ),
    ]
