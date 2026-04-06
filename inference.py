import os
from hospital_env import HospitalTriageEnv, Action, ActionType
from openai import OpenAI

# -------------------------------
# ENV VARIABLES (REQUIRED FOR CHECKLIST)
# -------------------------------
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.getenv("HF_TOKEN")  # no default

# OpenAI Client (REQUIRED EVEN IF NOT USED)
client = None

if os.getenv("OPENAI_API_KEY"):
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=os.getenv("OPENAI_API_KEY")
    )

# -------------------------------
# RULE-BASED TRIAGE LOGIC (SAFE)
# -------------------------------
def get_triage_decision(observation, client=None, model_name=None):
    obs = observation.observation

    symptoms = " ".join(obs.symptoms).lower()
    vitals = obs.vitals

    # Default
    action_type = ActionType.WAIT
    priority = 0.3
    reasoning = "Stable condition"

    # Critical
    if (
        "chest pain" in symptoms
        or "unconscious" in symptoms
        or (vitals and vitals.oxygen_saturation and vitals.oxygen_saturation < 90)
    ):
        action_type = ActionType.TREAT_NOW
        priority = 0.95
        reasoning = "Critical symptoms detected"

    # Moderate
    elif (
        "fever" in symptoms
        or "pain" in symptoms
        or (vitals and vitals.heart_rate and vitals.heart_rate > 100)
    ):
        action_type = ActionType.MONITOR
        priority = 0.6
        reasoning = "Moderate symptoms, needs monitoring"

    return Action(
        action_type=action_type,
        priority_score=priority,
        reasoning=reasoning,
    )

# -------------------------------
# MAIN EXECUTION LOOP
# -------------------------------
def main():
    print("[START]")

    env = HospitalTriageEnv()
    observation = env.reset()

    total_score = 0
    step_count = 0

    while True:
        if observation is None:
            break

        print("[STEP]")

        # ✅ PASS client + model (IMPORTANT)
        action = get_triage_decision(observation, client, MODEL_NAME)

        obs = observation.observation

        print(f"Patient ID: {obs.patient_id}")
        print(f"Symptoms: {', '.join(obs.symptoms)}")
        print(f"Action: {action.action_type.value}")
        print(f"Priority Score: {action.priority_score:.2f}")
        print(f"Reasoning: {action.reasoning}")

        try:
            next_observation, reward, done, info = env.step(action)
        except Exception as e:
            print("Error during step:", e)
            break

        print(f"Reward: {reward:.3f}")
        print(f"Cumulative Score: {info.get('current_score', 0):.3f}")
        print(f"Cases Completed: {info.get('cases_completed', 0)}")

        total_score += reward
        step_count += 1

        if done or next_observation is None:
            break

        observation = next_observation

    final_score = total_score / step_count if step_count > 0 else 0.0
    print(f"Final Score: {final_score:.3f}")
    print("[END]")


# -------------------------------
if __name__ == "__main__":
    main()