from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Имя на русском",
    )
    title_en = models.CharField(
        max_length=200,
        verbose_name="Имя на английском",
        blank=True,
        null=True,
    )
    title_jp = models.CharField(
        max_length=200,
        verbose_name="Имя на японском",
        blank=True,
        null=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
    )
    photo = models.ImageField(
        blank=True,
        null=True,
        verbose_name="Изображение",
    )

    evolve_from = models.ForeignKey(
        "Pokemon",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="next_evolution",
        verbose_name="Предыдущая эволюция",
    )

    def __str__(self):
        if self:
            return self.title
        return f"{self.title}"


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name="Покемон",
    )

    lat = models.FloatField(verbose_name="Широта")
    lon = models.FloatField(verbose_name="Долгота")

    appeared_at = models.DateTimeField(verbose_name="Появился в")
    disappeared_at = models.DateTimeField(verbose_name="Исчез в")

    level = models.IntegerField(
        verbose_name="Уровень",
        blank=True,
        null=True,
    )
    health = models.IntegerField(
        verbose_name="Здоровье",
        blank=True,
        null=True,
    )
    strength = models.IntegerField(
        verbose_name="Сила",
        blank=True,
        null=True,
    )
    defence = models.IntegerField(
        verbose_name="Защита",
        blank=True,
        null=True,
    )
    stamina = models.IntegerField(
        verbose_name="Выносливость",
        blank=True,
        null=True,
    )

    def __str__(self):
        if self:
            return self.pokemon.title
        return f"{self.pokemon.title}"
