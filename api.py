from cachetools import TTLCache
import aiohttp

cache = TTLCache(maxsize=100, ttl=3600)

async def get_exchange_rates():
    if "exchange_rates" in cache:
        return cache["exchange_rates"]

    url = "https://open.er-api.com/v6/latest/USD"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    dados = await response.json()
                    cache["exchange_rates"] = dados
                    return dados
                else:
                    print(f"Error: {response.status}")
                    return None

    except aiohttp.ClientError as e:
        print(f"Connection error: {e}")
        return None

async def main():
    dados = await get_exchange_rates()
    return dados
