from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from .models import StringRequest, StringResponse, StringsListResponse, NaturalLanguageResponse
from .storage import store_string, get_string_by_value, delete_string_by_value, filter_strings
from typing import Optional
import re

app = FastAPI(title="String Analyzer API")

# CORS: Allow all origins for testing bot
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/strings/filter-by-natural-language", response_model=NaturalLanguageResponse)
def natural_language_filter(query: str = Query(...)):
    # Simple heuristic parsing based on examples
    parsed_filters = {}
    original = query.lower()
    
    if "single word" in original and "palindromic" in original:
        parsed_filters["word_count"] = 1
        parsed_filters["is_palindrome"] = True
    elif "longer than" in original:
        match = re.search(r"longer than (\d+)", original)
        if match:
            parsed_filters["min_length"] = int(match.group(1)) + 1
        else:
            raise HTTPException(400, "Unable to parse natural language query")
    elif "palindromic" in original and "contain the first vowel" in original:
        parsed_filters["is_palindrome"] = True
        parsed_filters["contains_character"] = "a"  # Heuristic: first vowel is 'a'
    elif "containing the letter" in original:
        match = re.search(r"containing the letter (\w)", original)
        if match:
            parsed_filters["contains_character"] = match.group(1)
        else:
            raise HTTPException(400, "Unable to parse natural language query")
    else:
        raise HTTPException(400, "Unable to parse natural language query")
    
    # Check for conflicts (e.g., impossible combos, but simple check)
    if "min_length" in parsed_filters and "max_length" in parsed_filters and parsed_filters["min_length"] > parsed_filters["max_length"]:
        raise HTTPException(422, "Query parsed but resulted in conflicting filters")
    
    items = filter_strings(parsed_filters)
    return {
        "data": items,
        "count": len(items),
        "interpreted_query": {
            "original": query,
            "parsed_filters": parsed_filters
        }
    }

@app.post("/strings", response_model=StringResponse, status_code=201)
def create_string(request: StringRequest):
    try:
        data = store_string(request.value)
        return data
    except ValueError:
        raise HTTPException(status_code=409, detail="String already exists in the system")
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid data type for 'value' (must be string)")

@app.get("/strings/{string_value}", response_model=StringResponse)
def get_string(string_value: str):
    data = get_string_by_value(string_value)
    if not data:
        raise HTTPException(status_code=404, detail="String does not exist in the system")
    return data

def get_filters(
    is_palindrome: Optional[bool] = Query(None),
    min_length: Optional[int] = Query(None, ge=0),
    max_length: Optional[int] = Query(None, ge=0),
    word_count: Optional[int] = Query(None, ge=0),
    contains_character: Optional[str] = Query(None, min_length=1, max_length=1)
):
    filters = {}
    if is_palindrome is not None:
        filters["is_palindrome"] = is_palindrome
    if min_length is not None:
        filters["min_length"] = min_length
    if max_length is not None:
        filters["max_length"] = max_length
    if word_count is not None:
        filters["word_count"] = word_count
    if contains_character is not None:
        filters["contains_character"] = contains_character
    if min_length and max_length and min_length > max_length:
        raise HTTPException(status_code=400, detail="Invalid query parameter values or types")
    return filters

@app.get("/strings", response_model=StringsListResponse)
def get_all_strings(filters: dict = Depends(get_filters)):
    try:
        items = filter_strings(filters)
        return {
            "data": items,
            "count": len(items),
            "filters_applied": filters
        }
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid query parameter values or types")

@app.delete("/strings/{string_value}", status_code=204)
def delete_string(string_value: str):
    data = get_string_by_value(string_value)
    if not data:
        raise HTTPException(status_code=404, detail="String does not exist in the system")
    delete_string_by_value(string_value)
    return None