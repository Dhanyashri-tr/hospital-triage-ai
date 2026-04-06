import os
from fastapi import FastAPI
from hospital_env import HospitalTriageEnv, Action, ActionType

# REQUIRED ENV VARIABLES
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.getenv("HF_TOKEN")

app = FastAPI()

env = None

# ---------------------------
# TRIAGE LOGIC (SAFE)
# ---------------------------
def get_action(obs):
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
        reasoning = "Moderate symptoms"

    return Action(
        action_type=action_type,
        priority_score=priority,
        reasoning=reasoning,
    )

# ---------------------------
# REQUIRED ENDPOINTS
# ---------------------------

@app.post("/reset")
def reset():
    global env
    env = HospitalTriageEnv()
    observation = env.reset()

    return {
        "patient_id": observation.observation.patient_id,
        "symptoms": observation.observation.symptoms
    }


@app.post("/step")
def step():
    global env

    observation = env.current_observation
    action = get_action(observation.observation)

    next_obs, reward, done, info = env.step(action)

    return {
        "action": action.action_type.value,
        "priority": action.priority_score,
        "reward": reward,
        "done": done
    }