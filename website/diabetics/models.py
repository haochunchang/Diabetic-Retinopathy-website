from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
import os

# Create your models here.
class ImageName(models.Model):

    def get_image_path(self, filename):
        return filename

    imagename = models.CharField(max_length=200)
    result = models.CharField(max_length=20, null=True)       
    image = models.ImageField(upload_to=get_image_path, null=True)    
    
    def __str__(self):
        return self.imagename + ": " + self.result

class Severity(models.Model):
    imagename = models.ForeignKey(ImageName, on_delete=models.CASCADE)
    nodr = models.DecimalField(max_digits=20, decimal_places=15)
    mild = models.DecimalField(max_digits=20, decimal_places=15)
    moderate = models.DecimalField(max_digits=20, decimal_places=15)
    severe = models.DecimalField(max_digits=20, decimal_places=15)
    proliferative = models.DecimalField(max_digits=20, decimal_places=15)

    def __str__(self):
        return str(self.imagename) + "\n" \
                "No DR: " + str(self.nodr) + "\n"\
                "Mild: " + str(self.mild) + "\n"\
                "Moderate: " + str(self.moderate) + "\n"\
                "Severe: " + str(self.severe) + "\n"\
                "Proliferative: " + str(self.proliferative)

# These two auto-delete files from filesystem when they are unneeded:
@receiver(models.signals.post_delete, sender=ImageName)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(models.signals.pre_save, sender=ImageName)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `MediaFile` object is changed.
    """
    if not instance.pk:
        return False

    try:
        old_file = ImageName.objects.get(pk=instance.pk).image
    except ImageName.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
