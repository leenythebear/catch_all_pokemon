from django.db import models  # noqa F401


class Pokemon(models.Model):
    text = models.TextField()

    def __str__(self):
        if self:
            return self.text
        return f'{self.text}'
