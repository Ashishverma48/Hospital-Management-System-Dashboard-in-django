# Generated by Django 4.2.3 on 2023-07-25 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novapp', '0002_doctor_gender_patient_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='dob',
            field=models.CharField(max_length=14),
        ),
    ]
