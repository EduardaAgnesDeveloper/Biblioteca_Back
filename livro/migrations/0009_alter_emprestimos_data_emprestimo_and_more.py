# Generated by Django 5.0.2 on 2024-09-17 23:56

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livro', '0008_alter_emprestimos_data_emprestimo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emprestimos',
            name='data_emprestimo',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 17, 20, 56, 39, 419621)),
        ),
        migrations.AlterField(
            model_name='emprestimos',
            name='livro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='livro.livros'),
        ),
    ]
