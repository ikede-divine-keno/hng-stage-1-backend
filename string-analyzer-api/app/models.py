from pydantic import BaseModel, Field
from typing import Dict, Optional, Union
from datetime import datetime

class StringRequest(BaseModel):
    value: str = Field(..., min_length=1)  # Required, non-empty string

class StringProperties(BaseModel):
    length: int
    is_palindrome: bool
    unique_characters: int
    word_count: int
    sha256_hash: str
    character_frequency_map: Dict[str, int]

class StringResponse(BaseModel):
    id: str
    value: str
    properties: StringProperties
    created_at: datetime

class StringsListResponse(BaseModel):
    data: list[StringResponse]
    count: int
    filters_applied: Optional[Dict[str, Union[str, int, bool]]] = None  # Changed 'any' to 'Union[str, int, bool]'

class NaturalLanguageResponse(StringsListResponse):
    interpreted_query: Dict[str, Union[str, Dict[str, Union[str, int, bool]]]]  # Updated