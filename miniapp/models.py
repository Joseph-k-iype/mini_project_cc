from django.db import models

# Create your models here.

class upload_cheque(models.Model):
    cheque = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.cheque