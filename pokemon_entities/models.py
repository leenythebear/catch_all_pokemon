from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.TextField()
    photo = models.ImageField(blank=True, null=True)

    def __str__(self):
        if self:
            return self.title
        return f'{self.title}'


class PokemonEntity(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
