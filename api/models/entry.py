from pydantic import BaseModel
from typing import List, Dict

# pydantic modeling - !important: data types must match target JSON dataset 

# IBJJF dataset 
# class Entry(BaseModel):
#     id: int
#     name: str
#     federationAbbr: str
#     country: str
#     countryAbbr: str
#     city: str
#     responsible: str
#     address: str
#     website: str | None = None

# class EntryList(BaseModel):
#     data: List[Entry]


# Custom dataset
class Properties(BaseModel):
    id: int
    name: str
    city: str
    state: str | None = None
    stateAbbr: str
    country: str
    address: str
    website: str | None = None

class Geometry(BaseModel):
    type: str
    coordinates: list
    mapCoordinates: list

class Entry(BaseModel):
    type: str
    properties: Properties
    geometry: Geometry
    
class EntryList(BaseModel):
    data: List[Entry]