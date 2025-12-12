from django.db import models
from django.utils import timezone

STATUS_CHOICES = [
    ('Active', 'Active'),
    ('Pledge', 'Pledge'),
]

CATEGORY_CHOICES = [
    ('Service', 'Service'),
    ('Finance', 'Finance'),
    ('Membership', 'Membership'),
    ('Communication', 'Communication'),
    ('Leadership', 'Leadership'),
    ('CHIMPS', 'CHIMPS'),
    ('Meeting', 'Meeting'),
]

class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # Already indexed due to unique=True
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    semester_joined = models.CharField(max_length=20)
    dues_paid = models.BooleanField(default=False)
    total_dues_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        # Index for filtering members by status (used in reports)
        indexes = [
            models.Index(fields=['status'], name='member_status_idx'),
            models.Index(fields=['name'], name='member_name_idx'),
        ]

    def __str__(self):
        return f"{self.name} ({self.status})"

class Event(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    date = models.DateField(default=timezone.now)
    duration_hours = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True)

    class Meta:
        # Index for filtering events by category and date
        indexes = [
            models.Index(fields=['category'], name='event_category_idx'),
            models.Index(fields=['date'], name='event_date_idx'),
            models.Index(fields=['category', 'date'], name='event_cat_date_idx'),
        ]

    def __str__(self):
        return f"{self.name} - {self.category}"

class HourLog(models.Model):
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    hours = models.DecimalField(max_digits=5, decimal_places=2, editable=False)
    date = models.DateField(editable=False)

    class Meta:
        # Composite index for the most common query: filtering by member and event category
        indexes = [
            models.Index(fields=['member', 'date'], name='hourlog_member_date_idx'),
            models.Index(fields=['member'], name='hourlog_member_idx'),
        ]

    def save(self, *args, **kwargs):
        # Automatically take hours and date from the event
        if self.event:
            self.hours = self.event.duration_hours
            self.date = self.event.date
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.member.name} - {self.event.name} ({self.hours}h)"

class SemesterRequirement(models.Model):
    semester = models.CharField(max_length=20, unique=True)

    service_hours_required = models.IntegerField(default=0)
    comm_hours_required = models.IntegerField(default=0)
    membership_hours_required = models.IntegerField(default=0)
    finance_hours_required = models.IntegerField(default=0)
    ld_hours_required = models.IntegerField(default=0)
    chimps_required = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['semester'], name='semester_idx'),
        ]

    def __str__(self):
        return self.semester