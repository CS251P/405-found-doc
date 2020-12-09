from django.db import models
from django.contrib.auth.models import User
from PIL import Image
##This is an encapsulation of the User Profile Model which represents each user in the server uniquely.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, *args, **kawrgs):
		super().save(*args, **kawrgs)

		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)

##This class is an encapsulation of the editor.
class Snippet(models.Model):
	text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ('-created_at', )
