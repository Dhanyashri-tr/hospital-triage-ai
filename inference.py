import os
from fastapi import FastAPI, Request
from env import HospitalTriageEnv
from models import Action, ActionType

app = FastAPI()

# -------------------------------
# RULE-BASED DECISION FUNCTION
# -------------------------------
def get_triage_decision(observation):
    obs = observation.observation

    symptoms = " ".join(obs.symptoms).lower()
    vitals = obs.vitals

    action_type = ActionType.WAIT
    priority = 0.3
    reasoning = "Stable condition"

    if (
        "chest pain" in symptoms
        or "unconscious" in symptoms
        or (vitals and vitals.oxygen_saturation and vitals.oxygen_saturation < 90)
    ):
        action_type = ActionType.TREAT_NOW
        priority = 0.95
        reasoning = "Critical symptoms detected"

    elif (
        "fever" in symptoms
        or "pain" in symptoms
        or (vitals and vitals.heart_rate and vitals.heart_rate > 100)
    ):
        action_type = ActionType.MONITOR
        priority = 0.6
        reasoning = "Moderate symptoms, needs monitoring"

    return action_type.value, priority, reasoning


# -------------------------------
# GLOBAL ENV
# -------------------------------
env = None


# -------------------------------
# ROOT ENDPOINT
# -------------------------------
@app.get("/")
def home():
    return {"status": "ok"}


# -------------------------------
# RESET ENDPOINT (FIXED ✅)
# -------------------------------
@app.post("/reset")
def reset():
    global env

    env = HospitalTriageEnv()   # ✅ correct class
    observation = env.reset()   # ✅ MUST call reset

    return {
        "message": "Environment reset successful",
        "patient_id": observation.patient_id if hasattr(observation, "patient_id") else ""
    }


# -------------------------------
# STEP ENDPOINT
# -------------------------------
@app.post("/step")
async def step(request: Request):
    global env

    if env is None:
        env = HospitalTriageEnv()
        observation = env.reset()
    else:
        observation = env.current_case.observation if env.current_case else None
        if observation is None:
            observation = env.reset()

    action_type, priority, reasoning = get_triage_decision(observation)

    action = Action(
        action_type=ActionType(action_type),
        priority_score=priority,
        reasoning=reasoning,
    )

    next_observation, reward, done, info = env.step(action)

    return {
        "reward": reward,
        "done": done,
        "info": info
    }


# -------------------------------
# STATE ENDPOINT
# -------------------------------
@app.get("/state")
async def state():
    global env
    
    if env is None or env.current_case is None:
        return {"patient_id": "", "symptoms": []}
    
    obs = env.current_case.observation
    return {
        "patient_id": obs.patient_id,
        "symptoms": obs.symptoms
    }


# -------------------------------
# RUN SERVER (FIXED PORT ✅)
# -------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)