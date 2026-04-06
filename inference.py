import os
import json
import uuid
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from hospital_env import HospitalTriageEnv, Action, ActionType, Observation

# Global variables
env = None
current_observation = None

# FastAPI app
app = FastAPI(
    title="Hospital Triage API",
    docs_url="/docs",   # enable docs
    redoc_url="/redoc"
)

# Request/Response models
class StepRequest(BaseModel):
    action: str
    priority_score: float
    reasoning: str

class StepResponse(BaseModel):
    reward: float
    done: bool
    info: Dict[str, Any]

class StateResponse(BaseModel):
    patient_id: str
    symptoms: List[str]

class ResetResponse(BaseModel):
    status: str

def rule_based_triage(observation: Observation) -> Action:
    """
    Rule-based triage decision without calling OpenAI API.
    """
    symptoms_lower = [s.lower() for s in observation.symptoms]
    vitals = observation.vitals
    
    # Critical conditions - TREAT_NOW
    critical_symptoms = {
        "chest pain", "unconscious", "loss of consciousness", 
        "difficulty breathing", "shortness of breath", "severe bleeding",
        "stroke", "heart attack", "confusion"
    }
    
    if any(symptom in symptoms_lower for symptom in critical_symptoms):
        return Action(
            action_type=ActionType.TREAT_NOW,
            priority_score=0.9,
            reasoning="Critical symptoms detected requiring immediate attention"
        )
    
    # Check vitals for critical conditions
    if vitals.oxygen_saturation and vitals.oxygen_saturation < 90:
        return Action(
            action_type=ActionType.TREAT_NOW,
            priority_score=0.95,
            reasoning="Low oxygen saturation requires immediate intervention"
        )
    
    if vitals.blood_pressure_systolic and vitals.blood_pressure_systolic < 90:
        return Action(
            action_type=ActionType.TREAT_NOW,
            priority_score=0.9,
            reasoning="Low blood pressure indicates possible shock"
        )
    
    # Moderate conditions - MONITOR
    moderate_symptoms = {
        "fever", "pain", "high heart rate", "dehydration",
        "infection", "asthma", "wheezing", "dizziness"
    }
    
    if any(symptom in symptoms_lower for symptom in moderate_symptoms):
        return Action(
            action_type=ActionType.MONITOR,
            priority_score=0.6,
            reasoning="Moderate symptoms requiring monitoring and evaluation"
        )
    
    # Check vitals for moderate conditions
    if vitals.heart_rate and vitals.heart_rate > 100:
        return Action(
            action_type=ActionType.MONITOR,
            priority_score=0.6,
            reasoning="Elevated heart rate requires monitoring"
        )
    
    if vitals.temperature and vitals.temperature > 38.0:
        return Action(
            action_type=ActionType.MONITOR,
            priority_score=0.5,
            reasoning="Fever requires monitoring"
        )
    
    # Mild conditions - WAIT
    return Action(
        action_type=ActionType.WAIT,
        priority_score=0.2,
        reasoning="Mild symptoms that can wait for routine care"
    )

@app.post("/reset", response_model=ResetResponse)
async def reset():
    """Reset the environment and return initial observation."""
    global env, current_observation
    
    try:
        # Initialize environment
        env = HospitalTriageEnv(difficulty="MEDIUM", max_steps=10)
        current_observation = env.reset()
        
        return ResetResponse(status="reset done")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reset failed: {str(e)}")

@app.post("/step", response_model=StepResponse)
async def step(request: StepRequest):
    """Execute a step in the environment."""
    global env, current_observation
    
    if env is None or current_observation is None:
        raise HTTPException(status_code=400, detail="Environment not reset. Call /reset first.")
    
    try:
        # Create action from request
        action = Action(
            action_type=ActionType(request.action),
            priority_score=request.priority_score,
            reasoning=request.reasoning
        )
        
        # Execute step
        next_observation, reward, done, info = env.step(action)
        
        # Update current observation if not done
        if not done:
            current_observation = next_observation
        
        return StepResponse(
            reward=reward,
            done=done,
            info=info
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Step failed: {str(e)}")

@app.get("/state", response_model=StateResponse)
async def get_state():
    """Get current patient state."""
    global current_observation
    
    if current_observation is None:
        raise HTTPException(status_code=400, detail="No active observation. Call /reset first.")
    
    try:
        return StateResponse(
            patient_id=current_observation.patient_id,
            symptoms=current_observation.symptoms
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"State retrieval failed: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {"message": "AI Hospital Triage System API", "version": "1.0.0"}

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "environment_loaded": env is not None}

# Environment variables validation
def validate_environment():
    """Ensure required environment variables exist."""
    required_vars = ["API_BASE_URL", "MODEL_NAME", "HF_TOKEN"]
    missing_vars = []
    
    for var in required_vars:
        if var not in os.environ:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"Warning: Missing environment variables: {missing_vars}")
        print("Setting default values...")
        
        # Set default values if missing
        if "API_BASE_URL" not in os.environ:
            os.environ["API_BASE_URL"] = "https://api.openai.com/v1"
        if "MODEL_NAME" not in os.environ:
            os.environ["MODEL_NAME"] = "gpt-3.5-turbo"
        if "HF_TOKEN" not in os.environ:
            os.environ["HF_TOKEN"] = "dummy-token"

if __name__ == "__main__":
    # Validate environment variables
    validate_environment()
    
    # Run FastAPI server
    uvicorn.run(
        "inference:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
