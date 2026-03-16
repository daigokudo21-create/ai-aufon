
import json
import os

RESULT_FILE = "results_cache.json"

def load_results():
    if not os.path.exists(RESULT_FILE):
        return []

    try:
        with open(RESULT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_results(results):
    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
