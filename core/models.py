import uuid

from cloudinary_storage.storage import RawMediaCloudinaryStorage
from django.db import models
from django.urls.base import reverse

def upload_location_activity_images(instance, filename):
    file_path = 'the_'+str(filename)
    return file_path

class Record(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    voice_record = models.FileField(
        upload_to=upload_location_activity_images)
    language = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "Record"
        verbose_name_plural = "Records"

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse("core:record_detail", kwargs={"id": str(self.id)})
