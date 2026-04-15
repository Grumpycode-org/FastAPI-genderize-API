from fastapi import FastAPI, HTTPException, Query  # Import FastAPI tools
from typing import Optional  # For Optional[str]
from app.services.gender_service import get_gender_data  # Service layer
from app.utils.helpers import get_utc_timestamp  # Timestamp helper

from fastapi.middleware.cors import CORSMiddleware  # CORS middleware



# Create FastAPI app
app = FastAPI()

# Enable CORS (required for grading)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define GET Endpoint: /api/classify
@app.get("/api/classify")
async def classify(name: Optional[str] = Query(default=None)):

    # ---------------------------
    # INPUT VALIDATION
    # ---------------------------

    # Check if name is missing or empty
    # Missing or empty name → 400/422
    if name is None or name.strip() == "":
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "message": "Name parameter is required"
            }
        )

    # Reject names with digits (invalid type/content) → 422
    if any(ch.isdigit() for ch in name):
        raise HTTPException(
            status_code=422,
            detail={
                "status": "error",
                "message": "Invalid name parameter: must not contain digits"
            }
        )
 
    # ---------------------------
    # SERVICE CALL
    # ---------------------------

    try:
        result = get_gender_data(name)
    except Exception as e:
        print(f"Error calling external API: {e}")
        raise HTTPException(
            status_code=502,
            detail={
                "status": "error",
                "message": "External API error"
            }
        )

    # ---------------------------
    # EDGE CASE HANDLING
    # ---------------------------

    # If Genderize returns no prediction
    # if result is None:
    #     raise HTTPException(
    #         status_code=400,
    #         detail={
    #             "status": "error",
    #             "message": "No prediction available for the provided name"
    #         }
    #     )
        
    if not result or result.get("gender") is None or result.get("count") == 0:
        return {
            "status": "success",
            "data": {
                "name": name,
                "gender": None,
                "probability": 0,
                "sample_size": 0,
                "is_confident": False,
                "processed_at": get_utc_timestamp(),
            },
        }

    # ---------------------------
    # FINAL RESPONSE
    # ---------------------------

    return {
        "status": "success",
        "data": {
            **result,  # unpack service data
            "processed_at": get_utc_timestamp()  # add timestamp
        }
    }



async def classify_data(name: str):
    if not name:
        raise HTTPException(status_code=400, detail="Name is required")