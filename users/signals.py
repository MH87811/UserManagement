from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def assign_supervisor(sender, instance, created, **kwargs):
    if not created:
        return
    candidate = User.objects.filter(
        department=instance.department,
        role__priority__gt=instance.role.priority).order_by('role__priority').exclude(id=instance.id)

    supervisor = candidate.first()

    if supervisor:
        instance.supervisor = supervisor
    instance.save()