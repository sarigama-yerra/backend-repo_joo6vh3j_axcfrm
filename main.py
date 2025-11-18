import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict

from database import db, create_document, get_documents
from schemas import Booking, Contact

app = FastAPI(title="Kensington Tutors API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "service": "kensington-tutors"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set",
        "database_name": "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": [],
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["connection_status"] = "Connected"
            try:
                response["collections"] = db.list_collection_names()[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response


# Public endpoints for booking and contact submissions
@app.post("/api/book", status_code=201)
def create_booking(payload: Booking) -> Dict[str, Any]:
    try:
        booking_id = create_document("booking", payload)
        return {"id": booking_id, "message": "Booking request received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/contact", status_code=201)
def create_contact(payload: Contact) -> Dict[str, Any]:
    try:
        contact_id = create_document("contact", payload)
        return {"id": contact_id, "message": "Thanks for reaching out"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Simple list endpoints (admin/read-only preview)
@app.get("/api/bookings")
def list_bookings(limit: int = 50):
    try:
        docs = get_documents("booking", {}, limit)
        # Convert ObjectId to string
        for d in docs:
            if "_id" in d:
                d["_id"] = str(d["_id"])
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/contacts")
def list_contacts(limit: int = 50):
    try:
        docs = get_documents("contact", {}, limit)
        for d in docs:
            if "_id" in d:
                d["_id"] = str(d["_id"])
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
