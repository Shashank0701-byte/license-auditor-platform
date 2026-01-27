from django.db import models


class Scan(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total_packages = models.IntegerField()
    license_risks = models.IntegerField()
    abandoned_packages = models.IntegerField()

    def __str__(self):
        return f"Scan {self.id} - {self.created_at}"


class PackageRisk(models.Model):
    scan = models.ForeignKey(Scan, on_delete=models.CASCADE, related_name="packages")
    name = models.CharField(max_length=255)
    license = models.CharField(max_length=255, null=True, blank=True)
    last_updated = models.CharField(max_length=255, null=True, blank=True)
    risks = models.JSONField(default=list)

    def __str__(self):
        return f"{self.name} ({self.risks})"
