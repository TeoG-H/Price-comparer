import requests

KAUFLAND_STORE_ID = 73267
KAUFLAND_ADDRESS_ID = 159066


def fetch_glovo_search(store_id: int, address_id: int, query: str) -> dict:
    url = f"https://api.glovoapp.com/v3/stores/{store_id}/addresses/{address_id}/search"
    params = {"query": query}
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}

    resp = requests.get(url, headers=headers, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def parse_products_simple(data: dict) -> list[dict]:
    products = []
    for block in data.get("results", []):
        for p in block.get("products", []):
            products.append({
                "name": p.get("name"),
                "price": p.get("price"),
                "image": p.get("imageUrl"),
            })
    products.sort(key=lambda x: x["price"] if x["price"] is not None else 999999)
    return products


def search_kaufland(query: str) -> list[dict]:
    raw_json = fetch_glovo_search(
        store_id=KAUFLAND_STORE_ID,
        address_id=KAUFLAND_ADDRESS_ID,
        query=query
    )
    return parse_products_simple(raw_json)
