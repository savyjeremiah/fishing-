# Generated by Django 5.1.4 on 2025-02-19 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('smoked_fish', 'Smoked Fish'), ('ice_fish', 'Ice Fish'), ('finger_fish', 'Finger Fish')], max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('description', models.TextField(blank=True, null=True)),
                ('available', models.BooleanField(default=True)),
            ],
        ),
    ]
