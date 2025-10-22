from typing import Dict, List
from datetime import datetime
import hashlib
from collections import Counter

storage: Dict[str, Dict] = {}  # hash -> StringResponse dict

def compute_properties(value: str) -> Dict:
    length = len(value)
    lower_value = value.lower()
    is_palindrome = lower_value == lower_value[::-1]
    unique_characters = len(set(value))
    word_count = len(value.split())
    sha256_hash = hashlib.sha256(value.encode()).hexdigest()
    character_frequency_map = dict(Counter(value))
    return {
        "length": length,
        "is_palindrome": is_palindrome,
        "unique_characters": unique_characters,
        "word_count": word_count,
        "sha256_hash": sha256_hash,
        "character_frequency_map": character_frequency_map
    }

def store_string(value: str) -> Dict:
    props = compute_properties(value)
    hash_id = props["sha256_hash"]
    if hash_id in storage:
        raise ValueError("String already exists")
    created_at = datetime.utcnow()
    data = {
        "id": hash_id,
        "value": value,
        "properties": props,
        "created_at": created_at
    }
    storage[hash_id] = data
    return data

def get_string_by_value(value: str) -> Dict:
    hash_id = hashlib.sha256(value.encode()).hexdigest()
    return storage.get(hash_id)

def delete_string_by_value(value: str) -> None:
    hash_id = hashlib.sha256(value.encode()).hexdigest()
    if hash_id in storage:
        del storage[hash_id]

def get_all_strings() -> List[Dict]:
    return list(storage.values())

# Helper for filtering
def filter_strings(filters: Dict) -> List[Dict]:
    items = get_all_strings()
    if "is_palindrome" in filters:
        items = [i for i in items if i["properties"]["is_palindrome"] == filters["is_palindrome"]]
    if "min_length" in filters:
        items = [i for i in items if i["properties"]["length"] >= filters["min_length"]]
    if "max_length" in filters:
        items = [i for i in items if i["properties"]["length"] <= filters["max_length"]]
    if "word_count" in filters:
        items = [i for i in items if i["properties"]["word_count"] == filters["word_count"]]
    if "contains_character" in filters:
        char = filters["contains_character"].lower()
        items = [i for i in items if char in i["value"].lower()]
    return items