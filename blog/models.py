from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

## Encapsulation of the Post Model which represents files in the CodeFiles Directory.
class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	##String Representation
	def __str__(self):
		return self.title

	## url representation for the file detail view
	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})
