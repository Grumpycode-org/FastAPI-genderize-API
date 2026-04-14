"""
PURPOSE:
Handles all business logic:
- Calls Genderize API
- Processes response
- Applies confidence logic
"""

import requests

Genderize_url = "https://api.genderize.io"

def get_gender_data(name: str):
    """
    PURPOSE:
    Handles all business logic:
    - Calls Genderize API
    - Processes response
    - Applies confidence logic
    """

    # call Genderize API
    response = requests.get(Genderize_url,
        params={"name":name},
        timeout=2
    )

    #Check if API call failed
    if response.status_code != 200:
        raise Exception("External API Error")
    
    #Convert response to JSON
    data = response.json()

    if data.get("gender") is None or data.get("count") == 0:
        return None
    
    gender = data.get("gender"),
    probability = data.get("probability")
    sample_size = data.get("count")

    #comput confidence
    is_confident = (
        probability >= 0.7 and 
        sample_size >= 100
    )

    return {
        "name": name,
        "gender": gender,
        "probability": probability,
        "sample_size": sample_size,
        "is_confident": is_confident
    }
    