# Generated by Django 5.0.2 on 2024-04-13 20:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livro', '0022_alter_emprestimos_data_emprestimo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emprestimos',
            name='data_emprestimo',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 13, 17, 37, 46, 379141)),
        ),
    ]
