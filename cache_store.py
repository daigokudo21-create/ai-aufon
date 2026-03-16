import json
import os
import time

CACHE_FILE = "mercari_cache.json"
CACHE_TTL = 3600

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_cache(data):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_cached_price(model):
    data = load_cache()
    item = data.get(model)

    if not item:
        return None

    if time.time() - item.get("updated_at", 0) > CACHE_TTL:
        return None

    return item.get("price")

def set_cached_price(model, price):
    data = load_cache()
    data[model] = {
        "price": price,
        "updated_at": time.time()
    }
    save_cache(data)
