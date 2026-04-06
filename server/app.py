from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Hospital Triage AI", version="1.0.0")

class PredictRequest(BaseModel):
    symptoms: str

class PredictResponse(BaseModel):
    action: str

def analyze_symptoms(symptoms: str) -> str:
    """
    Simple rule-based symptom analysis.
    """
    symptoms_lower = symptoms.lower()
    
    # Critical symptoms requiring immediate attention
    critical_keywords = [
        "chest pain", "heart attack", "stroke", "unconscious", 
        "difficulty breathing", "shortness of breath", "severe bleeding",
        "loss of consciousness", "confusion", "seizure"
    ]
    
    # Moderate symptoms requiring monitoring
    moderate_keywords = [
        "fever", "pain", "headache", "dizziness", "nausea",
        "vomiting", "diarrhea", "dehydration", "infection",
        "wheezing", "asthma", "high blood pressure"
    ]
    
    # Check for critical symptoms first
    for keyword in critical_keywords:
        if keyword in symptoms_lower:
            return "TREAT_NOW"
    
    # Check for moderate symptoms
    for keyword in moderate_keywords:
        if keyword in symptoms_lower:
            return "MONITOR"
    
    # Default to wait for mild symptoms
    return "WAIT"

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    """
    Predict triage action based on symptoms.
    
    Args:
        request: JSON with symptoms field
        
    Returns:
        Predicted triage action
    """
    if not request.symptoms or not request.symptoms.strip():
        raise HTTPException(status_code=400, detail="Symptoms cannot be empty")
    
    try:
        action = analyze_symptoms(request.symptoms)
        return PredictResponse(action=action)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/health")
async def health():
    """Detailed health check."""
    return {
        "status": "healthy",
        "service": "Hospital Triage AI",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
