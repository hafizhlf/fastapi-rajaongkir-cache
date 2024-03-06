import os
from typing import Dict, Optional
from datetime import datetime, timedelta
import httpx
import json
from fastapi import FastAPI, HTTPException

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

RAJAONGKIR_API_KEY = os.getenv("RAJAONGKIR_API_KEY")
if RAJAONGKIR_API_KEY is None:
    raise EnvironmentError("RAJAONGKIR_API_KEY environment variable is not set")

RAJAONGKIR_BASE_URL = 'https://pro.rajaongkir.com/api'
CACHE_EXPIRATION_TIME = timedelta(days=1)

app = FastAPI()
cache: Dict[str, tuple[dict, datetime]] = {}


def get_from_cache(key: str) -> Optional[dict]:
    if key in cache:
        data, timestamp = cache[key]
        if datetime.now() - timestamp < CACHE_EXPIRATION_TIME:
            return data
    return None


def cache_data(key: str, data: dict) -> None:
    cache[key] = (data, datetime.now())


async def get_shipping_cost(origin: int, destination: int, weight: int, courier: str) -> dict:
    cache_key = f"shipping_cost_{origin}_{destination}_{weight}_{courier}"
    shipping_cost = get_from_cache(cache_key)
    if shipping_cost is not None:
        return shipping_cost

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{RAJAONGKIR_BASE_URL}/cost",
                headers={"key": RAJAONGKIR_API_KEY},
                data={"origin": origin, "originType": "city", "destination": destination, "destinationType": "city", "weight": weight, "courier": courier}
            )
            response.raise_for_status()
            shipping_cost = response.json()
            cache_data(cache_key, shipping_cost)
            return shipping_cost
    except (httpx.HTTPError, json.JSONDecodeError, httpx.InvalidURL) as e:
        raise HTTPException(status_code=500, detail=f"Error fetching shipping cost: {str(e)}")


async def get_provinces() -> dict:
    cache_key = "provinces"
    provinces = get_from_cache(cache_key)
    if provinces is not None:
        return provinces

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{RAJAONGKIR_BASE_URL}/province",
                headers={"key": RAJAONGKIR_API_KEY}
            )
            response.raise_for_status()
            provinces = response.json()
            cache_data(cache_key, provinces)
            return provinces
    except (httpx.HTTPError, json.JSONDecodeError, httpx.InvalidURL) as e:
        raise HTTPException(status_code=500, detail=f"Error fetching provinces: {str(e)}")


async def get_cities_in_province(province_id: int) -> dict:
    cache_key = f"cities_in_province_{province_id}"
    cities = get_from_cache(cache_key)
    if cities is not None:
        return cities

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{RAJAONGKIR_BASE_URL}/city",
                headers={"key": RAJAONGKIR_API_KEY},
                params={"province": province_id}
            )
            response.raise_for_status()
            cities = response.json()
            cache_data(cache_key, cities)
            return cities
    except (httpx.HTTPError, json.JSONDecodeError, httpx.InvalidURL) as e:
        raise HTTPException(status_code=500, detail=f"Error fetching cities in province: {str(e)}")


async def get_all_cities() -> dict:
    cache_key = "cities"
    cities = get_from_cache(cache_key)
    if cities is not None:
        return cities

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{RAJAONGKIR_BASE_URL}/city",
                headers={"key": RAJAONGKIR_API_KEY}
            )
            response.raise_for_status()
            cities = response.json()
            cache_data(cache_key, cities)
            return cities
    except (httpx.HTTPError, json.JSONDecodeError, httpx.InvalidURL) as e:
        raise HTTPException(status_code=500, detail=f"Error fetching all cities: {str(e)}")


async def get_subdistricts(city_id: int) -> dict:
    cache_key = f"subdistricts_{city_id}"
    subdistricts = get_from_cache(cache_key)
    if subdistricts is not None:
        return subdistricts

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{RAJAONGKIR_BASE_URL}/subdistrict",
                headers={"key": RAJAONGKIR_API_KEY},
                params={"city": city_id}
            )
            response.raise_for_status()
            subdistricts = response.json()
            cache_data(cache_key, subdistricts)
            return subdistricts
    except (httpx.HTTPError, json.JSONDecodeError, httpx.InvalidURL) as e:
        raise HTTPException(status_code=500, detail=f"Error fetching subdistricts: {str(e)}")


@app.get("/shipping-cost/")
async def calculate_shipping_cost(origin: int, destination: int, weight: int, courier: str):
    """
    Calculates shipping cost based on origin, destination, weight, and courier.
    """
    shipping_cost = await get_shipping_cost(origin, destination, weight, courier)
    return shipping_cost


@app.get("/provinces/")
async def list_provinces():
    """
    Lists all provinces.
    """
    provinces = await get_provinces()
    return provinces


@app.get("/cities/{province_id}")
async def list_cities(province_id: int):
    """
    Lists all cities in a given province.
    """
    cities = await get_cities_in_province(province_id)
    return cities


@app.get("/cities/")
async def list_all_cities():
    """
    Lists all cities.
    """
    cities = await get_all_cities()
    return cities


@app.get("/subdistricts/{city_id}")
async def list_subdistricts(city_id: int):
    """
    Lists all subdistricts in a given city.
    """
    subdistricts = await get_subdistricts(city_id)
    return subdistricts
