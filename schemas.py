"""
Database Schemas for Kensington Tutors

Each Pydantic model maps to a MongoDB collection using the lowercase
class name. These schemas validate incoming data for the API.
"""
from typing import Optional, Literal
from pydantic import BaseModel, Field, EmailStr


class Booking(BaseModel):
    """
    Collection: "booking"
    A parent or student request to book a session or consultation.
    """
    name: str = Field(..., description="Parent or student's full name")
    email: EmailStr = Field(..., description="Contact email")
    phone: Optional[str] = Field(None, description="Contact phone number")
    child_year_group: Optional[str] = Field(
        None, description="School year group (e.g., Year 5, Year 10)"
    )
    subject: str = Field(..., description="Requested subject or service")
    format: Literal["In Person", "Online"] = Field(
        "In Person", description="Preferred session format"
    )
    availability: Optional[str] = Field(
        None, description="Days/times that work for the family"
    )
    notes: Optional[str] = Field(None, description="Any extra information")
    postcode: Optional[str] = Field(
        None, description="Postcode for in-person sessions"
    )


class Contact(BaseModel):
    """
    Collection: "contact"
    A general contact or consultation enquiry.
    """
    name: str
    email: EmailStr
    message: str = Field(..., description="How we can help")
