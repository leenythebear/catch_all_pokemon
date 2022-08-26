import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils import timezone

from .models import Pokemon, PokemonEntity



MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
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
    try:
        searched_pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound("<h1>Такой покемон не найден</h1>")

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    img_url = request.build_absolute_uri(searched_pokemon.photo.url)
    pokemon = {
        "title_ru": searched_pokemon.title,
        "title_en": searched_pokemon.title_en,
        "title_jp": searched_pokemon.title_jp,
        "photo": img_url,
        "description": searched_pokemon.description,
    }
    pokemon_entities = PokemonEntity.objects.filter(id=searched_pokemon.id)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            img_url,
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
