import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Pokemon, PokemonEntity



MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision"
    "/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832"
    "&fill=transparent"
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons_entities = PokemonEntity.objects.filter(
        appeared_at__lt=timezone.localtime(),
        disappeared_at__gt=timezone.localtime(),
    )
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons_entities:
        img_url = request.build_absolute_uri(pokemon_entity.pokemon.photo.url)
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            img_url,
        )
    pokemons_above_the_map = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons_above_the_map:
        if pokemon.photo:
            img_url = request.build_absolute_uri(pokemon.photo.url)
            pokemons_on_page.append(
                {
                    "pokemon_id": pokemon.id,
                    "img_url": img_url,
                    "title_ru": pokemon.title,
                }
            )

    return render(
        request,
        "mainpage.html",
        context={
            "map": folium_map._repr_html_(),
            "pokemons": pokemons_on_page,
        },
    )


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    img_url = request.build_absolute_uri(pokemon.photo.url)
    serialized_pokemon = {
        "title_ru": pokemon.title,
        "title_en": pokemon.title_en,
        "title_jp": pokemon.title_jp,
        "img_url": img_url,
        "description": pokemon.description,
    }
    pokemon_entities = pokemon.entities.all()
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            img_url,
        )
    if pokemon.evolve_from:
        previous_evolution = {
            "title_ru": pokemon.evolve_from.title,
            "pokemon_id": pokemon.evolve_from.id,
            "img_url": request.build_absolute_uri(
                pokemon.evolve_from.photo.url
            ),
        }
        serialized_pokemon["previous_evolution"] = previous_evolution
    next_evolution = pokemon.next_evolutions.all()
    if next_evolution:
        next_evolution = {
            "title_ru": next_evolution[0].title,
            "pokemon_id": next_evolution[0].id,
            "img_url": next_evolution[0].photo.url,
        }
        serialized_pokemon["next_evolution"] = next_evolution

    return render(
        request,
        "pokemon.html",
        context={
            "img_url": img_url,
            "map": folium_map._repr_html_(),
            "pokemon": serialized_pokemon,
        },
    )
