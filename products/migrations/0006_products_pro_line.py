# Generated by Django 5.0.4 on 2025-03-06 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_products_pro_therapeutic_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='pro_line',
            field=models.CharField(choices=[('General', 'General'), ('Penicillins', "Penicillin's"), ('Cephalosporins', 'Cephalosporins'), ('Other', 'Other')], default='Other', max_length=20, verbose_name='Product Line'),
        ),
    ]
