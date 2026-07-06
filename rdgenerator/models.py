from django.db import models

class GithubRun(models.Model):
    id = models.IntegerField(verbose_name="ID",primary_key=True)
    uuid = models.CharField(verbose_name="uuid", max_length=100)
    status = models.CharField(verbose_name="status", max_length=100)
    github_run_id = models.BigIntegerField(null=True, blank=True)
    platform = models.CharField(verbose_name="platform", max_length=50, null=True, blank=True)
    filename = models.CharField(verbose_name="filename", max_length=200, null=True, blank=True)
