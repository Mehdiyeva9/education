from django.db import models
from tinymce.models import HTMLField

class Resource(models.Model):
    title = models.CharField(max_length=50)
    context = models.TextField()
    image = models.ImageField(upload_to="edu_photos/")
    created_by = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    
class HelpForm(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mail = models.EmailField(max_length=256)
    text = models.TextField()

    def __str__(self):
        return self.text[0:50]
    
class SiteSettings(models.Model):
    banner_title = models.CharField(max_length=50, blank=True, null=True)
    banner_text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="edu_photos/", blank=True, null=True)
    subscribe_mail = models.EmailField(max_length=256, blank=True, null=True)
    terms_title = models.CharField(max_length=100, blank=True, null=True)
    terms_content = HTMLField(blank=True, null=True)
    terms_created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    privacy_title = models.CharField(max_length=100, blank=True, null=True)
    privacy_content = HTMLField(blank=True, null=True)
    privacy_created_at = models.DateField(auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Site Settings'

    def save(self, *args, **kwargs):
        if not self.id and SiteSettings.objects.exists():
            return None
        return super(SiteSettings,self).save(*args,**kwargs)

    def __str__ (self):
        return "Setting"