from django.contrib.auth import get_user_model
from django.db import models
from PIL import Image

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=120, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    role = models.CharField(max_length=30, blank=True, null=True)
    image = models.ImageField(default='avatar.jpg', upload_to='profile_images')
    last_updated = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

