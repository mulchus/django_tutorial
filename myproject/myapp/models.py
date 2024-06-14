from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name
