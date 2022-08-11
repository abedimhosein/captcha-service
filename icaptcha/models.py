import io
import os
import random
import string
import sys
from uuid import uuid4

from captcha.image import ImageCaptcha
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models


def upload_any_path(root_dir: str, file_path: str):
    _, ext = os.path.splitext(os.path.basename(file_path))
    file_path = f'{random_string_generator(16)}{ext}'
    return os.path.join(root_dir, file_path)


def random_string_generator(size: int = 10, population: str = string.ascii_letters + string.digits):
    return ''.join(random.choices(population, k=size))


def captcha_upload_path(instance, *args):
    return upload_any_path(
        root_dir=os.path.join(settings.MEDIA_ROOT, 'captcha'),
        file_path=f"{random_string_generator()}.jpg"
    )


class CaptchaManager(models.Manager):
    def create(self):
        pri_id = random_string_generator(size=6)

        image = ImageCaptcha(width=280, height=80)
        image.generate_image(pri_id)
        memory_buffer = io.BytesIO()
        image.write(pri_id, output=memory_buffer, format='JPEG')

        image_on_memory = InMemoryUploadedFile(
            file=memory_buffer,
            field_name='ImageField',
            name='captcha.jpg',
            content_type='JPEG',
            size=sys.getsizeof(image),
            charset=None,
        )

        return super().create(pri_id=pri_id, image=image_on_memory)

    def get_by_pub_id(self, pub_id: str):
        return self.get_queryset().filter(pub_id=pub_id).first()


class Captcha(models.Model):
    pub_id = models.UUIDField(default=uuid4, primary_key=True)
    pri_id = models.CharField(max_length=255)
    image = models.ImageField(upload_to=captcha_upload_path, max_length=255)

    objects = CaptchaManager()
