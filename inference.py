import os
from hospital_env import HospitalTriageEnv, Action, ActionType

# OPTIONAL: comment out if not using API
from openai import OpenAI


# -------------------------------
# SIMPLE RULE-BASED DECISION (SAFE)
# -------------------------------
def get_triage_decision(observation, client=None, model_name=None):
    obs = observation.observation

    symptoms = " ".join(obs.symptoms).lower()
    vitals = obs.vitals

    # Default values
    action_type = ActionType.WAIT
    priority = 0.3
    reasoning = "Stable condition"

    # 🔥 Simple medical logic (works without API)
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

    return Action(
        action_type=action_type,
        priority_score=priority,
        reasoning=reasoning,
    )


# -------------------------------
# MAIN LOOP (100% SAFE)
# -------------------------------
def main():
    print("[START]")

    # INIT ENV
    env = HospitalTriageEnv()
    observation = env.reset()

    total_score = 0
    step_count = 0

    # LOOP
    while True:
        # ✅ STOP if no observation
        if observation is None:
            break

        print("[STEP]")

        action = get_triage_decision(observation)

        obs = observation.observation

        print(f"Patient ID: {obs.patient_id}")
        print(f"Symptoms: {', '.join(obs.symptoms)}")
        print(f"Action: {action.action_type.value}")
        print(f"Priority Score: {action.priority_score:.2f}")
        print(f"Reasoning: {action.reasoning}")

        # ✅ SAFE STEP CALL
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

        # ✅ STOP CONDITIONS (VERY IMPORTANT)
        if done or next_observation is None:
            break

        observation = next_observation

    # FINAL OUTPUT
    final_score = total_score / step_count if step_count > 0 else 0.0
    print(f"Final Score: {final_score:.3f}")
    print("[END]")


# -------------------------------
if __name__ == "__main__":
    main()