# Generated by Django 4.0.2 on 2022-11-17 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_ct'),
    ]

    operations = [
        migrations.CreateModel(
            name='saggital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saggital_photo', models.ImageField(upload_to='saggital_images')),
            ],
        ),
    ]