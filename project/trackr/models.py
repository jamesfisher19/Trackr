from django.db import models
from django.conf import settings
from django.utils import timezone

class Job(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jobs')
    company_name = models.CharField(max_length=100)
    position_title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    application_link = models.URLField()
    deadline = models.DateField()
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('not_applied', 'Not Applied'),
    )
    applied_status = models.BooleanField(default=False)
    def get_applied_status_display(self):
        return "Applied" if self.applied_status else "Not Applied"
    def __str__(self):
        return f"{self.position_title} at {self.company_name}"
