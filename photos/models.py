from django.db import models
from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from taskqueue import make_thumbnail

class Photo(models.Model) :
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    image = models.ImageField(upload_to='%Y/%m/%d/', blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
"""
@receiver(post_delete, sender=Photo)
def delete_attached_image(sender, **kwargs) :
    instance = kwargs.pop('instance')
    instance.image.delete(save=False)

@receiver(post_save, sender=Photo)   # 쵸. Photo model에 post_save 시그널이 감지되면 아래의 함수가 호출된다.
def make_thumbnail_image(sender, **kwargs) :
    instance = kwargs.pop('instance')
    make_thumbnail.delay(instance.image.path, 80, 80)
"""
class Comment(models.Model) :
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ForeignKey(Photo)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Like(models.Model) :
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ForeignKey(Photo)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
