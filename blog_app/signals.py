from django.dispatch import receiver
from django.db.models.signals import post_delete
from blog_app.models import Blog
import os

@receiver(post_delete, sender=Blog)
def delete_associated_image(sender, instance, **kwargs):
    if instance.featured_image:
        if os.path.isfile(instance.featured_image.path):
            os.remove(instance.featured_image.path)

