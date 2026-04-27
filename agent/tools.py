from langchain_core.tools import tool
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    location: str = Field(..., description="City in Bangladesh, e.g., 'Coxs Bazar'")
    check_in: str = Field(..., description="Check-in date YYYY-MM-DD")
    check_out: str = Field(..., description="Check-out date YYYY-MM-DD")
    guests: int = Field(..., description="Number of guests")

@tool(args_schema=SearchInput)
def search_available_properties(location: str, check_in: str, check_out: str, guests: int) -> list[dict]:
    """Search for available rental properties."""
    return[{"property_id": 1, "name": "Ocean View", "price_per_night_bdt": 4500}]

class DetailsInput(BaseModel):
    property_id: int = Field(..., description="The ID of the property")

@tool(args_schema=DetailsInput)
def get_listing_details(property_id: int) -> dict:
    """Get detailed information, amenities, and rules for a property."""
    return {"description": "Beautiful 2-bedroom.", "amenities": ["WiFi", "AC"]}

class BookingInput(BaseModel):
    property_id: int = Field(..., description="Property ID")
    check_in: str = Field(..., description="Check-in date YYYY-MM-DD")
    check_out: str = Field(..., description="Check-out date YYYY-MM-DD")
    guests: int = Field(..., description="Number of guests")

@tool(args_schema=BookingInput)
def create_booking(property_id: int, check_in: str, check_out: str, guests: int) -> dict:
    """Create a booking. Use ONLY after guest confirms pricing and dates."""
    return {"booking_ref": "BKG-123", "total_price_bdt": 9000}

stay_ease_tools =[search_available_properties, get_listing_details, create_booking]