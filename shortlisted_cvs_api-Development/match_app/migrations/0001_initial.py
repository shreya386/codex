# Generated by Django 4.2.3 on 2023-07-05 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExperienceLevelMaster',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('created_by', models.CharField(blank=True, max_length=255, null=True)),
                ('created_date', models.DateTimeField(blank=True, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=255, null=True)),
                ('updated_date', models.DateTimeField(blank=True, null=True)),
                ('expression', models.CharField(blank=True, max_length=255, null=True)),
                ('from_year', models.IntegerField()),
                ('is_enable', models.TextField(blank=True, null=True)),
                ('level', models.CharField(blank=True, max_length=255, null=True)),
                ('to_year', models.IntegerField()),
            ],
            options={
                'db_table': 'experience_level_master',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='JobDetail',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('created_by', models.CharField(blank=True, max_length=255, null=True)),
                ('created_date', models.DateTimeField(blank=True, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=255, null=True)),
                ('updated_date', models.DateTimeField(blank=True, null=True)),
                ('annual_salary_from', models.FloatField()),
                ('annual_salary_to', models.FloatField()),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('jd_skills_extracted', models.TextField(blank=True, null=True)),
                ('employment_type', models.CharField(blank=True, max_length=255, null=True)),
                ('estimated_start_date', models.DateTimeField(blank=True, null=True)),
                ('hourly_rate_from', models.FloatField()),
                ('hourly_rate_to', models.FloatField()),
                ('is401kretirement', models.IntegerField()),
                ('is_health_benifit', models.TextField()),
                ('is_pay_for_milage', models.TextField()),
                ('is_per_diem', models.TextField()),
                ('is_relocation_benifit', models.TextField()),
                ('is_yearly_bonus', models.TextField()),
                ('job_cancelled_date', models.DateTimeField(blank=True, null=True)),
                ('job_completed_date', models.DateTimeField(blank=True, null=True)),
                ('job_posted_date', models.DateTimeField(blank=True, null=True)),
                ('job_type', models.CharField(blank=True, max_length=255, null=True)),
                ('last_saved_step', models.IntegerField()),
                ('latitude', models.FloatField()),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('longitude', models.FloatField()),
                ('milage_rate', models.FloatField()),
                ('minimum_mile', models.FloatField()),
                ('no_of_opening_job', models.IntegerField()),
                ('per_diem_rate', models.FloatField()),
                ('region', models.CharField(blank=True, max_length=255, null=True)),
                ('special_qualification', models.TextField(blank=True, null=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('worker_margin', models.FloatField()),
                ('zip_code', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'job_detail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='JobTitleMaster',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('created_by', models.CharField(blank=True, max_length=255, null=True)),
                ('created_date', models.DateTimeField(blank=True, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=255, null=True)),
                ('updated_date', models.DateTimeField(blank=True, null=True)),
                ('is_enable', models.TextField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True, unique=True)),
            ],
            options={
                'db_table': 'job_title_master',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserMaster',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('created_by', models.CharField(blank=True, max_length=255, null=True)),
                ('created_date', models.DateTimeField(blank=True, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=255, null=True)),
                ('updated_date', models.DateTimeField(blank=True, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('is_active', models.TextField()),
                ('is_deleted', models.TextField()),
                ('is_verified', models.TextField()),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('reset_password_token', models.CharField(blank=True, max_length=255, null=True)),
                ('sub_admin_contact_number', models.CharField(blank=True, max_length=255, null=True)),
                ('verification_token', models.CharField(blank=True, max_length=255, null=True)),
                ('stripe_customer_id', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'user_master',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WorkerAttachment',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('file_name', models.CharField(max_length=255)),
                ('path', models.CharField(max_length=255)),
                ('skills_extracted', models.TextField(blank=True, null=True)),
                ('location', models.TextField(blank=True, null=True)),
                ('document_type', models.CharField(max_length=50)),
                ('created_date', models.DateTimeField(blank=True, null=True)),
                ('updated_date', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=255, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'worker_attachment',
                'managed': False,
            },
        ),
    ]
