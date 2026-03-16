import json
import os

RESULTS_FILE = "results.json"

def save_results(results):
    try:
        print(f"[result_store] save_results count={len(results)}")
        with open(RESULTS_FILE, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[result_store] save error: {e}")

def load_results():
    try:
        if not os.path.exists(RESULTS_FILE):
            print("[result_store] results.json not found")
            return []

        with open(RESULTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            print("[result_store] results.json is not a list")
            return []

        print(f"[result_store] load_results count={len(data)}")
        return data
    except Exception as e:
        print(f"[result_store] load error: {e}")
        return []
