import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(BASE_DIR, "app_data.json")


def _load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ---------- SAVED PLACES ----------

def load_saved_places():
    data = _load_data()
    return data.get("saved_places", [])


def save_saved_places(places):
    data = _load_data()
    data["saved_places"] = places
    data["last_updated"] = datetime.now().isoformat()
    _save_data(data)


# ---------- CHAT  ----------

def load_chat_history():
    data = _load_data()
    return data.get("chat_history", [])


def save_chat_history(chat):
    data = _load_data()
    data["chat_history"] = chat
    data["last_updated"] = datetime.now().isoformat()
    _save_data(data)
