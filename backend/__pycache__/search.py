import requests

# Kaufland (Glovo)
KAUFLAND_STORE_ID = 73267
KAUFLAND_ADDRESS_ID = 159066

# Carrefour (Glovo)
CARREFOUR_STORE_ID = 406498
CARREFOUR_ADDRESS_ID = 601218


def fetch_glovo_search(store_id: int, address_id: int, query: str) -> dict:
    url = f"https://api.glovoapp.com/v3/stores/{store_id}/addresses/{address_id}/search"
    params = {"query": query}
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    }

    resp = requests.get(url, headers=headers, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def parse_products_simple(data: dict, store: str) -> list[dict]:
    """
    Extrage produse din JSON + scoate dublurile pentru același magazin.
    """
    products = []
    seen = set()  # ca să nu se repete

    for block in data.get("results", []):
        for p in block.get("products", []):
            name = p.get("name")
            price = p.get("price")
            image = p.get("imageUrl")

            # cheia după care considerăm că e același produs
            key = (store, name, price, image)
            if key in seen:
                continue
            seen.add(key)

            products.append({
                "name": name,
                "price": price,
                "image": image,
                "store": store,   # ca să știi de unde e produsul
            })

    # sortare după preț
    products.sort(key=lambda x: x["price"] if x["price"] is not None else 999999)
    return products


def search_kaufland(query: str) -> list[dict]:
    raw_json = fetch_glovo_search(
        store_id=KAUFLAND_STORE_ID,
        address_id=KAUFLAND_ADDRESS_ID,
        query=query,
    )
    return parse_products_simple(raw_json, store="Kaufland")


def search_carrefour(query: str) -> list[dict]:
    raw_json = fetch_glovo_search(
        store_id=CARREFOUR_STORE_ID,
        address_id=CARREFOUR_ADDRESS_ID,
        query=query,
    )
    return parse_products_simple(raw_json, store="Carrefour")


def search_all_markets(query: str) -> list[dict]:
    """
    Combina rezultatele de la Kaufland + Carrefour și scoate dublurile.
    """
    kaufland_products = search_kaufland(query)
    carrefour_products = search_carrefour(query)

    combined = kaufland_products + carrefour_products

    unique = []
    seen = set()
    for p in combined:
        key = (p["store"], p["name"], p["price"], p["image"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(p)

    # (opțional) sortare globală după preț
    unique.sort(key=lambda x: x["price"] if x["price"] is not None else 999999)
    return unique
