from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def crear_grupos(sender, **kwargs):
    if sender.name != "core":
        return

    for nombre in ("admin", "normal", "viewer"):
        Group.objects.get_or_create(name=nombre)
