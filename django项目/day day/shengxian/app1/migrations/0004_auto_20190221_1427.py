# Generated by Django 2.1.5 on 2019-02-21 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_remove_good_type_ctime'),
    ]

    operations = [
        migrations.AddField(
            model_name='good_type',
            name='ctime',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间'),
        ),
        migrations.AddField(
            model_name='good_type',
            name='rec',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='新品推荐'),
        ),
        migrations.AddField(
            model_name='good_type',
            name='shangjia',
            field=models.SmallIntegerField(choices=[(0, '否'), (1, '上架')], default=1, verbose_name='是否上架'),
        ),
    ]
