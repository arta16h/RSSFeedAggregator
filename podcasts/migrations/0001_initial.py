# Generated by Django 4.2.5 on 2023-11-07 21:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('author', models.CharField(max_length=50, null=True)),
                ('rssOwner', models.CharField(blank=True, max_length=50, null=True)),
                ('websiteUrl', models.URLField(blank=True, max_length=255, null=True)),
                ('isExplicitContent', models.CharField(default='no', max_length=5)),
                ('copyright', models.CharField(blank=True, max_length=50, null=True)),
                ('language', models.CharField(blank=True, max_length=50, null=True)),
                ('contentType', models.CharField(blank=True, max_length=10, null=True)),
                ('pubDate', models.DateTimeField(auto_now_add=True)),
                ('imageUrl', models.URLField(blank=True, max_length=255, null=True)),
                ('subtitle', models.CharField(blank=True, max_length=255, null=True)),
                ('keywords', models.TextField(blank=True, null=True)),
                ('category', models.ManyToManyField(to='podcasts.category')),
            ],
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('duration', models.CharField(max_length=25)),
                ('pubDate', models.DateTimeField()),
                ('explicit', models.CharField(default='no', max_length=5)),
                ('summary', models.TextField(blank=True, null=True)),
                ('audioUrl', models.URLField(max_length=300)),
                ('imageUrl', models.URLField(blank=True, max_length=255, null=True)),
                ('podcast', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='podcasts.podcast')),
            ],
        ),
    ]
