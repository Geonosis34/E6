from django.contrib.auth.models import User
from django.db import models
from PIL import Image
from api.models import Room


class Profile(models.Model):
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)
    avatar = models.ImageField(
        default='img/profile/default.png', upload_to='img/profile')
    bio = models.TextField()
    is_online = models.BooleanField(default=False)

    def get_chats(self):
        chats = set()
        for chat in Room.objects.all():
            if self.user in chat.members.all():
                chats.add(chat)
        return chats

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
