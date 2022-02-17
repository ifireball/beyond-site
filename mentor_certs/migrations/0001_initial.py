# Generated by Django 4.0 on 2022-02-15 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mentor_level', models.IntegerField(choices=[(0, 'Not a mentor'), (1, 'mentor (1 semester)'), (2, 'mentor (2 semesters)'), (3, 'mentor (3 semesters)'), (4, 'mentoring star! (4+ semesters)'), (101, 'lead mentor (1 semester)'), (102, 'lead mentor (2 semesters)'), (103, 'lead mentor (3 semesters)'), (104, 'leading star! (4+ semesters)')], default=0)),
                ('instructor_level', models.IntegerField(choices=[(0, 'Not an instructor'), (100001, 'Speaker'), (100002, 'Course lead')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='StaffMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=60, unique=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('staff', models.ManyToManyField(through='mentor_certs.Certificate', to='mentor_certs.StaffMember')),
            ],
        ),
        migrations.AddField(
            model_name='certificate',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentor_certs.course'),
        ),
        migrations.AddField(
            model_name='certificate',
            name='staff_member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentor_certs.staffmember'),
        ),
    ]