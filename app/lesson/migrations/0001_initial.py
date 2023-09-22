# Generated by Django 4.2.5 on 2023-09-22 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('video_link', models.URLField()),
                ('duration_seconds', models.PositiveIntegerField()),
                ('products', models.ManyToManyField(related_name='lesson', to='product.product')),
            ],
        ),
    ]
