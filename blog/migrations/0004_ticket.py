# Generated by Django 4.2.3 on 2023-07-31 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_category_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='نام')),
                ('email', models.EmailField(max_length=250, verbose_name='ایمیل')),
                ('phone', models.CharField(max_length=12, verbose_name='شماره تماس')),
                ('subject', models.CharField(max_length=100, verbose_name='موضوع')),
                ('message', models.TextField(verbose_name='پیام')),
            ],
            options={
                'verbose_name': 'تیکت',
                'verbose_name_plural': 'تیکت ها',
            },
        ),
    ]
