# Generated migration for adding indexes
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_remove_semesterrequirement_category_and_more'),
    ]

    operations = [
        # Add indexes to Member model
        migrations.AddIndex(
            model_name='member',
            index=models.Index(fields=['status'], name='member_status_idx'),
        ),
        migrations.AddIndex(
            model_name='member',
            index=models.Index(fields=['name'], name='member_name_idx'),
        ),
        
        # Add indexes to Event model
        migrations.AddIndex(
            model_name='event',
            index=models.Index(fields=['category'], name='event_category_idx'),
        ),
        migrations.AddIndex(
            model_name='event',
            index=models.Index(fields=['date'], name='event_date_idx'),
        ),
        migrations.AddIndex(
            model_name='event',
            index=models.Index(fields=['category', 'date'], name='event_cat_date_idx'),
        ),
        
        # Add indexes to HourLog model
        migrations.AddIndex(
            model_name='hourlog',
            index=models.Index(fields=['member', 'date'], name='hourlog_member_date_idx'),
        ),
        migrations.AddIndex(
            model_name='hourlog',
            index=models.Index(fields=['member'], name='hourlog_member_idx'),
        ),
        
        # Add index to SemesterRequirement model
        migrations.AddIndex(
            model_name='semesterrequirement',
            index=models.Index(fields=['semester'], name='semester_idx'),
        ),
        
        # Make semester field unique
        migrations.AlterField(
            model_name='semesterrequirement',
            name='semester',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]