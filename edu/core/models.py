from django.db import models

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
    
