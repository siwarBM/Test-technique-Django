from django.db import models

# Create your models here.
from urlshort.models import ShortURL

class ClickAnalyticManager(models.Manager):
	def click_analyse(self, instance):
		print(f'INSTANCE: {instance}')
		if isinstance(instance, ShortURL):
			try:
				obj, created = self.get_or_create(short_url=instance)
				obj.count += 1
				obj.save()
				return obj.count
			except Exception as e:
				print(e)
				
		return None


class ClickAnalytic(models.Model):
	short_url = models.OneToOneField(ShortURL, on_delete=models.CASCADE)
	count = models.IntegerField(default=0)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.count}"

	objects = ClickAnalyticManager()