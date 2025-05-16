from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    USER_TYPES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    address_line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    photo = models.ImageField(upload_to="pics/", blank=True, null=True)
    # images=models.ImageField(upload_to='photos', default='default.jpg')

    def __str__(self):
        return f"{self.user.username} ({self.user_type})"
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
