from django.contrib.auth import get_user_model
from django.db import models

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


class DeliveryAddress(models.Model):
    STATE_CHOICES = [
        ('Abia', 'Abia'),
        ('Adamawa', 'Adamawa'),
        ('Akwa Ibom', 'Akwa Ibom'),
        ('Anambra ', 'Anambra '),
        ('Bauchi', 'Bauchi'),
        ('Bayelsa', 'Bayelsa'),
        ('Benue ', 'Benue '),
        ('Borno', 'Borno'),
        ('Cross River', 'Cross River'),
        ('Delta', 'Delta'),
        ('Ebonyi', 'Ebonyi'),
        ('Edo', 'Edo'),
        ('Ekiti', 'Ekiti'),
        ('Enugu', 'Enugu'),
        ('Gombe', 'Gombe'),
        ('Imo', 'Imo'),
        ('Jigawa', 'Jigawa'),
        ('Kaduna', 'Kaduna'),
         ('Kano', 'Kano'),
        ('Katsina', 'Katsina'),
        ('Kebbi', 'Kebbi'),
        ('Kogi', 'Kogi'),
        ('Kwara', 'Kwara'),
        ('Lagos', 'Lagos'),
        ('Abuja-FCT', 'Abuja-FCT'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    State = models.CharField(max_length=30, choices=STATE_CHOICES)
    Town = models.CharField(max_length=20, blank=True, null=True)
    Address = models.CharField(max_length=120, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
