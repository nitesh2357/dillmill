from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name='First Name', max_length=255, blank=True)
    last_name = models.CharField(verbose_name='Last Name', max_length=255, blank=True)
    email = models.EmailField(verbose_name='User Email', max_length=254, blank=True)
    gender = models.CharField(verbose_name='Gender', null=True, blank=True, max_length=10)
    bio = models.TextField(verbose_name='Description', blank=True, default='')
    age = models.PositiveSmallIntegerField(verbose_name='Age', null=True)
    created = models.DateTimeField(null=True, default=timezone.now)
    modified = models.DateTimeField(verbose_name='Last Updated', null=True, default=timezone.now)


class Preference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    max_distance = models.PositiveIntegerField(verbose_name='Maximun distance in search', null=True, blank=True)
    min_age = models.PositiveSmallIntegerField(verbose_name='Minumum age in search', null=True, blank=True)
    max_age = models.PositiveSmallIntegerField(verbose_name='Maximun age in search', null=True, blank=True)
    sex = models.CharField(verbose_name='Gender', blank=True, max_length=10)


class Action(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    other_person_user_id = models.IntegerField(verbose_name='Liked Person User ID')
    like = models.BooleanField(verbose_name='Like or Dislike')
    matched = models.BooleanField(verbose_name='Matched if other person also like', default=False)
    created = models.DateTimeField(verbose_name='Liked or Disliked', null=True, default=timezone.now)
    modified = models.DateTimeField(verbose_name='Match or Unmatched', null=True, default=timezone.now)

    class Meta:
        unique_together = (('user', 'other_person_user_id'),)

class Location(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitudes = models.FloatField(verbose_name='Current Location Latidue')
    longitudes = models.FloatField(verbose_name='Current Location longitude')


# Create a user profile and user preference everytime a user signup
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        Preference.objects.create(user=instance)

