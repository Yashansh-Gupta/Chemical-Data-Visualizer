from django.db import models

class Dataset(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="datasets/", null=True, blank=True)
    summary = models.JSONField()
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
