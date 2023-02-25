from django.db import models

# Create your models here.
class patient_radiogram(models.Model):
    radiogram = models.ImageField(upload_to = 'images/')

class CT(models.Model):
    image = models.FileField(upload_to = "images/")

    # def __str__(self):
    #     return self.image


class saggital(models.Model):
    saggital_photo = models.ImageField(upload_to="saggital_images")
    