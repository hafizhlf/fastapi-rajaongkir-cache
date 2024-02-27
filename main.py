import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import httpx
import time

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Retrieve API key from environment variable
RAJAONGKIR_API_KEY = os.getenv("RAJAONGKIR_API_KEY")
if RAJAONGKIR_API_KEY is None:
    raise EnvironmentError("RAJAONGKIR_API_KEY environment variable is not set")

RAJAONGKIR_BASE_URL = 'https://pro.rajaongkir.com/api'

cache = {}

def get_from_cache_with_timestamp(key):
    if key in cache:
        data, timestamp = cache[key]
        # Check if data is older than one day (86400 seconds)
        if time.time() - timestamp > 86400:
            # Invalidate cache if data is older than one day
            del cache[key]
            return None
        return data
    else:
        return None

def cache_data_with_timestamp(key, data):
    timestamp = time.time()
    cache[key] = (data, timestamp)

async def get_shipping_cost(origin: str, destination: str, weight: int, courier: str) -> dict:
    cache_key = f"shipping_cost_{origin}_{destination}_{weight}_{courier}"
    shipping_cost = get_from_cache_with_timestamp(cache_key)
    if shipping_cost is not None:
        return shipping_cost
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{RAJAONGKIR_BASE_URL}/cost",
            headers={"key": RAJAONGKIR_API_KEY},
            data={"origin": origin, "originType": "city", "destination": destination, "destinationType": "city", "weight": weight, "courier": courier}
        )
        if response.status_code == 200:
            shipping_cost = response.json()
            cache_data_with_timestamp(cache_key, shipping_cost)
            return shipping_cost
        else:
            raise HTTPException(status_code=response.status_code, detail="RajaOngkir API error")

async def get_provinces() -> dict:
    cache_key = "provinces"
    provinces = get_from_cache_with_timestamp(cache_key)
    if provinces is not None:
        return provinces
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{RAJAONGKIR_BASE_URL}/province",
            headers={"key": RAJAONGKIR_API_KEY}
        )
        if response.status_code == 200:
            provinces = response.json()
            cache_data_with_timestamp(cache_key, provinces)
            return provinces
        else:
            raise HTTPException(status_code=response.status_code, detail="RajaOngkir API error")

async def get_cities_in_province(province_id: int) -> dict:
    cache_key = f"cities_in_province_{province_id}"
    cities = get_from_cache_with_timestamp(cache_key)
    if cities is not None:
        return cities
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{RAJAONGKIR_BASE_URL}/city",
            headers={"key": RAJAONGKIR_API_KEY},
            params={"province": province_id}
        )
        if response.status_code == 200:
            cities = response.json()
            cache_data_with_timestamp(cache_key, cities)
            return cities
        else:
            raise HTTPException(status_code=response.status_code, detail="RajaOngkir API error")

async def get_all_cities() -> dict:
    cache_key = "cities"
    cities = get_from_cache_with_timestamp(cache_key)
    if cities is not None:
        return cities
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{RAJAONGKIR_BASE_URL}/city",
            headers={"key": RAJAONGKIR_API_KEY}
        )
        if response.status_code == 200:
            cities = response.json()
            cache_data_with_timestamp(cache_key, cities)
            return cities
        else:
            raise HTTPException(status_code=response.status_code, detail="RajaOngkir API error")

async def get_subdistricts(city_id: int) -> dict:
    cache_key = f"subdistricts_{city_id}"
    subdistricts = get_from_cache_with_timestamp(cache_key)
    if subdistricts is not None:
        return subdistricts
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{RAJAONGKIR_BASE_URL}/subdistrict",
            headers={"key": RAJAONGKIR_API_KEY},
            params={"city": city_id}
        )
        if response.status_code == 200:
            subdistricts = response.json()
            cache_data_with_timestamp(cache_key, subdistricts)
            return subdistricts
        else:
            raise HTTPException(status_code=response.status_code, detail=f"RajaOngkir API error")

@app.get("/shipping-cost/")
async def calculate_shipping_cost(origin: str, destination: str, weight: int, courier: str):
    shipping_cost = await get_shipping_cost(origin, destination, weight, courier)
    return shipping_cost

@app.get("/provinces/")
async def list_provinces():
    provinces = await get_provinces()
    return provinces

@app.get("/cities/{province_id}")
async def list_cities(province_id: int):
    cities = await get_cities_in_province(province_id)
    return cities

@app.get("/cities/")
async def list_all_cities():
    cities = await get_all_cities()
    return cities

@app.get("/subdistricts/{city_id}")
async def list_subdistricts(city_id: int):
    subdistricts = await get_subdistricts(city_id)
    return subdistricts
